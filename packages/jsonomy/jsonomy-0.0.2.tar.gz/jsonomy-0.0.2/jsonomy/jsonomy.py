
from typing import Any, Dict, List, Optional, Union
from jsonomy.functions import convert_camel_to_snake, is_date, validate_and_parse_json
import pprint

class Jsonomy:
    """
    Designed to format data from a JSON response in either a dictionary or string format & make it more pythonic.
    It includes methods to convert camel case to snake case,
    identify and parse strings that represent dates,
    and recursively process data structures.
    """
    data: Optional[Dict] = None

    def __init__(self, data: Any):
        """
        Initialises the JSONFormatter with the data to be processed.

        Args:
            data (Any): The json data to be processed.

        """
        self.load(data)

    def load(self, data: Any):
        """
        Re-initialises the JSONFormatter with the data to be processed.

        Args:
            data (Any): The json data to be processed.

        """
        self.data = validate_and_parse_json(data)

    def _process_dict(self, val: Dict) -> Dict:
        """
        Processes a dictionary, converting keys to snake case and recursively processing the values.

        Args:
            val (Dict): The dictionary to be processed.

        Returns:
            Dict: The processed dictionary.
        """
        if isinstance(val, dict):
            return {convert_camel_to_snake(k): self._process_value(v) for k, v in val.items()}
        return val

    def process_list(self, val: List) -> List:
        """
        Processes a list, recursively processing its elements.

        Args:
            val (List): The list to be processed.

        Returns:
            List: The processed list.
        """
        if isinstance(val, list):
            return [self._process_value(v) for v in val]
        return val

    def _process_value(self, val: Any) -> Any:
        """
        Processes a value. If the value is a string, it is checked to see if it is a date.
        If the value is a dictionary or a list, it is processed recursively.

        Args:
            val (Any): The value to be processed.

        Returns:
            Any: The processed value.
        """
        if isinstance(val, str):
            date_found, parsed = is_date(val)
            if date_found:
                return parsed
        if isinstance(val, dict):
            return self._process_dict(val)
        if isinstance(val, list):
            return self.process_list(val)
        return val

    def format(self) -> Any:
        """
        Starts the processing of the data.

        Returns:
            Any: The processed data.
        """
        return self._process_value(self.data)

    def pprint(self, as_str=False) -> Union[str, None]:
        """
        Pretty prints the processed data or returns it as a string.

        Args:
            as_str (bool): If True, returns the pretty printed data as a string.

        """
        if as_str:
            return pprint.pformat(self.format())
        else:
            pprint.pprint(self.format())
