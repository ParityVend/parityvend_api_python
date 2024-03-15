from setuptools import setup

from parityvend_api.config import VERSION

long_description = """
The official Python library for ParityVend API.

parityvend_api prides itself on being the most reliable, accurate, and in-depth source of IP address data available anywhere.
We process terabytes of data to produce our custom IP geolocation, company, carrier and IP type data sets.
You can visit our developer docs at https://parityvend_api.io/developers.
"""

setup(
    name="parityvend_api",
    version=VERSION,
    description="Official Python library for ParityVend API",
    long_description=long_description,
    url="https://github.com/parityvend/api_python",
    author="ParityVend",
    author_email="help@ambeteco.com",
    license="Apache License 2.0",
    packages=["parityvend_api", "parityvend_api.cache"],
    install_requires=["requests", "cachetools", "aiohttp<=4"],
    include_package_data=True,
    zip_safe=False,
)
