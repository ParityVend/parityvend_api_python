import asyncio
from parityvend_api import AsyncParityVendAPI, env_get


async def main():
    parityvend = AsyncParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))

    country = await parityvend.get_country_from_ip(
        "190.206.117.0"
    )  # example Venezuela IP
    print(country)

    print("Code:", country.code)  # prints 'VE'
    print("Name:", country.name)  # prints 'Venezuela'
    print("Currency code:", country.currency_code)  # prints 'VES'
    print("Currency localized:", country.currency_localized)  # prints 'VESBs.'
    print("Currency symbol:", country.currency_symbol)  # prints 'Bs.'

    invalid_country = await parityvend.get_country_from_ip("8.8.8.8")
    print('"8.8.8.8" is:', invalid_country)

    await parityvend.deinit()  # don't forget to close the session


asyncio.get_event_loop().run_until_complete(main())

# Output varies based on ParityVend account type (if the 'anti-VPN' feature is available):
# Paid account (with anti-VPN): 'Country Unknown (XX)'
# Free account (without anti-VPN): 'Country United States of America (US)'

"""

Example "Get country" (async)
Identifies the country from the given IP-address and prints it.

--- Expected output ---
Country Venezuela (VE)
Code: VE
Name: Venezuela
Currency code: VES
Currency localized: VESBs.
Currency symbol: Bs.
"8.8.8.8" is: Country Unknown (XX) # will be printed on a paid account
"8.8.8.8" is: Country United States of America (US) # will be printed on a free account

"""
