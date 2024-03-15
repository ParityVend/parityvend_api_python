import asyncio
from parityvend_api import AsyncParityVendAPI, env_get


async def main():
    parityvend = AsyncParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))

    discount = await parityvend.get_discount_from_ip(
        "190.206.117.0"
    )  # example Venezuela IP
    print(discount)

    # You can access the items via dot notation or dictionary key lookups
    print(discount.discount_str)
    print(discount["discount_str"])  # all three will print "40.00%"
    print(discount.get("discount_str"))

    print(discount.currency.code)
    print(discount["currency"]["code"])  # both will print 'VES'

    await parityvend.deinit()  # don't forget to close the session


asyncio.get_event_loop().run_until_complete(main())


"""

Example "Get discount" (async)
Identifies the country from the given IP-address and returns the configured discount.

--- Expected output ---
Response(
    {
        "status": "ok",
        "discount": 0.4,
        "discount_str": "40.00%",
        "coupon_code": "example_coupon",
        "country": Country("VE"),
        "currency": {
            "code": "VES",
            "symbol": "Bs.",
            "localized_symbol": "VESBs.",
            "conversion_rate": 36.092756259083146,
        },
    }
)
40.00%
40.00%
40.00%
VES
VES

"""
