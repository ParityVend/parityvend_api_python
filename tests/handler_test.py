import json
from ipaddress import IPv4Address, IPv6Address

import pytest
import requests

from parityvend_api import ParityVendAPI
from parityvend_api.cache.default import DefaultCache
from parityvend_api.exceptions import ProcessingError, ConnectionError
from parityvend_api.objects import Country, Response, Discounts, Discount
from tests.variables import (
    google_ipv4,
    invalid_secret_key,
    ipv4_switzerland,
    ipv4_zimbabwe,
    ipv6_vpn_cn,
    ipv6_zimbabwe,
    secret_key,
    secret_key_free,
)


def test_init():
    parityvend = ParityVendAPI(secret_key)

    assert parityvend.private_key == secret_key
    assert isinstance(parityvend.cache, DefaultCache)

    assert parityvend.request_options == {
        "headers": {
            "User-Agent": "Python ParityVend API Client/1.0.0 (+https://www.ambeteco.com/ParityVend/docs/index.html)"
        }
    }

    assert parityvend.json_loads == json.loads
    assert isinstance(parityvend.session, requests.Session)


def test_get_country_from_ip_timeout():
    parityvend = ParityVendAPI(secret_key)

    with pytest.raises(ConnectionError):
        parityvend.get_country_from_ip(google_ipv4, cache=False, timeout=1 * 10**-8)


def test_get_country_from_ip():
    parityvend = ParityVendAPI(secret_key)
    parityvend_free = ParityVendAPI(secret_key_free)

    assert parityvend.get_country_from_ip(google_ipv4) == Country("XX")
    assert parityvend.get_country_from_ip(ipv6_vpn_cn) == Country("XX")
    assert parityvend.get_country_from_ip(ipv4_zimbabwe) == Country("ZW")
    assert parityvend.get_country_from_ip(ipv6_zimbabwe) == Country("ZW")

    assert parityvend.get_country_from_ip(IPv4Address(google_ipv4)) == Country("XX")
    assert parityvend.get_country_from_ip(IPv6Address(ipv6_vpn_cn)) == Country("XX")
    assert parityvend.get_country_from_ip(IPv4Address(ipv4_zimbabwe)) == Country("ZW")
    assert parityvend.get_country_from_ip(IPv6Address(ipv6_zimbabwe)) == Country("ZW")

    assert parityvend_free.get_country_from_ip(google_ipv4) == Country("US")
    assert parityvend_free.get_country_from_ip(ipv6_vpn_cn) == Country("CN")
    assert parityvend_free.get_country_from_ip(ipv4_zimbabwe) == Country("ZW")
    assert parityvend_free.get_country_from_ip(ipv6_zimbabwe) == Country("ZW")


def test_cache_quota():
    parityvend = ParityVendAPI(secret_key)

    initial_quota = parityvend.get_quota_info(cache=False)
    assert parityvend.get_country_from_ip(ipv4_zimbabwe, cache=False) == Country("ZW")
    new_quota = parityvend.get_quota_info(cache=False)

    assert new_quota["quota_used"] > initial_quota["quota_used"]
    assert new_quota["status"] == "ok"
    assert isinstance(new_quota["quota_limit"], int)
    assert isinstance(new_quota["quota_used"], int)
    assert isinstance(new_quota["quota_left"], int)


def test_get_discounts_info():
    parityvend = ParityVendAPI(secret_key)

    discounts_info = parityvend.get_discounts_info()
    discounts = discounts_info["discounts"]

    assert isinstance(discounts, Discounts)

    assert isinstance(discounts["AC"], Discount)
    assert discounts["AC"].country == Country("AC") == discounts["AC"]["country"]
    assert discounts["AC"].discount == 0.0 == discounts["AC"]["discount"]
    assert discounts["AC"].discount_str == "0.00%" == discounts["AC"]["discount_str"]
    assert discounts["AC"].coupon_code == "" == discounts["AC"]["coupon_code"]

    assert discounts["ZW"].country == Country("ZW") == discounts["ZW"]["country"]
    assert discounts["ZW"].discount == 0.7 == discounts["ZW"]["discount"]
    assert discounts["ZW"].discount_str == "70.00%" == discounts["ZW"]["discount_str"]
    assert (
        discounts["ZW"].coupon_code
        == "example_coupon"
        == discounts["ZW"]["coupon_code"]
    )

    assert discounts["SV"].country == Country("SV") == discounts["SV"]["country"]
    assert discounts["SV"].discount == 0.5 == discounts["SV"]["discount"]
    assert discounts["SV"].discount_str == "50.00%" == discounts["SV"]["discount_str"]
    assert (
        discounts["SV"].coupon_code
        == "example_coupon"
        == discounts["SV"]["coupon_code"]
    )

    assert discounts.get_discount_by_country("AC") == discounts["AC"]
    assert discounts.get_discount_by_country("ZW") == discounts["ZW"]
    assert discounts.get_discount_by_country("SV") == discounts["SV"]


def test_get_discount_from_ip():
    parityvend = ParityVendAPI(secret_key)
    response = parityvend.get_discount_from_ip(ipv4_zimbabwe)
    response_ipv6 = parityvend.get_discount_from_ip(ipv6_zimbabwe)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_discount_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = parityvend_free.get_discount_from_ip(ipv6_zimbabwe)

    assert response == response_free == response_ipv6 == response_free_ipv6

    assert response["status"] == "ok"
    assert response["discount"] == 0.7
    assert response["discount_str"] == "70.00%"
    assert response["coupon_code"] == "example_coupon"
    assert response["country"] == Country("ZW")

    assert response["currency"]["code"] == "ZWL"
    assert response["currency"]["symbol"] == "$"
    assert response["currency"]["localized_symbol"] == "ZWL$"
    assert response["currency"]["conversion_rate"] > 0


def test_get_discount_from_ip_currency():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_discount_from_ip(ipv4_zimbabwe)
    response_eur = parityvend.get_discount_from_ip(ipv4_zimbabwe, "EUR")

    assert (
        response["currency"]["conversion_rate"]
        != response_eur["currency"]["conversion_rate"]
    )


def test_get_discount_with_html_from_ip():
    parityvend = ParityVendAPI(secret_key)
    response = parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_ipv6 = parityvend.get_discount_with_html_from_ip(ipv6_zimbabwe)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = parityvend_free.get_discount_with_html_from_ip(ipv6_zimbabwe)

    assert response == response_ipv6
    assert response_free == response_free_ipv6

    assert "Zimbabwe" in response["html"]
    assert "Zimbabwe" in response_free["html"]

    assert "70.00%" in response["html"]
    assert "70.00%" in response_free["html"]

    assert response["status"] == "ok"
    assert response["discount"] == 0.7
    assert response["discount_str"] == "70.00%"
    assert response["coupon_code"] == "example_coupon"
    assert response["country"] == Country("ZW")

    assert response["currency"]["code"] == "ZWL"
    assert response["currency"]["symbol"] == "$"
    assert response["currency"]["localized_symbol"] == "ZWL$"
    assert response["currency"]["conversion_rate"] > 0

    assert response_free["status"] == "ok"
    assert response_free["discount"] == 0.7
    assert response_free["discount_str"] == "70.00%"
    assert response_free["coupon_code"] == "example_coupon"
    assert response_free["country"] == Country("ZW")

    assert response_free["currency"]["code"] == "ZWL"
    assert response_free["currency"]["symbol"] == "$"
    assert response_free["currency"]["localized_symbol"] == "ZWL$"
    assert response_free["currency"]["conversion_rate"] > 0


def test_get_discount_with_html_from_ip_currency():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_eur = parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe, "EUR")

    assert (
        response["currency"]["conversion_rate"]
        != response_eur["currency"]["conversion_rate"]
    )


def test_get_banner_from_ip():
    parityvend = ParityVendAPI(secret_key)
    response = parityvend.get_banner_from_ip(ipv4_zimbabwe)
    response_ipv6 = parityvend.get_banner_from_ip(ipv6_zimbabwe)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_banner_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = parityvend_free.get_banner_from_ip(ipv6_zimbabwe)

    assert response == response_ipv6
    assert response_free == response_free_ipv6

    assert "This fair pricing is powered by" in response_free
    assert "This fair pricing is powered by" not in response

    assert "Zimbabwe" in response
    assert "Zimbabwe" in response_free

    assert "70.00%" in response
    assert "70.00%" in response_free


def test_invalid_private_key():
    parityvend = ParityVendAPI(invalid_secret_key)

    with pytest.raises(ProcessingError):
        response = parityvend.get_discount_from_ip(ipv4_zimbabwe)


def test_get_discount_from_ip_none():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_discount_from_ip(google_ipv4)
    response_vpn_cn = parityvend.get_discount_from_ip(ipv6_vpn_cn)
    response_ch = parityvend.get_discount_from_ip(ipv4_switzerland)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_discount_from_ip(google_ipv4)
    response_free_ch = parityvend_free.get_discount_from_ip(ipv4_switzerland)

    response["currency"].pop("conversion_rate")
    response_ch["currency"].pop("conversion_rate")
    response_free["currency"].pop("conversion_rate")
    response_free_ch["currency"].pop("conversion_rate")

    assert response == {
        "status": "ok",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("US"),
        "currency": {"code": "USD", "symbol": "$", "localized_symbol": "USD$"},
    }
    assert response_ch == {
        "status": "ok",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("CH"),
        "currency": {"code": "CHF", "symbol": "CHF", "localized_symbol": "CHF"},
    }
    assert response_free == {
        "status": "ok",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("US"),
        "currency": {"code": "USD", "symbol": "$", "localized_symbol": "USD$"},
    }
    assert response_free_ch == {
        "status": "ok",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("CH"),
        "currency": {"code": "CHF", "symbol": "CHF", "localized_symbol": "CHF"},
    }

    assert response_vpn_cn == Response(
        {
            "status": "ok",
            "discount": None,
            "discount_str": None,
            "coupon_code": None,
            "country": {},
            "currency": {},
        }
    )


def test_get_discount_with_html_from_ip_none():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_discount_with_html_from_ip(google_ipv4)
    response_vpn_cn = parityvend.get_discount_with_html_from_ip(ipv6_vpn_cn)
    response_ch = parityvend.get_discount_with_html_from_ip(ipv4_switzerland)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_discount_with_html_from_ip(google_ipv4)
    response_free_ch = parityvend_free.get_discount_with_html_from_ip(ipv4_switzerland)

    response["currency"].pop("conversion_rate")
    response_ch["currency"].pop("conversion_rate")
    response_free["currency"].pop("conversion_rate")
    response_free_ch["currency"].pop("conversion_rate")

    assert response == {
        "status": "ok",
        "html": "",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("US"),
        "currency": {"code": "USD", "symbol": "$", "localized_symbol": "USD$"},
    }
    assert response_ch == {
        "status": "ok",
        "html": "",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("CH"),
        "currency": {"code": "CHF", "symbol": "CHF", "localized_symbol": "CHF"},
    }
    assert response_free == {
        "status": "ok",
        "html": "",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("US"),
        "currency": {"code": "USD", "symbol": "$", "localized_symbol": "USD$"},
    }
    assert response_free_ch == {
        "status": "ok",
        "html": "",
        "discount": 0.0,
        "discount_str": "0.00%",
        "coupon_code": "",
        "country": Country("CH"),
        "currency": {"code": "CHF", "symbol": "CHF", "localized_symbol": "CHF"},
    }

    assert response_vpn_cn == Response(
        {
            "status": "ok",
            "html": None,
            "discount": None,
            "discount_str": None,
            "coupon_code": None,
            "country": {},
            "currency": {},
        }
    )


def test_get_banner_from_ip_none():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_banner_from_ip(google_ipv4)
    response_vpn_cn = parityvend.get_banner_from_ip(ipv6_vpn_cn)
    response_ch = parityvend.get_banner_from_ip(ipv4_switzerland)

    parityvend_free = ParityVendAPI(secret_key_free)
    response_free = parityvend_free.get_banner_from_ip(google_ipv4)
    response_free_ch = parityvend_free.get_banner_from_ip(ipv4_switzerland)

    assert (
        response
        == response_ch
        == response_vpn_cn
        == response_free
        == response_free_ch
        == Response(
            {
                "status": "ok",
                "html": None,
                "discount": None,
                "discount_str": None,
                "coupon_code": None,
                "country": {},
                "currency": {},
            }
        )
    )


def test_get_exchange_rate_info():
    parityvend = ParityVendAPI(secret_key)

    response = parityvend.get_exchange_rate_info()
    rates = response["rates"]

    response_eur = parityvend.get_exchange_rate_info("EUR")
    rates_eur = response_eur["rates"]

    assert "USD" in rates
    assert "EUR" in rates
    assert "GBP" in rates
    assert rates_eur["EUR"] == 1.0
    assert rates["USD"] == 1.0
    assert (isinstance(i, float) for i in rates.values())

    with pytest.raises(ProcessingError):
        parityvend_free = ParityVendAPI(secret_key_free)
        parityvend_free.get_exchange_rate_info()
