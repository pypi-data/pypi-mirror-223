import datetime
import json
import re
from typing import Union, Any, Dict

from dateutil.parser import parse

ERROR_TEXT = "Json not in expected format"


def validate_and_parse_json(data: Any) -> Dict:
    """
    Validates or parses json data and returns a dictionary.

    Args:
        data (Any): The data to be validated or parsed.

    Returns:
        Dict: The validated or parsed data.

    Raises:
        ValueError: If the data is None or not in the expected format.

    """

    # the allowed types
    allowed_types = (list, dict)

    # if the data is None, raise an error
    if isinstance(data, str):
        try:
            out = json.loads(data)
            if isinstance(out, allowed_types):
                return out
            raise ValueError(ERROR_TEXT)
        except json.JSONDecodeError:
            # if the data is not in json format, raise an error
            raise ValueError(ERROR_TEXT)
    elif isinstance(data, allowed_types):
        # if the data is already in the allowed format, return it
        return data
    else:
        # if the data is not in the allowed format, raise an error
        raise ValueError(ERROR_TEXT)


def convert_camel_to_snake(name: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        name (str): The string to be converted.

    Returns:
        str: The converted string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def is_date(string: Union[str, int]) -> tuple[bool, datetime] | tuple[bool, str]:
    """
    Checks if a string can be parsed into a date.

    Args:
        string (str): The string to be checked.

    Returns:
        bool: True if the string can be parsed into a date, False otherwise.
        str: The parsed date if the string is a date, otherwise the original string.
    """
    if isinstance(string, str) and len(string) > 6 and any(x in string for x in ["-", ":", "/"]):
        try:
            return True, parse(string)
        except ValueError:
            pass

    return False, string
