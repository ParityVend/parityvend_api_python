import pytest
from parityvend_api.objects import Response


def test_init():
    response = Response({"foo": "bar"})
    assert response.foo == "bar" == response["foo"]


def test_getattr_fail():
    response = Response({"foo": "bar"})
    with pytest.raises(KeyError):
        response.blah


def test_all():
    data = {"foo": "bar", "ham": "eggs"}
    response = Response(data)
    assert tuple(response.items()) == tuple(data.items())


def test_nested_init():
    response = Response({"foo": {"bar": "baz"}})
    assert response.foo == {"bar": "baz"} == response["foo"]


def test_nested_getattr_fail():
    response = Response({"foo": {"bar": "baz"}})
    with pytest.raises(KeyError):
        response.blah

    with pytest.raises(KeyError):
        response.foo.blah


def test_nested_all():
    data = {"foo": {"bar": "baz"}, "ham": "eggs"}
    response = Response(data)
    assert tuple(response.items()) == tuple(data.items())
