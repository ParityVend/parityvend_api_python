import pytest
from parityvend_api.objects import Country
from parityvend_api import COUNTRIES, get_country_by_code


def test_init():
    assert [{key == country.code for key, country in COUNTRIES.items()}]


def test_meta():
    us = Country("US")

    assert (
        us
        == Country("us")
        == Country(b"US")
        == get_country_by_code("US")
        == get_country_by_code("us")
        == get_country_by_code(b"US")
        == COUNTRIES["US"]
    )

    assert us != Country("CA")

    with pytest.raises(ValueError):
        Country("11")

    assert us.code == "US"
    assert us.name == "United States of America"
    assert us.emoji_flag == "🇺🇸"
    assert us.currency_code == "USD"
    assert us.currency_symbol == "$"
    assert us.currency_localized == "USD$"
    assert repr(us) == "Country('US')"
    assert str(us) == "Country United States of America (US)"

    assert sorted([Country("US"), Country("UA"), Country("AU")]) == [
        Country("AU"),
        Country("UA"),
        Country("US"),
    ]


def test_eq():
    assert Country("US") == get_country_by_code("US") == get_country_by_code(b"US")

    assert [
        {
            country.code == get_country_by_code(country.code)
            for key, country in COUNTRIES.items()
        }
    ]


def test_getattr_fail():
    country = Country("US")
    with pytest.raises(AttributeError):
        country.blah
