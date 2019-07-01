import pytest
from jsonschema import ValidationError
from mock import MagicMock

from connexion.json_schema import (Draft4RequestValidator,
                                   Draft4ResponseValidator)


def test_support_nullable_properties():
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "x-nullable": True}},
    }
    try:
        Draft4RequestValidator(schema).validate({"foo": None})
    except ValidationError:
        pytest.fail("Shouldn't raise ValidationError")


def test_support_nullable_properties_raises_validation_error():
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "x-nullable": False}},
    }

    with pytest.raises(ValidationError):
        Draft4RequestValidator(schema).validate({"foo": None})


def test_support_nullable_properties_not_iterable():
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "x-nullable": True}},
    }
    with pytest.raises(ValidationError):
        Draft4RequestValidator(schema).validate(12345)


def test_nullable_enum():
    schema = {
        "enum": ["foo", 7],
        "nullable": True
    }
    try:
        Draft4RequestValidator(schema).validate(None)
    except ValidationError:
        pytest.fail("Shouldn't raise ValidationError")


def test_nullable_enum_error():
    schema = {
        "enum": ["foo", 7]
    }
    with pytest.raises(ValidationError):
        Draft4RequestValidator(schema).validate(None)


def test_writeonly_value():
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "writeOnly": True}},
    }
    try:
        Draft4RequestValidator(schema).validate({"foo": "bar"})
    except ValidationError:
        pytest.fail("Shouldn't raise ValidationError")


def test_writeonly_value_error():
    schema = {
        "type": "object",
        "properties": {"foo": {"type": "string", "writeOnly": True}},
    }
    with pytest.raises(ValidationError):
        Draft4ResponseValidator(schema).validate({"foo": "bar"})


def test_writeonly_required():
    schema = {
        "type": "object",
        "required": ["foo"],
        "properties": {"foo": {"type": "string", "writeOnly": True}},
    }
    try:
        Draft4RequestValidator(schema).validate({"foo": "bar"})
    except ValidationError:
        pytest.fail("Shouldn't raise ValidationError")


def test_writeonly_required_error():
    schema = {
        "type": "object",
        "required": ["foo"],
        "properties": {"foo": {"type": "string", "writeOnly": True}},
    }
    with pytest.raises(ValidationError):
        Draft4RequestValidator(schema).validate({"bar": "baz"})
