from parityvend_api import ParityVendAPI, env_get

parityvend = ParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))

discount = parityvend.get_discount_from_ip("190.206.117.0")  # example Venezuela IP
print(discount)

# You can access the items via dot notation or dictionary key lookups
print(discount.discount_str)
print(discount["discount_str"])  # all three will print "40.00%"
print(discount.get("discount_str"))

print(discount.currency.code)
print(discount["currency"]["code"])  # both will print 'VES'

"""

Example "Get discount" (sync)
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
