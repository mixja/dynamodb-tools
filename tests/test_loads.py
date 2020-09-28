from decimal import Decimal

from boto3.dynamodb.types import Binary
from dynamodb_tools import loads


fn = lambda v: loads(v, to_json=False)

def test_loads_integer():
    data = {'N': '1'}
    result = fn(data)
    assert isinstance(result, Decimal)
    assert result == Decimal('1')


def test_loads_float():
    data = {'N': '1.0'}
    result = fn(data)
    assert isinstance(result, Decimal)
    assert result == Decimal('1.0')


def test_loads_string():
    data = {'S': '1.0'}
    result = fn(data)
    assert result == '1.0'


def test_loads_binary():
    data = {'B': b'1.0'}
    result = fn(data)
    assert isinstance(result, Binary)
    assert result == b'1.0'


def test_loads_map():
    data = {'M': {'foo': {'N': '1'}}}
    result = fn(data)
    assert result == {'foo': Decimal('1')}


def test_loads_list():
    data = {'L': [{'N': '1'}, {'N': '2'}]}
    result = fn(data)
    assert result == [Decimal('1'), Decimal('2')]


def test_loads_string_set():
    data = {'SS': {'1','2','3'}}
    result = fn(data)
    assert isinstance(result, set)
    assert set(result) == {'1', '2', '3'}


def test_loads_number_set():
    data = {'NS': {'1.1','2.2','3.3'}}
    result = fn(data)
    assert isinstance(result, set)
    assert set(result) == {Decimal('1.1'), Decimal('2.2'), Decimal('3.3')}


def test_loads_binary_set():
    data = {'BS': {b'1.1',b'2.2',b'3.3'}}
    result = fn(data)
    assert isinstance(result, set)
    assert set(result) == {b'1.1', b'2.2', b'3.3'}
