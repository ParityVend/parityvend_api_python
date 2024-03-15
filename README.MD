# ParityVend API Python Library

**Welcome to the ParityVend API Python Library!** This library simplifies the process of integrating ParityVend's location-based pricing into your Python applications, allowing you to expand your business and take it to a global level.

[![ParityVend API Python Library - cover](https://github.com/ParityVend/parityvend_api_python/blob/main/images/_cover_gh.png?raw=true)](https://www.ambeteco.com/ParityVend/)

ParityVend is a powerful tool that helps businesses go global by offering smart pricing that adapts to each visitor's purchasing power based on their location. By using ParityVend, you can customize the prices of your products to match the economic diversity of the global market, just like industry giants Netflix, Google, Microsoft, Apple, and Spotify do. This approach ensures that your products are competitively priced in various countries, helping you expand your customer base, increase sales, and optimize profits.

The ParityVend API Python library helps you interact with the ParityVend API more easily. It provides ready-to-use functions that act as a wrapper for the ParityVend API's backend endpoints. This wrapper simplifies the use of ParityVend's features in your Python backends, microservices, or other server-side applications.

By using this library, you can take advantage of ParityVend's powerful API features to:

- adjust your prices based on visitors' locations.
- implement anti-abuse systems to protect against fraudulent activities like VPN, proxy, and TOR.
- get information about your customers' locations.

You can find more integration ideas in the ParityVend documentation: [ParityVend integration ideas](https://www.ambeteco.com/ParityVend/docs/api_integration_tutorial.html#integration-ideas).

**Key features include:**

- Easy Integration: Simplified access to the ParityVend API endpoints.
- Asynchronous Support: Provides both synchronous and asynchronous handlers.
- Simplified API Usage: The library abstracts away the complexities of the raw API, allowing you to focus on your application logic.
- Pythonic responses: Providing convenient response types, such as `Response`, `Country`, `Discounts`, etc. instead of raw JSON.

## Documentation

For the ParityVend API Python library, please refer to ['quick start' section](https://github.com/ParityVend/parityvend_api_python?tab=readme-ov-file#quick-start)

For general documentation on the ParityVend API, please refer to [https://www.ambeteco.com/ParityVend/docs/api_reference.html](https://www.ambeteco.com/ParityVend/docs/api_reference.html)

## Requirements and Dependencies

The library is cross-platform. It is compatible with all Python versions 3.8 to 3.13 (including support for PyPy). The ParityVend API Python library uses `requests` for the synchronous handler and `aiohttp` for the asynchronous handler, as well as `cachetools` for providing memoization.

[![ParityVend API Python Library - Getting Started](https://github.com/ParityVend/parityvend_api_python/blob/main/images/_get_started_cover_gh.png?raw=true)](https://www.ambeteco.com/ParityVend/)

## Getting Started

To use the ParityVend API, you need to obtain an API key, also known as a `private_key`. ParityVend offers a generous free plan that allows you to get your API key without any cost.

### Free Plan

The free plan provides the following benefits:

- 7,500 requests per month
- Full access to the API and its functionality (except for the currency exchange endpoint and anti-abuse systems)
- No "demo-like" restrictions or limitations

### Getting the Free API Key

To get your free API key, follow these steps:

1. Visit the [ParityVend Pricing Page](https://www.ambeteco.com/ParityVend/pricing/).
2. Sign up for the free plan by providing the required information.
3. Create a new project. Your API key (`private_key`) will be issued and made available to you.

### Paid Plans

If you require more monthly requests or need access to the currency exchange endpoint and advanced anti-abuse systems, you can consider upgrading to one of the paid plans offered by ParityVend.

To explore the paid plan options and pricing details, visit the [ParityVend Pricing Page](https://www.ambeteco.com/ParityVend/pricing/).

With your API key (`private_key`) in hand, you can start integrating the ParityVend API into your applications and benefiting from its features and functionality.

### Installation

**Pre-built Package**

If you simply want to use the library without modifying the source code, install it using pip:

```bash
pip install --upgrade parityvend_api
```

**Installation from Source**

To install from the source code (useful for development or customization):

```bash
python setup.py install
```

### Quick Start

The library provides two main handlers that provide convenient access to the ParityVend API: `ParityVendAPI` and `AsyncParityVendAPI`, which need to be initiated with your account's private API key, available in the [Dashboard](https://www.ambeteco.com/ParityVend/dash/).

- `ParityVendAPI`: This class is designed for synchronous interactions with the ParityVend API (via `requests`).
- `AsyncParityVendAPI`: Provides asynchronous functions for improved performance (via `aiohttp`).

Check out the [examples folder](https://github.com/ParityVend/parityvend_api_python/tree/main/examples) for more, or get started with these simple snippets below.

**Get country information from an IP Address**
View the full documentation for this API endpoint here: [get-country-from-ip](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-country-from-ip-(private_key)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> ip_address = '190.206.117.0' # an example IP from Venezuela
>>> country = parityvend.get_country_from_ip(ip_address)
>>> country
Country('VE')
>>> country.name # you can use the dot notation to access data
'Venezuela'
>>> country.code
'VE'
>>> country.emoji_flag
'🇻🇪'
>>> country.currency_code
'VES'
>>> country.currency_symbol
'Bs.'
>>> country.currency_localized
'VESBs.'
>>> country['name']  # you can also use dictionary lookups
'Venezuela'
```

**Get discount information from an IP Address**
View the full documentation for this API endpoint here: [get-discount-from-ip](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discount-from-ip-(private_key)-(opt.-base_currency)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> ip_address = '190.206.117.0' # an example IP from Venezuela
>>> response = parityvend.get_discount_from_ip(ip_address)
>>> response
Response({'status': 'ok', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': {'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 36.092756259083146}})
>>> response.discount
0.4
>>> response.currency.code
'VES'
>>> response['coupon_code']
'example_coupon'
```

**Get discount banner from an IP Address**
View the full documentation for this API endpoint here: [get-banner-from-ip](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-banner-from-ip-(private_key)-(opt.-base_currency)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> ip_address = '190.206.117.0' # an example IP from Venezuela
>>> banner = parityvend.get_banner_from_ip(ip_address)
>>> print(banner)
We're committed to fair pricing worldwide and support <span class="parityvend-var-country-name">Venezuela</span>'s purchasing power. Enjoy a <span class="parityvend-var-discount-str">40.00%</span> discount with code <span class="parityvend-var-coupon-code">example_coupon</span>. Happy shopping!
```

**Get discount information with the HTML banner from an IP Address**
View the full documentation for this API endpoint here: [get-discount-with-html-from-ip](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discount-with-html-from-ip-(private_key)-(opt.-base_currency)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> ip_address = '190.206.117.0' # an example IP from Venezuela
>>> response = parityvend.get_discount_with_html_from_ip(ip_address)
>>> response
Response({'status': 'ok', 'html': 'We\'re committed to fair pricing worldwide and support <span class="parityvend-var-country-name">Venezuela</span>\'s purchasing power. Enjoy a <span class="parityvend-var-discount-str">40.00%</span> discount with code <span class="parityvend-var-coupon-code">example_coupon</span>. Happy shopping!', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': {'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 36.092756259083146}})
>>> print(response.html)
We're committed to fair pricing worldwide and support <span class="parityvend-var-country-name">Venezuela</span>'s purchasing power. Enjoy a <span class="parityvend-var-discount-str">40.00%</span> discount with code <span class="parityvend-var-coupon-code">example_coupon</span>. Happy shopping!
>>> response.discount_str
'40.00%'
>>>
```

**Get your account quota information**
View the full documentation for this API endpoint here: [get-quota-info](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-quota-info-(private_key)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> response = parityvend.get_quota_info()
>>> response
Response({'status': 'ok', 'quota_limit': 1000000, 'quota_used': 4716, 'quota_left': 995284})
>>> response.quota_limit
1000000
>>> response['quota_used']
4716
>>>
```

**Get all the discounts for the current project**
View the full documentation for this API endpoint here: [get-discounts-info](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discounts-info-(private_key)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> response = parityvend.get_discounts_info()
>>> response
Response({'status': 'ok', 'discounts': Discounts({'AC': Discount(Country('AC'), '', 0.0), 'AD': Discount(Country('AD'), '', 0.0), 'AE': Discount(Country('AE'), '', 0.0), 'AF': Discount(Country('AF'), 'example_coupon', 0.7), 'AG': Discount(Country('AG'), 'example_coupon', 0.2), 'AI': Discount(Country('AI'), 'example_coupon', 0.2), 'AL': Discount(Country('AL'),  ... })}) # discounts information for all 255 countries
>>>
>>> response.discounts['VE'] # access individual countries with key lookups
Discount(Country('VE'), 'example_coupon', 0.4)
>>> response.discounts['US']
Discount(Country('US'), '', 0.0)
>>> # or via the bound method:
>>> response.discounts.get_discount_by_country('CA')
Discount(Country('CA'), '', 0.0)
>>>
>>> # the discount object has the discount itself, as well as coupon code and country information
>>> response.discounts['VE'].discount_str
'40.00%'
>>> response.discounts['VE'].coupon_code
'example_coupon'
>>> response.discounts['VE'].country
Country('VE')
>>>
```

**Get the currency exchange rates (only for accounts with paid plans)**
View the full documentation for this API endpoint here: [get-exchange-rate-info](<https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-exchange-rate-info-(private_key)-(opt.-base_currency)->)

```python
>>> from parityvend_api import ParityVendAPI
>>> parityvend = ParityVendAPI('your_private_key')
>>> response = parityvend.get_exchange_rate_info()
>>> response
Response({'status': 'ok', 'rates': Response({'AED': 3.6728503704071045, 'AFN': 72.5033950805664, 'ALL': 95.3699951171875, 'AMD': 404.7422790527344, 'ANG': 1.803326964378357, 'AOA': 828.7760620117188, 'ARS': 819.7839965820312, 'AUD': 1.5208089351654053, 'AWG': 1.8025002479553223, 'AZN': 1.6963270902633667, 'BAM': 1.7974870204925537, 'BBD': 2.020319700241089, 'BDT': 109.81781005859375, 'BGN': 1.7990400791168213, 'BHD': 0.3769211173057556, 'BIF': 2859.500244140625, ... })})
>>> response.rates.EUR
0.9195351004600525
>>> response.rates.GBP
0.7895551323890686
>>>
>>> # you can also change the base currency
>>> response_eur = parityvend.get_exchange_rate_info(base_currency='EUR')
>>> response_eur.rates.USD
1.0875060558319092
>>> response_eur.rates.EUR
1.0
>>>
```

**Some utility functions and miscellaneous stuff:**

```python
>>> from parityvend_api import env_get, get_country_by_code, COUNTRIES
>>>
>>> COUNTRIES # a dict of country ISO codes to a pre-created 'Country' object
{'AC': Country('AC'), 'AD': Country('AD'), 'AE': Country('AE'), 'AF': Country('AF'), 'AG': Country('AG'), ..., 'ZM': Country('ZM'), 'ZW': Country('ZW'), 'XX': Country('XX')}
>>> COUNTRIES['GB']
Country('GB')
>>> COUNTRIES['AU']
Country('AU')
>>>
>>>
>>> get_country_by_code('CA') # get the 'Country' object from the ISO code
Country('CA')
>>> country = get_country_by_code('US')
>>> country.name
'United States of America'
>>>
>>>
>>> # get an environment variable if it exists, or return the default value
>>> env_get('some_env_variable', 'default value')
'default value'
>>>
```

### The `base_currency` argument

The functions `get_discount_from_ip`, `get_banner_from_ip`, `get_discount_with_html_from_ip`, and `get_exchange_rate_info` all have an optional keyword argument called `base_currency`. This argument allows you to specify a base currency for calculating the exchange rate of the IP's local currency. The default value for `base_currency` is `USD`.

```python
>>> ...
>>> # set the `base_currency` to 'EUR'. By default, it's set to 'USD'
>>> response_eur = parityvend.get_discount_from_ip(ip_address, base_currency='EUR')
>>> response_eur
Response({'status': 'ok', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': Response({'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 39.25109100341797})})
>>> print(f'1 EUR is {response_eur.currency.conversion_rate} {response_eur.currency.code}')
1 EUR is 39.25109100341797 VES
>>>
>>> response_gbp = parityvend.get_discount_from_ip(ip_address, base_currency='GBP')
>>> response_gbp
Response({'status': 'ok', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': {'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 45.71277583460257}})
>>> print(f'1 GBP is {response_gbp.currency.conversion_rate} {response_eur.currency.code}')
1 GBP is 45.71277583460257 VES
>>>
```

### Asynchronous support

An asynchronous handler, `AsyncParityVendAPI`, can be used in the same way as the synchronous handler:

```python
from parityvend_api import AsyncParityVendAPI
import asyncio

async def run():
    parityvend = AsyncParityVendAPI("your private key")
    ip_address = "190.206.117.0"  # an example IP from Venezuela
    country = await parityvend.get_country_from_ip(ip_address)
    print(repr(country)) # will print 'Country("VE")'
    await parityvend.deinit()  # don't forget to close the session

loop = asyncio.get_event_loop().run_until_complete(run())
```

### The `timeout` and `cache` Keyword Arguments

Each function in the library accepts two optional keyword arguments: `timeout` and `cache`. These arguments allow you to customize the behavior of the API requests and the caching mechanism on a per-call basis.

#### Using the `timeout` argument

The `timeout` argument specifies the maximum amount of time (in seconds) to wait for the API request to complete before raising a timeout error. By default, all functions in the library have `timeout=None`, which means that the operating system's default timeout value will be used.

You can override this default behavior by passing a specific value (in seconds) to the `timeout` argument. For example:

```python
parityvend.get_country_from_ip('8.8.8.8', timeout=5)  # set a 5-second timeout
```

Setting an appropriate timeout value can help prevent your application from getting stuck indefinitely waiting for a response from the API.

#### Using the `cache` argument

The `cache` argument allows you to enable or disable the caching mechanism for a specific API call. All functions in the library have `cache=True` by default, which means that they will return a cached response if it's available in the cache. This behavior helps optimize your API quota usage and reduce response times.

However, there may be situations where you want to bypass the cache and always fetch fresh data from the API. In such cases, you can set `cache=False` when calling the function.

One exception to the default behavior is the `get_quota_info` function, which has `cache=False` by default. This is because quota information is expected to change frequently, and serving stale cached data could lead to inaccurate quota calculations.

```python
parityvend.get_country_from_ip('8.8.8.8', cache=False)  # Bypass the cache
```

### The `Response` object

The functions in this library return a `Response` object that contains all fields listed in the [ParityVend API documentation](https://www.ambeteco.com/ParityVend/docs/api_reference.html#backend-primary-endpoints) for the given endpoint, along with some additional properties and functionality. You can access the response properties using dot notation or dictionary-style lookup methods. The `"country"` and `"discounts"` items in the response are automatically converted to auxiliary `Country` and `Discounts` objects, respectively. These objects provide additional methods and attributes for ease of use. For example:

```python
...
>>> r = parityvend.get_discount_from_ip("190.206.117.0")
>>> r # the Response object looks like this:
Response({'status': 'ok', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': Response({'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 36.092756259083146})})
>>> r.discount # access the data via dot notation...
0.4
>>> r.country.name
'Venezuela'
>>> r.currency.conversion_rate
36.092756259083146
>>> r['currency']['conversion_rate'] # ... or like a dictionary key lookup
36.092756259083146
>>>
...
>>> # All the functions return Response objects:
>>> parityvend.get_discount_from_ip("190.206.117.0")
Response({'status': 'ok', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': {'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 36.092756259083146}})
>>> parityvend.get_discount_with_html_from_ip("190.206.117.0")
Response({'status': 'ok', 'html': 'We\'re committed to fair pricing worldwide and support <span class="parityvend-var-country-name">Venezuela</span>\'s purchasing power. Enjoy a <span class="parityvend-var-discount-str">40.00%</span> discount with code <span class="parityvend-var-coupon-code">example_coupon</span>. Happy shopping!', 'discount': 0.4, 'discount_str': '40.00%', 'coupon_code': 'example_coupon', 'country': Country('VE'), 'currency': {'code': 'VES', 'symbol': 'Bs.', 'localized_symbol': 'VESBs.', 'conversion_rate': 36.092756259083146}})
>>> parityvend.get_quota_info("190.206.117.0")
Response({'status': 'ok', 'quota_limit': 1000000, 'quota_used': 4188, 'quota_left': 995812})
>>>
```

### Caching

This library provides in-memory caching of API responses by default, using the [cachetools](https://cachetools.readthedocs.io/en/latest/) library. The caching mechanism employs a Least Recently Used (LRU) cache with a Time to Live (TTL) value. This means that cached values will be kept for a specified duration, and when the cache reaches its maximum size, the least recently used entries will be automatically removed to accommodate new ones.

Caching helps optimize your API quota usage and reduces response times by serving cached data instead of making redundant API requests. However, it's important to note that cached data may become stale over time, so the cache should be invalidated or refreshed as needed, depending on your application's requirements.

#### Default Caching Options

By default, the following caching options are applied:

- **Maximum Cache Size**: 4096 entries (using multiples of 2 for memory efficiency)
- **Time to Live (TTL)**: 24 hours (86,400 seconds)

These default settings aim to provide a balance between cache performance and memory usage. However, you can modify these settings to suit your specific needs.

#### Modifying Cache Options

You can customize the cache behavior by setting the `cache_options` keyword argument when initializing the handler. The `cache_options` parameter should be a dictionary, where the keys are keyword arguments accepted by the `cachetools` library. For more advanced caching options and configurations, refer to the [cachetools documentation](https://cachetools.readthedocs.io/en/latest/).

```python
>>> from parityvend_api import ParityVendAPI
>>>
>>> # the cache is enabled by default! you don't have to do anything.
>>> parityvend = ParityVendAPI("your private key")
>>>
>>> # let's measure the quota usage via the 'get_quota_info' endpoint
>>> quota_used = parityvend.get_quota_info().quota_used
>>>
>>> # these three calls will only send one request and return the cached response
>>> parityvend.get_country_from_ip("190.206.117.0")
Country('VE')
>>> parityvend.get_country_from_ip("190.206.117.0")
Country('VE')
>>> parityvend.get_country_from_ip("190.206.117.0")
Country('VE')
>>>
>>> new_quota_used = parityvend.get_quota_info().quota_used
>>> print(new_quota_used - quota_used) # this will show how much quota was used
1
>>> # Thanks to the cache, only 1 request was sent, even though we called the function 3 times.
>>>
>>> # specify the cache options like this:
>>> ParityVendAPI(
...     "your private key",
...     cache_options={
...         "ttl": 60 * 60 * 8,
...         "maxsize": 2048,
...     },
... )
ParityVendAPI('...')
>>>
>>>
```

### Modifying Request Options

The library uses the popular `requests` (for synchronous requests) and `aiohttp` (for asynchronous requests) libraries under the hood to make API calls. You can modify the behavior of these requests by setting the `request_options` keyword argument when initializing the handler.

The `request_options` parameter should be a dictionary where the keys are keyword arguments accepted by the `requests` or `aiohttp` library, depending on whether you're using the synchronous or asynchronous handler. These options will be passed to each API request made by the handler, allowing you to customize various aspects of the requests, such as headers, timeouts, proxies, and more. For a complete list of available options and their descriptions, please refer to the documentation of the `requests` library (for synchronous handlers) or the `aiohttp` library (for asynchronous handlers).

```python
>>> from parityvend_api import ParityVendAPI
>>>
>>> parityvend = ParityVendAPI("your private key", request_options={
    "headers": {
        "User-Agent": "just an example"
    }
})
```

## Contributing

Contributions to the ParityVend API Python Library are welcome and encouraged! We appreciate any feedback, bug reports, or feature requests that can help improve the library and make it more useful for the community.

Please refer to the [`CONTRIBUTING.md`](https://github.com/ParityVend/parityvend_api_python/blob/main/CONTRIBUTING.md) file for more detailed guidelines on how to contribute, including the environment setup, coding standards, and testing requirements.

## License

The ParityVend API Python Library is released under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). This means that you are free to use, modify, and distribute this library in your commercial or non-commercial software products, as long as you comply with the terms of the license.

The Apache 2.0 License is a permissive open-source license that allows you to:

- Use the library in your projects, both commercial and non-commercial.
- Modify the library's source code to suit your needs.
- Distribute the library or your modified versions of it.

However, you must include a copy of the Apache 2.0 License and the copyright notice in any distribution of the library or modified versions of it.

## Support

If you encounter any issues or challenges during the integration process, we recommend referring to the ParityVend documentation as your first resource. It provides comprehensive guidance to help you troubleshoot and resolve any errors you may encounter. If you require further support, our team is always ready to assist you. Feel free to [contact us](https://www.ambeteco.com/ParityVend/contact-us/) for personalized assistance to ensure a seamless integration experience, or view the [FAQ section](https://www.ambeteco.com/ParityVend/support/) on the ParityVend Support page.