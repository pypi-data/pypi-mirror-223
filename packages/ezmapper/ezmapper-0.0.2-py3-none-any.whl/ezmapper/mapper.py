import logging
import os
import re
import sys
import traceback
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any, Literal, Optional

import numpy as np
import pandas as pd
import yaml
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from yaml.loader import SafeLoader

from ezmapper.utils import dates as util_dates
from ezmapper.utils import excel_formatting

logger = logging.getLogger()


@dataclass
class EntryMapping:
    column: str | Literal["CREATE_COLUMN()"]
    rule_value: Optional[list[str] | str] = None
    default_value: Optional[str | int | float | bool] = None
    override: Optional[str] = None


@dataclass
class ConfigMapping:
    id_column: Optional[str] = None
    comment_column: Optional[str] = None


@dataclass
class MapperMapping:
    mapping: dict[str, EntryMapping]
    config: ConfigMapping
    filters: list[str]

    def __init__(
        self,
        mapping: dict[str, str | Literal["CREATE_COLUMN()"] | dict],
        config: Optional[dict] = None,
        filters: Optional[list[str] | str] = None,
    ):
        # init mapping
        self.mapping = {}
        for col, entry in mapping.items():
            if isinstance(entry, dict):
                self.mapping[col] = EntryMapping(**entry)
            if isinstance(entry, str):
                self.mapping[col] = EntryMapping(column=entry, default_value="")

        # init config
        if isinstance(config, dict):
            self.config = ConfigMapping(**config)
        else:
            self.config = ConfigMapping()

        # init filters
        if isinstance(filters, str):
            self.filters = [filters]
        elif isinstance(filters, list):
            self.filters = filters
        else:
            self.filters = []


class MapperKeys(Enum):
    """
    Enum class containing special functions used in mapper YAML file.
    """

    DATE_FUNCTION = "DATE"  # Parses str_date to date_object
    CREATE_COLUMN = "CREATE_COLUMN()"  # Create a new column


class MapperKeysExcel(Enum):
    """
    Enumeration class for the names of the Excel sheets and columns used by the
    `Mapper` class when reading and writing to Excel files.
    """

    # Excel Sheets
    SHEET_CONFIG = "Config"
    SHEET_COLUMNS = "Columns"
    SHEET_FILTERS = "Filters"

    # Excel Columns Columns Sheet
    COL_NEW_COLUMN = "New Column"
    COL_OLD_COLUMN = "Old Column"
    COL_OVERRIDE = "Override Column"
    COL_VALUE_RULE = "Value Rule"
    COL_DEFAULT_VALUE = "Default Value"
    # Config Sheet
    COL_COLUMN_USED = "Column Used"
    # Filter Sheet
    COL_FILTERS = "Filters"


class Mapper:
    """
    Mapper class is a simple ETL.

    This class allows you to load a YAML mapping file or provide a dictionary of
    mapping directly. You can then apply the mapping to a pandas DataFrame using
    the `load()` method or reverse the mapping using the `dump()` method.

    The YAML mapping file should follow the structure described in the
    `MapperKeys` enum class, with entries for `config`, `filters`, and either
    new columns to create or existing columns to modify. You can also define
    default value rules using the `MapperKeys` enum class.

    These rules are applied when using the `load()` method.

    You can save the mapping to an Excel file using the `to_excel()` method or
    load the mapping from an Excel file using the `from_excel()` class method.
    The Excel file should follow the structure described in the
    `MapperKeysExcel` enum class.
    """

    def __init__(
        self, yaml_file_path: str | Path | None = None, mapper_dict: dict | None = None
    ) -> None:
        """
        Initializes an instance of the Mapper class.

        Args:
            yaml_file_path (str | Path | None): Path to the YAML file containing
                the mapping.If None, then `mapper_dict` must be provided. Defaults to None.
            mapper_dict (dict | None): Dictionary containing the mapping. If
                None, then `yaml_file_path` must be provided. Defaults to None.

        Raises:
            ValueError: If neither `yaml_file_path` nor `mapper_dict` is
            provided, or if `yaml_file_path` does not exist.
        """
        self._yaml_file_path = yaml_file_path

        # Last value_rules execution will be saved here in df format
        self._df_value_rules = pd.DataFrame()

        if yaml_file_path:
            if not os.path.isfile(yaml_file_path):
                logger.exception(f'Mapper file: "{yaml_file_path}" does not exist')
                raise ValueError(f'Mapper file: "{yaml_file_path}" does not exist')

            with open(yaml_file_path) as f:
                _mapping = yaml.load(f, Loader=SafeLoader)
                self._mapping = MapperMapping(**_mapping)

        elif mapper_dict:
            self._mapping = MapperMapping(**mapper_dict)

        else:
            logger.exception("No mapping passed to Mapper()")
            raise ValueError("No mapping passed to Mapper()")

    #################### Properties #####################
    #####################################################

    @property
    def required_columns(self):
        _required_columns = list(self.load_rename_dict.keys())
        _override_cols = self.columns_with_attr("override")
        _original_override_cols = [
            self._mapping.mapping[x].override for x in _override_cols  # type: ignore
        ]
        _original_override_cols = [
            override_col
            for override_col in _original_override_cols
            if isinstance(override_col, str)
        ]
        return _required_columns + _original_override_cols

    @property
    def load_rename_dict(self) -> dict[str, str]:
        """
        dict: Returns a dictionary to rename columns in a DataFrame based on the
        entries in the mapper YAML file.
        """
        dict_to_rename = {}
        for col, entry in self._mapping.mapping.items():
            if entry.column == MapperKeys.CREATE_COLUMN.value:
                continue
            if entry.column in dict_to_rename:
                raise ValueError(f"Same column can't be renamed twice '{entry.column}'")
            dict_to_rename[entry.column] = col

        return dict_to_rename

    @property
    def dump_rename_dict(self) -> dict:
        """
        dict: Returns a dictionary mapping the renamed column names to their
        original names.
        """
        return {v: k for k, v in self.load_rename_dict.items()}

    @property
    def df_value_rules(self) -> pd.DataFrame:
        """
        pd.DataFrame: This property returns the dataframe containing the
        DEFAULT_VALUE_RULE entries of the YAML mapper, ordered based on the
        order of appearance in the mapper file.
        """
        return self._df_value_rules

    ###################   Functions  ####################
    #####################################################

    # Columns related functions

    def columns_with_attr(
        self,
        attr_name: Literal["column"]
        | Literal["rule_value"]
        | Literal["default_value"]
        | Literal["override"],
    ) -> list[str]:
        """
        Returns a list of column names in the mapper file that have a specific
        attribute defined.

        Args:
            attr_name (MapperKeys): The attribute name to search for.

        Returns:
            list[str]: A list of column names that have the attribute defined.
        """
        return list(
            filter(
                lambda col: isinstance(self._mapping.mapping[col], EntryMapping)
                and getattr(self._mapping.mapping[col], attr_name) is not None,
                self._mapping.mapping.keys(),
            )
        )

    def columns_created(self) -> list[str]:
        """
        Return a list of columns that are created in the mapping file.

        Returns:
            list[str]: A list of columns that are created in the mapping file.

        """

        def filter_new_columns(col: str) -> bool:
            yaml_entry = self._mapping.mapping[col]
            return (yaml_entry == MapperKeys.CREATE_COLUMN.value) or (
                isinstance(yaml_entry, EntryMapping)
                and yaml_entry.column == MapperKeys.CREATE_COLUMN.value
            )

        return list(filter(filter_new_columns, self._mapping.mapping.keys()))

    def columns_mapped(self, df: pd.DataFrame) -> list[str]:
        """
        This method returns a list of columns present in both the YAML data and
        the input dataframe.

        Args:
            df (pd.DataFrame): Input dataframe to check for mapped columns.

        Returns:
            list[str]: List of column names that are present in both the YAML
            data and the input dataframe
        """
        return list(set(self._mapping.mapping.keys()).intersection(set(df.columns)))

    def column_comments(self, df: pd.DataFrame) -> None | str:
        """
        Extracts the column name to be used as a comment column from the mapper
        config.

        Args:
            df (pd.DataFrame): The DataFrame to be checked.

        Returns:
            str or None: The name of the column to be used for comments in the
            DataFrame. Returns None if no comment column is defined in the
            mapper config, or if the specified comment column is not present in
            the DataFrame.
        """

        comment_column = self._mapping.config.comment_column

        # Check if Comment colum has been declared under config key
        if comment_column is None:
            return None

        # Check if column is present in the df
        if comment_column not in df.columns:
            logger.error(
                f'comment_column: "{comment_column}"' " is not present in the dataframe"
            )
            return None

        return comment_column

    #####################    IO    ######################

    # DataFrame

    def load(
        self,
        df: pd.DataFrame,
        *,
        renaming: bool = True,
        overrides: bool = True,
        filters: bool = True,
        drop_unmapped_columns: bool = True,
        create_columns: bool = True,
        rule_values: bool = True,
        save_rule_value: bool = False,
    ) -> pd.DataFrame:
        """
        Args:
            df (pd.DataFrame): The input DataFrame to load.
            overrides (bool, optional): Whether to apply column values overrides.
                Defaults to True.
            filters (bool, optional): Whether to apply filters based on YAML entries.
                Defaults to True.
            create_columns (bool, optional): Whether to apply CREATE_COLUMN() and
                default_value. Defaults to True.
            rule_values (bool, optional): Whether to apply rule_value.
                Defaults to True.
            save_rule_value (bool, optional): Whether to save executed
                default_value rules in the mapper instance. Defaults to False.

        Returns:
            pd.DataFrame: The loaded DataFrame.

        Raises:
            ValueError: If the mapper has no config or column_id entries.
            ValueError: If the column_id specified in the mapper is not present in
                the input DataFrame.
            ValueError: If the column specified as column_id is not unique.
            ValueError: If in entry that defines new column, default_value is not defined.
            ValueError: If the rule_value value is not valid (neither a
                string nor a list).

        Example:
            >>> mapper = Mapper("mapper.yaml")
            >>> df = pd.read_csv("data.csv")
            >>> df_mapped = mapper.load(df)
            >>> df_dumped = mapper.dump(df_mapped)
        """
        # 0. Make a copy of the df in order to not modify the original df
        df = df.copy()
        df.fillna(value="", inplace=True)

        # 1. Apply column renaming
        if renaming:
            df = self._apply_column_renaming(df)
        df = self._apply_index(df)

        # 2. Apply column values overrides
        if overrides:
            df = self._apply_overrides(df)

        # 3. Apply filters
        if filters:
            # Filter by rows based on yaml filters entries
            df = self._apply_filters(df)

        # 4. Keep mapped columns
        if drop_unmapped_columns:
            mapped_columns = self.columns_mapped(df)
            logger.debug(f"Keeping mapped columns: {mapped_columns}")
            df = df[mapped_columns]

        # 5. Apply CREATE_COLUMN() and default_value
        if create_columns:
            df = self._apply_new_columns(df)

        # 6. Apply rule_value
        if rule_values:
            df = self._apply_rule_value(df, save_rule_value)

        # 7. Order COLUMNS by order of appearance in the mapper
        df = self._apply_ordering(df)

        df.replace("", np.nan, inplace=True)
        return df

    def dump(
        self,
        df: pd.DataFrame,
        rename_columns: bool = True,
        drop_created_columns: bool = True,
    ) -> pd.DataFrame:
        """
        Rename and drop columns in a dataframe based on mapper configuration.

        Args:
            df (pd.DataFrame): DataFrame to be dumped
            rename_columns (bool, optional): Whether to rename columns in df.
                Defaults to True.
            drop_created_columns (bool, optional): Whether to drop columns
                created by the mapper in df. Defaults to True.

        Returns:
            pd.DataFrame: A DataFrame with columns renamed and created columns
            dropped, according to mapper configuration.

        Example:
            >>> mapper = DataFrameMapper("mapper.yaml")
            >>> df = pd.read_csv("data.csv")
            >>> df_mapped = mapper.load(df)
            >>> df_dumped = mapper.dump(df_mapped)
        """
        df = df.copy()

        if rename_columns:
            df = df.rename(self.dump_rename_dict, axis="columns")
        if drop_created_columns:
            df = df.drop(self.columns_created(), axis="columns", errors="ignore")  # type: ignore

        return df

    # Mapper

    def to_excel(self, output_file: str | Path) -> None:
        """
        The to_excel method writes the mapper object into an excel file with
        three sheets: columns, filters, and config.

        Args:
            output_file (str | Path): The output excel file path.
        """

        df_config = pd.DataFrame.from_dict(
            self._mapping.config.__dict__,
            orient="index",
            columns=[MapperKeysExcel.COL_COLUMN_USED.value],
        )

        df_filters = pd.DataFrame(
            {MapperKeysExcel.COL_FILTERS.value: self._mapping.filters}
        )

        dict_columns = {
            MapperKeysExcel.COL_NEW_COLUMN.value: [],
            MapperKeysExcel.COL_OLD_COLUMN.value: [],
            MapperKeysExcel.COL_OVERRIDE.value: [],
            MapperKeysExcel.COL_DEFAULT_VALUE.value: [],
            MapperKeysExcel.COL_VALUE_RULE.value: [],
        }

        for col, entry in self._mapping.mapping.items():
            if isinstance(entry, str):
                old_column = entry
                override_column = ""
                value_rule = ""
                default_value = ""
            else:
                # value = defaultdict(str, value.__dict__)
                old_column = entry.column
                override_column = entry.override
                default_value = entry.default_value
                value_rule = entry.rule_value
                if isinstance(value_rule, list):
                    value_rule = "\n".join(value_rule)

            dict_columns[MapperKeysExcel.COL_NEW_COLUMN.value].append(col)
            dict_columns[MapperKeysExcel.COL_OLD_COLUMN.value].append(old_column)
            dict_columns[MapperKeysExcel.COL_OVERRIDE.value].append(override_column)
            dict_columns[MapperKeysExcel.COL_VALUE_RULE.value].append(value_rule)
            dict_columns[MapperKeysExcel.COL_DEFAULT_VALUE.value].append(default_value)

        df_columns = pd.DataFrame(dict_columns)

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
            df_columns.to_excel(
                writer, sheet_name=MapperKeysExcel.SHEET_COLUMNS.value, index=False
            )
            df_filters.to_excel(writer, sheet_name=MapperKeysExcel.SHEET_FILTERS.value)
            df_config.to_excel(writer, sheet_name=MapperKeysExcel.SHEET_CONFIG.value)

    @classmethod
    def from_excel(cls, excel_file: str | Path) -> "Mapper":
        """
        Creates a Mapper instance from an Excel file.

        Args:
            excel_file (str): path to Excel file.

        Returns:
            Mapper: An Mapper instance.

        Raises:
            ValueError: If the Excel file does not contain the necessary sheets
            or columns.
        """
        # Read excel file
        with pd.ExcelFile(excel_file, engine="openpyxl") as xls:
            # Load columns sheet
            df_columns = pd.read_excel(xls, MapperKeysExcel.SHEET_COLUMNS.value)

            # Process filters sheet
            filters_data = pd.read_excel(xls, MapperKeysExcel.SHEET_FILTERS.value)[
                MapperKeysExcel.COL_FILTERS.value
            ].tolist()

            # Process config sheet
            config_data = pd.read_excel(
                xls, MapperKeysExcel.SHEET_CONFIG.value, index_col=0
            )[MapperKeysExcel.COL_COLUMN_USED.value].to_dict()

        # Create yaml_data
        yaml_data = {
            "config": config_data,
            "filters": filters_data,
            "mapping": cls._df_columns_to_dict(df_columns),
        }

        # Create an instance of the class with the loaded yaml_data
        instance = cls(mapper_dict=yaml_data)

        return instance

    # Value Changes Report

    def to_excel_value_changes_report(self, output_excel_file: str | Path):
        # Create an ExcelWriter object
        summary_by_column: pd.DataFrame
        column_name = "Column Name"
        number_of_modifications = "Number of Modifications"
        rules_col = "Rules"
        column_id = self._mapping.config.id_column
        with pd.ExcelWriter(output_excel_file) as writer:
            # Create the 'Summary by Column Name' report
            #####################################################################
            summary_by_column = (
                self._df_value_rules.xs("new", axis=1, level=1, drop_level=False)
                .count()
                .reset_index()  # type: ignore
            )
            summary_by_column.columns = [column_name, "_", number_of_modifications]
            summary_by_column[column_name] = summary_by_column[column_name].str.replace(
                "_new", "", regex=False
            )
            summary_by_column = summary_by_column[
                [column_name, number_of_modifications]
            ]
            # Add rules descriptions
            rules = {column_name: [], rules_col: []}
            for col in self.columns_with_attr("rule_value"):
                entry = self._mapping.mapping[col]
                rules[column_name].append(col)
                rules[rules_col].append(entry.rule_value)  # type: ignore
            rules = pd.DataFrame(rules)
            rules[rules_col] = rules[rules_col].apply(
                lambda x: "\n".join(x) if isinstance(x, list) else x
            )
            summary_by_column = pd.merge(summary_by_column, rules, on=column_name)
            summary_by_column = summary_by_column.sort_values(
                number_of_modifications, ascending=False
            )
            # Save the 'Summary by Column Name' report to a sheet
            summary_by_column.to_excel(
                writer, sheet_name="Summary by Column Name", index=False
            )

            # Create the 'Summary by id' report
            #####################################################################
            df_dropped = self._df_value_rules.iloc[1:]
            modifications_count = df_dropped.xs("new", axis=1, level=1).count(axis=1)  # type: ignore
            modified_columns = df_dropped.xs("new", axis=1, level=1).apply(
                lambda row: ", ".join(row.dropna().index), axis=1
            )
            # Combine the count and column names into a DataFrame
            summary_by_id = pd.DataFrame(
                {
                    column_id: df_dropped.index,
                    number_of_modifications: modifications_count,
                    "Modified Columns": modified_columns,
                }
            )
            summary_by_id = summary_by_id.sort_values(
                number_of_modifications, ascending=False
            )
            # Save the 'Summary by id' report to a sheet
            summary_by_id.to_excel(writer, sheet_name="Summary by ID", index=False)

            # Create New Columns Summary Report
            #####################################################################
            new_cols = {
                column_name: [],
                "default_value": [],
                rules_col: [],
            }
            for col in self.columns_created():
                new_cols[column_name].append(col)
                entry = self._mapping.mapping[col]

                if isinstance(entry, str):
                    new_cols["default_value"].append(None)
                    new_cols[rules_col].append(None)

                else:
                    new_cols["default_value"].append(entry.default_value)

                    if isinstance(entry.rule_value, list):
                        new_cols[rules_col].append("\n".join(entry.rule_value))
                    else:
                        new_cols[rules_col].append(entry.rule_value)

            pd.DataFrame(new_cols).to_excel(
                writer, sheet_name="New Columns", index=False
            )

            # Create Renaming Report
            #####################################################################
            renaming = {
                "Source Column": [],
                MapperKeysExcel.COL_OVERRIDE.value: [],
                MapperKeysExcel.COL_NEW_COLUMN.value: [],
            }
            for source_col, new_col in self.load_rename_dict.items():
                renaming["Source Column"].append(source_col)
                renaming[MapperKeysExcel.COL_NEW_COLUMN.value].append(new_col)
                entry = self._mapping.mapping[new_col]
                renaming[MapperKeysExcel.COL_OVERRIDE.value].append(
                    entry.override if isinstance(entry, EntryMapping) else None
                )

            pd.DataFrame(renaming).to_excel(
                writer, sheet_name="Columns Mapping", index=False
            )

            # Create Filters
            #####################################################################
            if self._mapping.filters:
                filters = self._mapping.filters
                if isinstance(filters, str):
                    filters = [filters]
                dict_filters = {"Filter Rules": filters}
                pd.DataFrame(dict_filters).to_excel(
                    writer, sheet_name="Row Filters", index=False
                )

            # Save the original DataFrame to a sheet
            #####################################################################
            self._df_value_rules.dropna(axis="index", how="all").to_excel(
                writer, sheet_name="Changes - Deep Dive"
            )

        excel_formatting.auto_fit_width(output_excel_file)
        excel_formatting.auto_wrap_text(
            output_excel_file, sheet_name="Summary by Column Name"
        )
        excel_formatting.auto_wrap_text(output_excel_file, sheet_name="New Columns")
        return summary_by_column.drop([rules_col], axis=1, errors="ignore")

    #####################  Parser  ######################

    # Apply functions

    def _apply_ordering(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies column ordering based on the order of the columns in the mapper
        file.

        Args:
            df: DataFrame to be ordered.

        Returns:
            Ordered DataFrame.
        """
        df = df.reset_index()

        mapper_order = list(
            filter(
                lambda x: x in df.columns,
                self._mapping.mapping.keys(),
            )
        )

        df = df[mapper_order]

        return df

    def _apply_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Applies the index on a given DataFrame using a column specified in the
        mapper YAML file.

        Args:
            df (pd.DataFrame): DataFrame to have its index set.

        Raises:
            ValueError: When logging_id is not present in the mapper YAML file.
            ValueError: When logging_id is not present under "config" in the
            mapper YAML file. ValueError: When the column specified in
            logging_id is not present in the DataFrame. ValueError: When the
            column specified in logging_id is not unique.

        Returns:
            pd.DataFrame: DataFrame with its index set.
        """

        column_id = self._mapping.config.id_column

        if column_id is None:
            column_id = "__index"
            df[column_id] = range(len(df))

        if column_id not in df.columns:
            logger.exception(
                f'Column ID: "{column_id}" is not present in the DataFrame'
            )
            raise ValueError(
                f'Column ID: "{column_id}" is not present in the DataFrame'
            )

        # Check that logging_id has unique values
        if not df[column_id].is_unique:
            logger.exception(f"Column {column_id} must contain unique values")
            raise ValueError(f"Column {column_id} must contain unique values")

        # Set Index
        df = df.set_index(column_id)

        return df

    def _apply_column_renaming(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply column renaming to the DataFrame based on the YAML configuration.

        Args:
            df (pd.DataFrame): The DataFrame to rename columns in.

        Returns:
            pd.DataFrame: The DataFrame with columns renamed.
        """

        load_rename_dict = self.load_rename_dict
        logger.debug(
            f"Column renaming. See '{self._yaml_file_path}' for more information."
        )

        # Error for unused mapper columns
        unused_df_columns = list(set(load_rename_dict.keys()) - set(df.columns))

        for col in unused_df_columns:
            logger.error(
                f"Column '{col}' not included. Is present in mapper:"
                f"'{self._yaml_file_path}' but not in df.columns"
            )
        if unused_df_columns:
            raise ValueError(
                f"Columns '{unused_df_columns}' not included. They are in mapper:"
                f"'{self._yaml_file_path}' but not in df.columns"
            )

        df = df.rename(load_rename_dict, axis="columns")

        return df

    def _apply_overrides(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply column overrides to the DataFrame based on the YAML configuration.

        Args:
            df (pd.DataFrame): The DataFrame to apply overrides to.

        Returns:
            pd.DataFrame: The DataFrame with column overrides applied.
        """

        # def apply_column_override(row: pd.Series, col: str):
        #     col_override = self._mapping.mapping[col][
        #         MapperKeys.OVERRIDE.value
        #     ]
        #     row = row.fillna("")
        #     return row[col_override] if row[col_override] != "" else row[col]

        # override_columns = self.columns_with_attr(MapperKeys.OVERRIDE)
        # logger.debug(f"Running override rules for columns: {override_columns}")
        # for col in override_columns:
        #     # Double check that the column exists
        #     if col in df.columns:
        #         df[col] = df.apply(apply_column_override, col=col, axis=1)
        # return df

        # Get columns with override attribute
        override_columns = self.columns_with_attr("override")

        logger.debug(f"Running override rules for columns:{override_columns}")

        # Apply overrides
        for col in override_columns:
            if col in df.columns:
                col_override = self._mapping.mapping[col].override  # type: ignore
                # Using vectorized operations
                mask = df[col_override] != ""
                df.loc[mask, col] = df.loc[mask, col_override]

        return df

    def _apply_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply filters to the DataFrame based on the YAML configuration.

        Args:
            df (pd.DataFrame): The DataFrame to apply filters to.

        Returns:
            pd.DataFrame: The filtered DataFrame with rows matching the filter
            criteria.

        """
        filters = self._mapping.filters

        if len(filters) == 0:
            logger.debug(
                f"No filters detected in the YAML file: {self._yaml_file_path}"
            )
            return df

        logger.debug(f"Loaded filters: {filters}")

        # Init mask to the len of the dataframe
        mask = pd.Series(data=False, index=df.index)

        # Run Filter on the dataframe
        for filter in filters:
            mask = mask | df.apply(
                self._parse_value, value=self._preprocess_values(df, filter), axis=1  # type: ignore
            )

        df_filtered = df[mask]

        logger.debug(
            f"Filters applied, keeping {len(df_filtered)} rows from {len(df)} total rows"
        )

        return df_filtered

    def _apply_new_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Create new columns in the DataFrame as specified in the YAML
        configuration.

        Args:
            df (pd.DataFrame): The DataFrame to add new columns to.

        Returns:
            pd.DataFrame: The updated DataFrame with the new columns added.

        Raises:
            ValueError: If the default value for a new column is not defined in
            the YAML file.
        """
        new_columns = self.columns_created()
        logger.debug(f"Creating new columns: {new_columns}")

        for new_column in new_columns:
            entry = self._mapping.mapping[new_column]

            raw_value = ""
            if entry.default_value is None:
                logger.exception(
                    f"The 'default_value' for column "
                    f'"{new_column}" is not defined in the yaml file'
                )
                raise ValueError(
                    f"The 'default_value' for column "
                    f'"{new_column}" is not defined in the yaml file'
                )

            raw_value = entry.default_value  # type: ignore

            # Create the new column with the default value
            df[new_column] = df.apply(
                self._parse_value,  # type: ignore
                value=self._preprocess_values(df, raw_value, new_column),
                axis=1,
            )

            logger.debug(f'New column: "{new_column}"; Value: {raw_value}')

        return df

    def _apply_rule_value(
        self, df: pd.DataFrame, save_rule_value: bool = False
    ) -> pd.DataFrame:
        """
        Apply default value rules on the specified columns and update the
        DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to apply default value rules to.
            save_rule_value (bool): Flag indicating whether to save the
            applied default value rules.

        Returns:
            pd.DataFrame: The updated DataFrame after applying default value
            rules.

        """

        default_value_columns = self.columns_with_attr("rule_value")
        logger.debug(f"Running default value rules on columns: {default_value_columns}")

        df_pre_rules = df.copy()

        comments_column = self.column_comments(df)
        if comments_column:
            df[comments_column] = ""

        if save_rule_value:
            # Create an empty df to store the executed value rules
            columns = pd.MultiIndex(
                levels=[[], []], codes=[[], []], names=["Column Name", ""]
            )
            self._df_value_rules = pd.DataFrame(index=df.index, columns=columns)

        for default_value_column in default_value_columns:
            updated_col = self._parse_rule_value(df_pre_rules, default_value_column)

            if save_rule_value or comments_column:
                df_cmp = pd.DataFrame(
                    {
                        "old": df[default_value_column],  # .fillna(""),
                        "new": updated_col,  # .fillna(""),
                    }
                )

                # dtype datetime
                for col_datetime in [
                    column for column in df_cmp.columns if is_datetime(df_cmp[column])
                ]:
                    df_cmp[col_datetime] = pd.to_datetime(df_cmp[col_datetime]).dt.date

                if save_rule_value:
                    self._df_value_rules[default_value_column, "old"] = df_cmp.apply(
                        self._get_diff_col, get_col="old", axis=1
                    )
                    self._df_value_rules[default_value_column, "new"] = df_cmp.apply(
                        self._get_diff_col, get_col="new", axis=1
                    )
                if comments_column:
                    # Add modified columns and values to comment_column Format:
                    # modified_column(old -> new), ...,
                    comments = df_cmp.apply(
                        self._get_diff_values_comment,
                        old="old",
                        new="new",
                        default_value_column=default_value_column,
                        axis=1,
                    )
                    df[comments_column] = df[comments_column] + comments

            df[default_value_column] = updated_col

        return df

    # Parse functions

    def _parse_value(self, row: pd.Series, value: str | int | bool | None):
        """
        Parse and evaluate the given value expression for the provided row.

        Args:
            row (pd.Series): A pandas Series representing a row of data.
            value(str | int | bool | None): The value expression to be parsed and
                evaluated.

        Returns:
            The evaluated value based on the provided row.

        Raises:
            NameError: If the evaluation of the value expression encounters a
            name error.
        """

        if value == "":
            return ""

        if not isinstance(value, str):
            return value

        # row = row.fillna(value="")

        try:
            parsed_value = eval(
                value, {"pd": pd, "util_dates": util_dates}, {"row": row}
            )
        except NameError:
            parsed_value = eval(
                f'"{value}"', {"pd": pd, "util_dates": util_dates}, {"row": row}
            )
        except Exception:
            logger.exception(traceback.format_exc())
            logger.error(
                f'at row ID "{row.name}" expression/Value "{value}" caused an exception.'
            )
            matches = list(set(re.findall(r"row\['(.*?)'\]", value)))
            if matches:
                logger.error([f"row['{match}'] = {row[match]}" for match in matches])
            sys.exit()

        return parsed_value

    def _parse_rule(
        self, df: pd.DataFrame, rule: str, col: str = ""
    ) -> tuple[str, str]:
        """
        Parse a rule from the YAML data for the given column.

        Args:
            df (pd.DataFrame): A pandas DataFrame containing the data. rule
            (str): A string containing the rule to be parsed. col (str,
            optional): Column name to be used in the rule. Defaults to an empty
            string.

        Returns:
            tuple[str, str]: A tuple containing two strings:
                1. The parsed rule (rule condition).
                2. The value to be applied if the rule condition is met.

        Raises:
            ValueError: If the input 'rule' is not of type str, or if the rule
            does not have exactly one '->' token.
        """
        if not isinstance(rule, str):
            logger.exception(f"'rule' must be of type str and not {type(rule)}: {rule}")
            raise ValueError(f"'rule' must be of type str and not {type(rule)}: {rule}")

        parsed_rule = self._preprocess_values(df, rule, col)

        parsed_rule = parsed_rule.split("->")

        if len(parsed_rule) != 2:
            logger.exception("Each rule must only have one '->' token: ", rule)
            raise ValueError("Each rule must only have one '->' token: ", rule)

        # rule, value
        return parsed_rule[0], parsed_rule[1].strip()

    def _parse_rule_value(self, df: pd.DataFrame, rule_value_column: str) -> pd.Series:
        """
        Parse and apply default value rules from the YAML data for a given
        column.

        Args:
            df (pd.DataFrame): A pandas DataFrame containing the data.

            rule_value_column (str): The column for which the default value
            rule should be applied.

        Returns:
            pd.Series: The updated column with default value rules applied.
        """

        # 1. Extract raw_rule from _mapping
        raw_rules = self._mapping.mapping[rule_value_column].rule_value  # type: ignore

        if not isinstance(raw_rules, list):
            raw_rules = [raw_rules]

        processed_row = df[rule_value_column]  # .copy() # -> do not copy

        # Empty Series, will be used to update the original column
        update_col = pd.Series(np.nan, processed_row.index)
        for raw_rule in raw_rules:
            # 2. Parse the raw_rule
            rule, value = self._parse_rule(df, raw_rule, rule_value_column)  # type: ignore

            # 3. Run rule across all df
            def run_rule(row: pd.Series, rule: str, value: str):
                if self._parse_value(row, rule):  # Asses rule
                    return self._parse_value(row, value)  # Return value
                return np.nan

            update_wave = df.apply(
                run_rule,  # type: ignore
                args=(rule, value),
                axis=1,
            )

            # Update only rows that have no previous value -> replicate if elif
            # elif feature
            update_col = update_col.fillna(update_wave)

        processed_row.update(update_col)
        return processed_row

    # Aux

    def _preprocess_values(
        self, df: pd.DataFrame, rule: Any, col: str | None = None
    ) -> str:
        """
        Preprocess the given rule by replacing column names with the row format
        and applying specific replacements for special cases.

        Args:
            df (pd.DataFrame): A pandas DataFrame containing the data. rule
            (str): The rule to be preprocessed. col (str | None, optional): A
            specific column to be used for replacement, if any.

        Returns:
            str: The preprocessed rule with the appropriate column name and
            function replacements.
        """
        if not isinstance(rule, str):
            return rule

        def replace_variable(rule: str, variable: str, new_variable: str) -> str:
            return re.sub(
                r"\b{}\b".format(re.escape(str(variable))),
                f"{str(new_variable)}",
                str(rule),
            )

        def row_format(rule: str, variable: str) -> str:
            return re.sub(
                r"\b{}\b".format(re.escape(str(variable))),
                f"row['{str(variable)}']",
                str(rule),
            )

        # Format all df columns present to row[col] format
        for df_col in df.columns:
            rule = row_format(rule, df_col)

        # Replace and format row[] format to 'x' variable name
        rule = row_format(rule, "x")
        if col:
            rule = replace_variable(rule, "x", col)

        # Replace DATE() dummy function with wrapper pd.to_datetime() function
        rule = replace_variable(
            rule, MapperKeys.DATE_FUNCTION.value, "util_dates.safe_to_datetime"
        )

        return rule

    def _get_diff_values(self, row: pd.Series, old: str, new: str) -> str | float:
        """
        Get the difference between the old and new values in a given row, if
        any.

        Args:
            row (pd.Series): A pandas Series containing information about a row
            of data. old (str): The old value to compare. new (str): The new
            value to compare.

        Returns:
            str | float: The difference between the old and new values, if any,
                            otherwise a numpy NaN value.
        """
        return (
            f"{row[old]} -> {row[new]}"
            if (row[old] != row[new]) and not (pd.isna(row[old]) and pd.isna(row[new]))
            else np.nan
        )

    def _get_diff_col(self, row: pd.Series, get_col: str) -> str | float:
        """
        Get the col values if there are differences between 'old' and 'new'.

        Args:
            row (pd.Series): A pandas Series containing information about a row
            of data. get_col (str): column to retrieve

        Returns:
            str | float: The difference between the old and new values, if any,
                            otherwise a numpy NaN value.
        """
        old = row["old"]
        new = row["new"]

        if pd.isna(old) and pd.isna(new):
            diff = False
        elif isinstance(old, pd.Timestamp) and isinstance(new, date):
            diff = old.date() != new
        elif isinstance(old, date) and isinstance(new, pd.Timestamp):
            diff = old != new.date()
        else:
            diff = old != new

        return row[get_col] if diff else np.nan

    def _get_diff_values_comment(
        self, row: pd.Series, default_value_column: str, old: str, new: str
    ) -> str:
        """
        Get a formatted string with the difference between the old and new
        values, if any.

        Args:
            row (pd.Series): A pandas Series containing information about a row
            of data. default_value_column (str): The name of the default value
            column. old (str): The old value to compare. new (str): The new
            value to compare.

        Returns:
            str: A formatted string with the difference between the old and new
            values,
                if any, otherwise an empty string.
        """

        diff_values = self._get_diff_values(row, old, new)
        return (
            f"{default_value_column}({diff_values}) "
            if not pd.isna(diff_values)
            else ""
        )

    @staticmethod
    def _process_row_data(row: pd.Series) -> dict[str, str | list[str]]:
        """
        Process a row of data and create a dictionary containing column
        information.

        Args:
            row (pd.Series): A pandas Series containing information about a row
            of
                            column data.

        Returns:
            dict[str, str | list[str]]: A dictionary containing keys related to
                column information such as 'column', 'override',
                'default_value', and 'rule_value', and their respective
                values.
        """

        column_data = {
            "column": row[MapperKeysExcel.COL_OLD_COLUMN.value],
            "override": row[MapperKeysExcel.COL_OVERRIDE.value],
            "default_value": row[MapperKeysExcel.COL_DEFAULT_VALUE.value],
            "rule_value": row[MapperKeysExcel.COL_VALUE_RULE.value].split("\n")
            if not pd.isna(row[MapperKeysExcel.COL_VALUE_RULE.value])
            else np.nan,
        }

        # Transform len()==1 list into string representation
        for k, v in column_data.items():
            if isinstance(v, list) and len(v) == 1:
                column_data[k] = v[0]

        # Make sure to have an empty default value if creating a new column
        if column_data["column"] == MapperKeys.CREATE_COLUMN.value and pd.isna(
            column_data["default_value"]
        ):
            column_data["default_value"] = ""

        return {
            k: v
            for k, v in column_data.items()
            if not (isinstance(v, float) and pd.isna(v))
        }  # type: ignore

    @staticmethod
    def _df_columns_to_dict(df_columns: pd.DataFrame) -> dict:
        """
        Convert a DataFrame containing column information into a dictionary.

        The input DataFrame should have specific columns with old and new column
        names, override, value rule, and default value information.

        Args:
            df_columns (pd.DataFrame): A DataFrame containing column
            information.

        Returns:
            dict: A dictionary containing new column names as keys and either
            old
                column names or a processed row data dictionary as values.
        """

        columns_data = {}
        nan_columns = [
            MapperKeysExcel.COL_OVERRIDE.value,
            MapperKeysExcel.COL_VALUE_RULE.value,
            MapperKeysExcel.COL_DEFAULT_VALUE.value,
        ]

        for _, row in df_columns.iterrows():
            new_column = row[MapperKeysExcel.COL_NEW_COLUMN.value]

            if all(pd.isna(row[col]) for col in nan_columns):
                # Create new column
                if (
                    row[MapperKeysExcel.COL_OLD_COLUMN.value]
                    == MapperKeys.CREATE_COLUMN.value
                ):
                    columns_data[new_column] = {
                        "column": MapperKeys.CREATE_COLUMN.value,
                        "default_value": "",
                    }
                # Simple entry
                else:
                    columns_data[new_column] = row[MapperKeysExcel.COL_OLD_COLUMN.value]
            else:
                # Complex entry
                columns_data[new_column] = Mapper._process_row_data(row)

        return columns_data
