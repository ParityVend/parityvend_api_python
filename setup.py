from setuptools import setup

long_description = """The official Python client library for the ParityVend API. Add location-based pricing to your Python applications and take your business to a global level."""

setup(
    name="parityvend_api",
    version='1.0.0',
    description="Official Python library for ParityVend API",
    long_description=long_description,
    url="https://github.com/parityvend/api_python",
    author="ParityVend",
    author_email="help@ambeteco.com",
    license="Apache License 2.0",
    packages=["parityvend_api", "parityvend_api.cache"],
    install_requires=["requests>=2.31.0", "cachetools>=5.3.3", "aiohttp>=3.9.3"],
    include_package_data=True,
    zip_safe=False,
)
