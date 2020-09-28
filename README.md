# dynamodb-tools

This package provides various utility functions for AWS DynamoDB:

- `loads` - loads DynamoDB formatted data into Python objects
- `dumps` - Outputs Python objects into DynamoDB formatted data

## Installation

```
pip install dynamodb-tools
```

## Usage

### Loading DynamoDB Data into Python Objects

By default, the `loads` function ensures the resulting Python object is JSON compatible:

```python
from dynamodb_tools import loads

dynamo_json = {
  "my_dict": {"M": {"my_date": {"S": "2017-04-22T14:41:35.780000"}}}, 
  "MyBool": {"BOOL": False}, "MyNone": {"NULL": True}, 
  "MyNestedDict": {
    "M": {"my_other_nested": {
        "M": {"myUUID": {"S": "2f4ad21e098f49b18e22ad209779048b"}, 
              "surname": {"S": "Lennon"}, "name": {"S": "John"}, 
              "mySet": {"L": [{"N": "1"}, {"N": "3"}, {"N": "4"}, {"N": "5"}, {"N": "6"}]}, 
              "floaty": {"N": "29.4"}, "time": {"N": "1492872095.78"}, 
              "myList": {"L": [{"N": "1"}, {"N": "3"}, {"N": "4"}, {"N": "5"}, {"N": "6"}, {"S": "This Is Sparta!"}]}, 
              "MyOtherNone": {"NULL": True}}
              }
        }
    }, 
  "myDecimal": {"N": "19.2"}, "num": {"N": "4"}, 
  "MyString": {"S": "a"}, 
  "myLong": {"N": "1938475658493"}, 
  "MyZero": {"N": "0"}
}

data = loads(dynamo_json)
assert data == {
  'my_dict': {'my_date': '2017-04-22T14:41:35.780000'},
  'MyBool': False,
  'MyNone': None,
  'MyNestedDict': {'my_other_nested': {'myUUID': '2f4ad21e098f49b18e22ad209779048b',
    'surname': 'Lennon',
    'name': 'John',
    'mySet': [1, 3, 4, 5, 6],
    'floaty': 29.4,
    'time': 1492872095.78,
    'myList': [1, 3, 4, 5, 6, 'This Is Sparta!'],
    'MyOtherNone': None}},
  'myDecimal': 19.2,
  'num': 4,
  'MyString': 'a',
  'myLong': 1938475658493,
  'MyZero': 0
}
assert json.dumps(data)
```

The `loads` function is performant and is approximately 3-4x faster than [another popular library](https://github.com/Alonreznik/dynamodb-json).

```python
items = []
for i in range(10000):
  items.append(dynamo_json)

%timeit loads(items)
554 ms ± 9.34 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# See https://github.com/Alonreznik/dynamodb-json
from dynamodb_utils import json_util
%timeit json_util.loads(items)
1.27 s ± 14.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

You can disable JSON compatibility by passing the `to_json=False` parameter to the `loads` function, which will execute approximately 25% faster.   

Note this will return `Decimal` types for numbers and `boto3.dynamodb.types.Binary` types for binary attributes:

```python
data = loads(dynamo_json, to_json=False)

assert data == {'my_dict': {'my_date': '2017-04-22T14:41:35.780000'},
  'MyBool': False,
  'MyNone': None,
  'MyNestedDict': {'my_other_nested': {'myUUID': '2f4ad21e098f49b18e22ad209779048b',
    'surname': 'Lennon',
    'name': 'John',
    'mySet': [Decimal('1'),
    Decimal('3'),
    Decimal('4'),
    Decimal('5'),
    Decimal('6')],
    'floaty': Decimal('29.4'),
    'time': Decimal('1492872095.78'),
    'myList': [Decimal('1'),
    Decimal('3'),
    Decimal('4'),
    Decimal('5'),
    Decimal('6'),
    'This Is Sparta!'],
    'MyOtherNone': None}},
  'myDecimal': Decimal('19.2'),
  'num': Decimal('4'),
  'MyString': 'a',
  'myLong': Decimal('1938475658493'),
  'MyZero': Decimal('0')
}
```

### Dumping Python Objects into DynamoDB Data

The `dumps` function creates DynamoDB formatted data from Python objects:

```python
from dynamodb_tools import dumps

data = {
  'my_dict': {'my_date': '2017-04-22T14:41:35.780000'},
  'MyBool': False,
  'MyNone': None,
  'MyNestedDict': {'my_other_nested': {'myUUID': '2f4ad21e098f49b18e22ad209779048b',
    'surname': 'Lennon',
    'name': 'John',
    'mySet': [1, 3, 4, 5, 6],
    'floaty': 29.4,
    'time': 1492872095.78,
    'myList': [1, 3, 4, 5, 6, 'This Is Sparta!'],
    'MyOtherNone': None}},
  'myDecimal': 19.2,
  'num': 4,
  'MyString': 'a',
  'myLong': 1938475658493,
  'MyZero': 0
}

dynamodb_json = dumps(data)

assert dynamodb_json == {
  'my_dict': {'M': {'my_date': {'S': '2017-04-22T14:41:35.780000'}}},
  'MyBool': {'BOOL': False},
  'MyNone': {'NULL': True},
  'MyNestedDict': {'M': {'my_other_nested': {'M': {'myUUID': {'S': '2f4ad21e098f49b18e22ad209779048b'},
      'surname': {'S': 'Lennon'},
      'name': {'S': 'John'},
      'mySet': {'L': [{'N': '1'},
        {'N': '3'},
        {'N': '4'},
        {'N': '5'},
        {'N': '6'}]},
      'floaty': {'N': '29.4'},
      'time': {'N': '1492872095.78'},
      'myList': {'L': [{'N': '1'},
        {'N': '3'},
        {'N': '4'},
        {'N': '5'},
        {'N': '6'},
        {'S': 'This Is Sparta!'}]},
      'MyOtherNone': {'NULL': True}}}}},
  'myDecimal': {'N': '19.2'},
  'num': {'N': '4'},
  'MyString': {'S': 'a'},
  'myLong': {'N': '1938475658493'},
  'MyZero': {'N': '0'}}
```
