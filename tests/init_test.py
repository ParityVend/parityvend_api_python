import pytest
from parityvend_api import AsyncParityVendAPI, ParityVendAPI
from tests.variables import secret_key, invalid_secret_key


def test_async_handler_empty():
    with pytest.raises(TypeError):
        AsyncParityVendAPI()


def test_handler_empty():
    with pytest.raises(TypeError):
        ParityVendAPI()


def test_handler():
    assert isinstance(ParityVendAPI(secret_key), ParityVendAPI)


def test_async_handler():
    assert isinstance(AsyncParityVendAPI(secret_key), ParityVendAPI)


def test_handler_invalid():
    assert isinstance(ParityVendAPI(invalid_secret_key), ParityVendAPI)


def test_async_handler_invalid():
    assert isinstance(AsyncParityVendAPI(invalid_secret_key), ParityVendAPI)
