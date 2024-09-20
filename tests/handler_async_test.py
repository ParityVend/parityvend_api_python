import json
from ipaddress import IPv4Address, IPv6Address

import pytest
import aiohttp

from parityvend_api import AsyncParityVendAPI
from parityvend_api.cache.default import DefaultCache
from parityvend_api.exceptions import ProcessingError
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


@pytest.mark.asyncio
async def test_init():
    parityvend = AsyncParityVendAPI(secret_key)

    assert parityvend.private_key == secret_key
    assert isinstance(parityvend.cache, DefaultCache)

    assert parityvend.request_options == {
        "headers": {
            "User-Agent": "Python ParityVend API Client/1.0.1 (+https://www.ambeteco.com/ParityVend/docs/index.html)"
        }
    }

    assert parityvend.json_loads == json.loads
    assert parityvend.session is None
    await parityvend.init()
    assert isinstance(parityvend.session, aiohttp.ClientSession)
    await parityvend.deinit()
    assert parityvend.session is None


@pytest.mark.asyncio
async def test_get_country_from_ip():
    parityvend = AsyncParityVendAPI(secret_key)
    parityvend_free = AsyncParityVendAPI(secret_key_free)

    assert await parityvend.get_country_from_ip(google_ipv4) == Country("XX")
    assert await parityvend.get_country_from_ip(ipv6_vpn_cn) == Country("XX")
    assert await parityvend.get_country_from_ip(ipv4_zimbabwe) == Country("ZW")
    assert await parityvend.get_country_from_ip(ipv6_zimbabwe) == Country("ZW")

    assert await parityvend.get_country_from_ip(IPv4Address(google_ipv4)) == Country(
        "XX"
    )
    assert await parityvend.get_country_from_ip(IPv6Address(ipv6_vpn_cn)) == Country(
        "XX"
    )
    assert await parityvend.get_country_from_ip(IPv4Address(ipv4_zimbabwe)) == Country(
        "ZW"
    )
    assert await parityvend.get_country_from_ip(IPv6Address(ipv6_zimbabwe)) == Country(
        "ZW"
    )

    assert await parityvend_free.get_country_from_ip(google_ipv4) == Country("US")
    assert await parityvend_free.get_country_from_ip(ipv6_vpn_cn) == Country("CN")
    assert await parityvend_free.get_country_from_ip(ipv4_zimbabwe) == Country("ZW")
    assert await parityvend_free.get_country_from_ip(ipv6_zimbabwe) == Country("ZW")

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_cache_quota():
    parityvend = AsyncParityVendAPI(secret_key)

    initial_quota = await parityvend.get_quota_info(cache=False)
    assert await parityvend.get_country_from_ip(ipv4_zimbabwe, cache=False) == Country(
        "ZW"
    )
    new_quota = await parityvend.get_quota_info(cache=False)

    assert new_quota["quota_used"] > initial_quota["quota_used"]
    assert new_quota["status"] == "ok"
    assert isinstance(new_quota["quota_limit"], int)
    assert isinstance(new_quota["quota_used"], int)
    assert isinstance(new_quota["quota_left"], int)

    await parityvend.deinit()


@pytest.mark.asyncio
async def test_get_discounts_info():
    parityvend = AsyncParityVendAPI(secret_key)

    discounts_info = await parityvend.get_discounts_info()
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

    await parityvend.deinit()


@pytest.mark.asyncio
async def test_get_discount_from_ip():
    parityvend = AsyncParityVendAPI(secret_key)
    response = await parityvend.get_discount_from_ip(ipv4_zimbabwe)
    response_ipv6 = await parityvend.get_discount_from_ip(ipv6_zimbabwe)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_discount_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = await parityvend_free.get_discount_from_ip(ipv6_zimbabwe)

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

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_get_discount_from_ip_currency():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_discount_from_ip(ipv4_zimbabwe)
    response_eur = await parityvend.get_discount_from_ip(ipv4_zimbabwe, "EUR")

    assert (
        response["currency"]["conversion_rate"]
        != response_eur["currency"]["conversion_rate"]
    )

    await parityvend.deinit()


@pytest.mark.asyncio
async def test_get_discount_with_html_from_ip():
    parityvend = AsyncParityVendAPI(secret_key)
    response = await parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_ipv6 = await parityvend.get_discount_with_html_from_ip(ipv6_zimbabwe)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = await parityvend_free.get_discount_with_html_from_ip(
        ipv6_zimbabwe
    )

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

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_get_discount_with_html_from_ip_currency():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe)
    response_eur = await parityvend.get_discount_with_html_from_ip(ipv4_zimbabwe, "EUR")

    assert (
        response["currency"]["conversion_rate"]
        != response_eur["currency"]["conversion_rate"]
    )

    await parityvend.deinit()


@pytest.mark.asyncio
async def test_get_banner_from_ip():
    parityvend = AsyncParityVendAPI(secret_key)
    response = await parityvend.get_banner_from_ip(ipv4_zimbabwe)
    response_ipv6 = await parityvend.get_banner_from_ip(ipv6_zimbabwe)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_banner_from_ip(ipv4_zimbabwe)
    response_free_ipv6 = await parityvend_free.get_banner_from_ip(ipv6_zimbabwe)

    assert response == response_ipv6
    assert response_free == response_free_ipv6

    assert "This fair pricing is powered by" in response_free
    assert "This fair pricing is powered by" not in response

    assert "Zimbabwe" in response
    assert "Zimbabwe" in response_free

    assert "70.00%" in response
    assert "70.00%" in response_free

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_invalid_private_key():
    parityvend = AsyncParityVendAPI(invalid_secret_key)

    with pytest.raises(ProcessingError):
        await parityvend.get_discount_from_ip(ipv4_zimbabwe)

    await parityvend.deinit()


@pytest.mark.asyncio
async def test_get_discount_from_ip_none():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_discount_from_ip(google_ipv4)
    response_vpn_cn = await parityvend.get_discount_from_ip(ipv6_vpn_cn)
    response_ch = await parityvend.get_discount_from_ip(ipv4_switzerland)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_discount_from_ip(google_ipv4)
    response_free_ch = await parityvend_free.get_discount_from_ip(ipv4_switzerland)

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

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_get_discount_with_html_from_ip_none():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_discount_with_html_from_ip(google_ipv4)
    response_vpn_cn = await parityvend.get_discount_with_html_from_ip(ipv6_vpn_cn)
    response_ch = await parityvend.get_discount_with_html_from_ip(ipv4_switzerland)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_discount_with_html_from_ip(google_ipv4)
    response_free_ch = await parityvend_free.get_discount_with_html_from_ip(
        ipv4_switzerland
    )

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

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_get_banner_from_ip_none():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_banner_from_ip(google_ipv4)
    response_vpn_cn = await parityvend.get_banner_from_ip(ipv6_vpn_cn)
    response_ch = await parityvend.get_banner_from_ip(ipv4_switzerland)

    parityvend_free = AsyncParityVendAPI(secret_key_free)
    response_free = await parityvend_free.get_banner_from_ip(google_ipv4)
    response_free_ch = await parityvend_free.get_banner_from_ip(ipv4_switzerland)

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

    await parityvend.deinit()
    await parityvend_free.deinit()


@pytest.mark.asyncio
async def test_get_exchange_rate_info():
    parityvend = AsyncParityVendAPI(secret_key)

    response = await parityvend.get_exchange_rate_info()
    rates = response["rates"]

    response_eur = await parityvend.get_exchange_rate_info("EUR")
    rates_eur = response_eur["rates"]

    assert "USD" in rates
    assert "EUR" in rates
    assert "GBP" in rates
    assert rates_eur["EUR"] == 1.0
    assert rates["USD"] == 1.0
    assert (isinstance(i, float) for i in rates.values())

    with pytest.raises(ProcessingError):
        parityvend_free = AsyncParityVendAPI(secret_key_free)
        await parityvend_free.get_exchange_rate_info()

    await parityvend.deinit()
    await parityvend_free.deinit()
