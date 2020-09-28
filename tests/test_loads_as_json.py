import json

import pytest

from dynamodb_tools import loads


def test_loads_integer():
    data = {'N': '1'}
    result = loads(data)
    assert isinstance(result, int)
    assert result == 1
    assert json.dumps(result)


def test_loads_float():
    data = {'N': '1.0'}
    result = loads(data)
    assert isinstance(result, float)
    assert result == 1.0
    assert json.dumps(result)


def test_loads_string():
    data = {'S': '1.0'}
    result = loads(data)
    assert result == '1.0'
    assert json.dumps(result)


def test_loads_binary():
    data = {'B': b'1.0'}
    result = loads(data)
    assert isinstance(result, str)
    assert result == '1.0'
    assert json.dumps(result)


def test_loads_map():
    data = {'M': {'foo': {'N': '1'}}}
    result = loads(data)
    assert result == {'foo': 1}
    assert json.dumps(result)


def test_loads_list():
    data = {'L': [{'N': '1'}, {'N': '2'}]}
    result = loads(data)
    assert result == [1, 2]
    assert json.dumps(result)


def test_loads_string_set():
    data = {'SS': {'1','2','3'}}
    result = loads(data)
    assert isinstance(result, list)
    assert set(result) == {'1', '2', '3'}
    assert json.dumps(result)


def test_loads_number_set():
    data = {'NS': {'1.1','2.2','3.3'}}
    result = loads(data)
    assert isinstance(result, list)
    assert set(result) == {1.1, 2.2, 3.3}
    assert json.dumps(result)


def test_loads_binary_set():
    data = {'BS': {b'1.1',b'2.2',b'3.3'}}
    result = loads(data)
    assert isinstance(result, list)
    assert set(result) == {'1.1', '2.2', '3.3'}
    assert json.dumps(result)


def test_loads_null():
    data = {'NULL': True}
    result = loads(data)
    assert result is None


def test_loads_invalid_type():
    with pytest.raises(TypeError) as e:
        result = loads(10)
    assert str(e.value) == 'Only dict or list types are supported'