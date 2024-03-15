from parityvend_api import ParityVendAPI, env_get

parityvend = ParityVendAPI(env_get("PARITYVEND_SECRET_KEY", ""))

country = parityvend.get_country_from_ip("190.206.117.0")  # example Venezuela IP
print(country)

print("Code:", country.code)  # prints 'VE'
print("Name:", country.name)  # prints 'Venezuela'
print("Currency code:", country.currency_code)  # prints 'VES'
print("Currency localized:", country.currency_localized)  # prints 'VESBs.'
print("Currency symbol:", country.currency_symbol)  # prints 'Bs.'

invalid_country = parityvend.get_country_from_ip("8.8.8.8")
print('"8.8.8.8" is:', invalid_country)

# Output varies based on ParityVend account type (if the 'anti-VPN' feature is available):
# Paid account (with anti-VPN): 'Country Unknown (XX)'
# Free account (without anti-VPN): 'Country United States of America (US)'

"""

Example "Get country" (sync)
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
