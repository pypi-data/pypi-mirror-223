from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta


def get_timestamp(format="%Y-%m-%d_%H-%M-%S"):
    """
    Get the current timestamp and return it as a string formatted according to
    the input format string.

    Args:
        format (str, optional): A string representing the desired timestamp
        format. Defaults to "%Y-%m-%d_%H-%M-%S".

    Returns:
        str: The current timestamp as a string in the specified format.

    Examples:
        >>> get_timestamp("%Y-%m-%d_%H-%M")
        '2023-07-13_15-30'
    """
    return datetime.now().strftime(format)


def safe_to_datetime(date_string: str) -> pd.Timestamp:
    """
    This function safely converts a date string to a pandas.Timestamp object. If
    the date is outside the pandas.Timestamp bounds, it returns the maximum
    datetime representable by Pandas.

    Args:
        date_string (str): The date string to convert.

    Returns:
        pd.Timestamp: A pandas.Timestamp if the date is within bounds, max
            representable datetime otherwise.
    """
    try:
        return pd.to_datetime(date_string)
    except Exception as _:
        return pd.Timestamp.max
