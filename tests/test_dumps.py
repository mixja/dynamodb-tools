from dynamodb_tools import dumps


def test_dumps_integer():
    data = 1
    result = dumps(data)
    assert result == {'N': '1'}


def test_dumps_float():
    data = 1.0
    result = dumps(data)
    assert result == {'N': '1.0'}


def test_dumps_string():
    data = '1.0'
    result = dumps(data)
    assert result == {'S': '1.0'}


def test_dumps_binary():
    data = b'1.0'
    result = dumps(data)
    assert result == {'B': b'1.0'}


def test_dumps_map():
    data = {'foo': {'bar': 1} }
    result = dumps(data)
    assert result == {'foo': {'M': {'bar': {'N': '1'}}}}


def test_dumps_list():
    data = {'foo': [1, 2]}
    result = dumps(data)
    assert result == {'foo': {'L': [{'N': '1'}, {'N': '2'}]}}


def test_dumps_string_set():
    data = {'1', '2', '3'}
    result = dumps(data)
    assert set(result['SS']) == {'1','2','3'}


def test_dumps_number_set():
    data = {1.1, 2.2, 3.3}
    result = dumps(data)
    assert set(result['NS']) == {'1.1','2.2','3.3'}


def test_dumps_binary_set():
    data = {b'1.1',b'2.2',b'3.3'}
    result = dumps(data)
    assert set(result['BS']) == {b'1.1',b'2.2',b'3.3'}


def test_dumps_null():
    data = {'foo': None}
    result = dumps(data)
    assert result == {'foo': {'NULL': True}}