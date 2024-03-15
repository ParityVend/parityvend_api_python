from parityvend_api import ParityVendAPI, env_get

parityvend = ParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))

# example Venezuela IP
ip = "190.206.117.0"

# by default, get the conversion rate with USD as base
discount_usd = parityvend.get_discount_from_ip(ip)
print("USD discount:", discount_usd)

# the base currency can be changed
discount_gbp = parityvend.get_discount_from_ip(ip, base_currency="GBP")
print("GBP discount:", discount_gbp)

print()

print(
    f"Conversion rate of 1 USD to {discount_usd.currency.code}:",
    discount_usd.currency.conversion_rate,
)
print(
    f"Conversion rate of 1 GBP to {discount_gbp.currency.code}:",
    discount_gbp.currency.conversion_rate,
)


"""

Example "Get discount with custom base currency" (sync)
Identifies the country from the given IP-address and returns the configured discount with the custom base currency.

--- Expected output ---
USD discount: Response(
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
GBP discount: Response(
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
            "conversion_rate": 45.71277583460257,
        },
    }
)

Conversion rate of 1 USD to VES: 36.092756259083146
Conversion rate of 1 GBP to VES: 45.71277583460257

"""
