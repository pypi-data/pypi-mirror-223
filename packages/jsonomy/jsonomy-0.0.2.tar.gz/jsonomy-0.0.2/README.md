Copy code
# Jsonomy

Jsonomy is a basic JSON parser that converts API's JSON output to be more Pythonic. It includes functionalities like converting camel case to snake case, and timestamps to datetime objects.

## Features

- Convert JSON keys from camel case to snake case.
- Identify strings that represent dates and convert them to datetime objects.
- Recursively process JSON data structures.

## Installation

To install Jsonomy, you can use pip:

```bash
pip install jsonomy
```

## Usage

```python  
from jsonomy import Jsonomy

data = {
    "createdAt": "2022-07-01T10:00:00Z",
    "someNestedData": {
        "moreDetails": "data"
    },
    "aList": ["item1", "item2"]
}

# load data into Jsonomy and process
formatter = Jsonomy(data)
processed = formatter.format()

# print the processed data 
formatter.pprint()

# reload new data
formatter.load(data)

#load and format
Jsonomy(data).format()

#load and pretty print to a string
pretty_json = Jsonomy(data).pprint(as_str=True)

```


## License
This project is licensed under the terms of the MIT license.

## Contact
For questions, feel free to reach out to Lewis Morris at lewis.morris@gmail.com
