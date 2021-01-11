from decimal import Decimal

from boto3.dynamodb.types import Binary, TypeDeserializer, TypeSerializer

_deserializer = TypeDeserializer()
_serializer = TypeSerializer()
_dynamo_keys = {'S', 'NS', 'SS', 'BS', 'B', 'N', 'L', 'M', 'BOOL', 'NULL'}


def _decimal_to_number(val):
    """Converts decimal to float or integer"""
    float_val = float(val)
    if str(float_val) == str(val):
        return float_val
    else:
        return int(float_val)


def _load_incompatible_types(obj):
    """Walks dicts and lists and ensures JSON compatible types"""
    if isinstance(obj, list):
        return [
            _load_incompatible_types(obj[i])
            for i in range(len(obj))
        ]
    elif isinstance(obj, dict):
        return {
            k: _load_incompatible_types(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, set):
        return [ _load_incompatible_types(k) for k in obj ]
    elif isinstance(obj, Decimal):
        return _decimal_to_number(obj)
    elif isinstance(obj, Binary):
        return obj.value.decode('utf-8')
    else:
        return obj


def _load(data, to_json):
    if len(data.keys()) == 1 and set(data.keys()) & _dynamo_keys:
        return next(
            _load_incompatible_types(_deserializer.deserialize(data))
            if to_json else _deserializer.deserialize(data)
            for k in data.keys()
        )
    else:
        return { 
            k: _load_incompatible_types(_deserializer.deserialize(v))
            if to_json else _deserializer.deserialize(v)
            for k, v in data.items()
        }


def loads(data, to_json=True):
    """Returns normal values from dynamodb values"""
    if isinstance(data, dict):
        return _load(data, to_json)
    elif isinstance(data, list):
        return [ _load(d, to_json) for d in data ]
    else:
        raise TypeError('Only dict or list types are supported')


def _dump_incompatible_types(obj):
    """Walks dicts and lists and replaces incompatible types"""
    if isinstance(obj, list):
        return [
            _dump_incompatible_types(obj[i])
            for i in range(len(obj))
        ]
    elif isinstance(obj, dict):
        return {
            k: _dump_incompatible_types(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, set):
        return { _dump_incompatible_types(k) for k in obj }
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


def _dump(data):
    """Returns dynamodb dict from dict"""
    if isinstance(data, dict):
        return {
            k: _serializer.serialize(_dump_incompatible_types(v))
            for k,v in data.items()
        }
    else:
        return _serializer.serialize(_dump_incompatible_types(data))


def dumps(data):
    """Returns dynamodb values from normal values"""
    if isinstance(data, list):
        return [ _dump(d) for d in data ]
    else:
        return _dump(data)