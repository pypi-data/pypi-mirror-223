import datetime
import pytest
from dateutil.tz import tzutc

from jsonomy import Jsonomy
from jsonomy.functions import is_date, convert_camel_to_snake, validate_and_parse_json
from dateutil.tz import tzoffset

PLACE_NAME = 'New York'

class TestIsDate:
    #  Tests that a string with a valid date format is correctly parsed
    def test_valid_date_format(self):
        assert is_date('2022-01-01') == (True, datetime.datetime(2022, 1, 1, 0, 0))

    #  Tests that a string with a valid date and time format is correctly parsed
    def test_valid_date_time_format(self):
        assert is_date('2022-01-01 12:30:45') == (True, datetime.datetime(2022, 1, 1, 12, 30, 45))

    #  Tests that a string with a valid date, time and timezone format is correctly parsed
    def test_valid_date_time_zone_format(self):
        assert is_date('2022-01-01 12:30:45+00:00') == (
        True, datetime.datetime(2022, 1, 1, 12, 30, 45, tzinfo=datetime.timezone.utc))

    #  Tests that an empty string is not parsed as a date
    def test_empty_string(self):
        assert is_date('') == (False, '')

    #  Tests that a string with an invalid date format is not parsed as a date
    def test_invalid_date_format(self):
        assert is_date('2022-13-01') == (False, '2022-13-01')

    #  Tests that is_date function do not convert strings that are not dates
    def test_does_not_convert_21_or_3(self):
        assert is_date('21') == (False, '21')
        assert is_date(3) == (False, 3)
        assert is_date("MAY1") == (False, "MAY1")

    # tests that the function handles timezones.
    def test_handles_timezone_strings(self):
        assert is_date('2022-01-01T00:00:00.000Z') == (True,
                                                       datetime.datetime(2022, 1, 1, 0, 0, tzinfo=tzutc()))
        assert is_date('2022-01-01T00:00:00.000+01:00') == (True,
                                                            datetime.datetime(2022, 1, 1, 0, 0,
                                                                              tzinfo=tzoffset(None, 3600)))


class TestConvertCamelToSnake:
    #  Tests that the function converts a simple camel case string to snake case
    def test_simple_conversion(self):
        assert convert_camel_to_snake('simpleCamelCase') == 'simple_camel_case'

    #  Tests that the function converts a camel case string with numbers to snake case
    def test_conversion_with_numbers(self):
        assert convert_camel_to_snake('camelCaseWith123Numbers') == 'camel_case_with123_numbers'

    #  Tests that the function converts a camel case string with consecutive capital letters to snake case
    def test_conversion_with_consecutive_capitals(self):
        assert convert_camel_to_snake('camelCaseWithConsecutiveCAPITALS') == 'camel_case_with_consecutive_capitals'

    #  Tests that the function converts a camel case string with first letter capitalized to snake case
    def test_conversion_with_first_letter_capitalized(self):
        assert convert_camel_to_snake(
            'CamelCaseWithFirstLetterCapitalized') == 'camel_case_with_first_letter_capitalized'

    #  Tests that the function converts an empty string to an empty string
    def test_empty_string_conversion(self):
        assert convert_camel_to_snake('') == ''


class TestValidateOrParse:
    #  Tests that passing a valid JSON string returns a dictionary
    def test_valid_json_string_returns_dict(self):
        data = '{"name": "John", "age": 30, "city": "New York"}'
        expected_output = {'name': 'John', 'age': 30, 'city': PLACE_NAME}
        assert validate_and_parse_json(data) == expected_output

    #  Tests that passing a valid dictionary returns the same dictionary
    def test_valid_dict_returns_same_dict(self):
        data = {'name': 'John', 'age': 30, 'city': PLACE_NAME}
        expected_output = {'name': 'John', 'age': 30, 'city': PLACE_NAME}
        assert validate_and_parse_json(data) == expected_output

    #  Tests that passing None raises a ValueError
    def test_none_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_and_parse_json(None)

    #  Tests that passing an empty string raises a ValueError
    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_and_parse_json('')

    #  Tests that passing a non-JSON string raises a ValueError
    def test_non_json_string_raises_value_error(self):
        with pytest.raises(ValueError):
            validate_and_parse_json('this is not a json string')

    #  Tests that passing a JSON string with extra whitespace returns a dictionary
    def test_json_string_with_extra_whitespace_returns_dict(self):
        data = '  {  "name"  :  "John"  ,  "age"  :  30  ,  "city"  :  "New York"  }  '
        expected_output = {'name': 'John', 'age': 30, 'city': PLACE_NAME}
        assert validate_and_parse_json(data) == expected_output


class TestJsonomy:
    #  Tests that the class can be initialized with valid JSON data
    def test_valid_json_data(self):
        data = '{"name": "John", "age": 30}'
        jsonomy = Jsonomy(data)
        assert jsonomy.data == {"name": "John", "age": 30}

    #  Tests that the 'format' method returns the expected processed data
    def test_format_method(self):
        data = '{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}'
        expected = {"first_name": "John", "last_name": "Doe", "age": 30,
                    "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the 'pprint' method prints the processed data without errors
    def test_pprint_method(self):
        data = '{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}'
        jsonomy = Jsonomy(data)
        try:
            jsonomy.pprint()
        except:
            pytest.fail("pprint raised an exception")

    #  Tests that the class raises a ValueError when initialized with invalid JSON data
    def test_invalid_json_data(self):
        data = '{"name": "John", "age": 30'  # missing closing bracket
        with pytest.raises(ValueError):
            Jsonomy(data)

    #  Tests that the class raises error when passed none
    def test_none_data(self):
        with pytest.raises(ValueError):
            Jsonomy(None)

    #  Tests that the class raises and error when the data is not json
    def test_incorrect_data(self):

        with pytest.raises(ValueError):
            Jsonomy(73)
        with pytest.raises(ValueError):
            Jsonomy("73")

    #  Tests that the class returns the original string when processing a string that is not a date
    def test_non_date_string_data(self):
        data = '{"name": "John", "age": "30"}'
        expected = {"name": "John", "age": "30"}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class returns the original string when processing a string that is a date but cannot be parsed
    def test_parse_date(self):
        data = '{"name": "John", "age": "1990-01-01T00:00:00Z"}'
        expected = {"name": "John", "age": datetime.datetime(1990, 1, 1, 0, 0, tzinfo=tzutc())}
        assert Jsonomy(data).format() == expected

    #  Tests that the class correctly processes nested dictionaries
    def test_nested_dict_processing(self):
        data = '{"person": {"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}}'
        expected = {"person": {"first_name": "John", "last_name": "Doe", "age": 30,
                               "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)}}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class correctly processes nested lists
    def test_nested_list_processing(self):
        data = '[{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}, {"firstName": "Jane", "lastName": "Doe", "age": 25, "dateOfBirth": "1995-01-01"}]'
        expected = [
            {"first_name": "John", "last_name": "Doe", "age": 30, "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)},
            {"first_name": "Jane", "last_name": "Doe", "age": 25, "date_of_birth": datetime.datetime(1995, 1, 1, 0, 0)}]
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class correctly processes a mix of nested dictionaries and lists with string dates
    def test_mixed_nested_processing(self):
        data = '{"people": [{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}, {"firstName": "Jane", "lastName": "Doe", "age": 25, "dateOfBirth": "1995-01-01"}], "company": {"name": "ACME", "foundedDate": "1980-01-01"}}'
        expected = {"people": [
            {"first_name": "John", "last_name": "Doe", "age": 30, "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)},
            {"first_name": "Jane", "last_name": "Doe", "age": 25,
             "date_of_birth": datetime.datetime(1995, 1, 1, 0, 0)}],
                    "company": {"name": "ACME", "founded_date": datetime.datetime(1980, 1, 1, 0, 0)}}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected



    def test_dict_valid_json_data(self):
        data = {"name": "John", "age": 30}
        jsonomy = Jsonomy(data)
        assert jsonomy.data == {"name": "John", "age": 30}

    #  Tests that the 'format' method returns the expected processed data
    def test_dict_format_method(self):
        data = {"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}
        expected = {"first_name": "John", "last_name": "Doe", "age": 30,
                    "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the 'pprint' method prints the processed data without errors
    def test_dict_pprint_method(self):
        data = {"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}
        jsonomy = Jsonomy(data)
        try:
            jsonomy.pprint()
        except:
            pytest.fail("pprint raised an exception")


    #  Tests that the class returns the original string when processing a string that is not a date
    def test_dict_non_date_string_data(self):
        data = {"name": "John", "age": "30"}
        expected = {"name": "John", "age": "30"}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class returns the original string when processing a string that is a date but cannot be parsed
    def test_dict_parse_date(self):
        data = {"name": "John", "age": "1990-01-01T00:00:00Z"}
        expected = {"name": "John", "age": datetime.datetime(1990, 1, 1, 0, 0, tzinfo=tzutc())}
        assert Jsonomy(data).format() == expected

    #  Tests that the class correctly processes nested dictionaries
    def test_dict_nested_dict_processing(self):
        data = {"person": {"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}}
        expected = {"person": {"first_name": "John", "last_name": "Doe", "age": 30,
                               "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)}}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class correctly processes nested lists
    def test_dict_nested_list_processing(self):
        data = [{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}, {"firstName": "Jane", "lastName": "Doe", "age": 25, "dateOfBirth": "1995-01-01"}]
        expected = [
            {"first_name": "John", "last_name": "Doe", "age": 30, "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)},
            {"first_name": "Jane", "last_name": "Doe", "age": 25, "date_of_birth": datetime.datetime(1995, 1, 1, 0, 0)}]
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected

    #  Tests that the class correctly processes a mix of nested dictionaries and lists with string dates
    def test_dict_mixed_nested_processing(self):
        data = {"people": [{"firstName": "John", "lastName": "Doe", "age": 30, "dateOfBirth": "1990-01-01"}, {"firstName": "Jane", "lastName": "Doe", "age": 25, "dateOfBirth": "1995-01-01"}], "company": {"name": "ACME", "foundedDate": "1980-01-01"}}
        expected = {"people": [
            {"first_name": "John", "last_name": "Doe", "age": 30, "date_of_birth": datetime.datetime(1990, 1, 1, 0, 0)},
            {"first_name": "Jane", "last_name": "Doe", "age": 25,
             "date_of_birth": datetime.datetime(1995, 1, 1, 0, 0)}],
                    "company": {"name": "ACME", "founded_date": datetime.datetime(1980, 1, 1, 0, 0)}}
        jsonomy = Jsonomy(data)
        assert jsonomy.format() == expected
