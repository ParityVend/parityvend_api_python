import json
import logging
from ipaddress import IPv4Address, IPv6Address
from typing import Callable, Optional, Union

import requests

from .cache.default import DefaultCache
from .cache.interface import CacheInterface
from .config import API_URL
from .exceptions import APIError, ConnectionError, ProcessingError, QuotaExceededError
from .objects import COUNTRIES, Country, Discounts, Response

logger = logging.getLogger("parityvend")


class ParityVendAPI:
    def __init__(
        self,
        private_key: str,
        request_options: Optional[dict] = None,
        cache_instance: Optional[CacheInterface] = None,
        cache_options: Optional[dict] = None,
        json_loads: Optional[Callable[[str], dict]] = None,
        cache_on_error: bool = True,
        log_api_errors: bool = True,
        raise_exc_on_error: bool = True,
    ):
        """
        Initialize the ParityVendAPI object.

        Args:
            private_key (str): Your ParityVend API private key.
            request_options (Optional[dict], optional): Additional options to pass to the requests library. Defaults to None.
            cache_instance (Optional[CacheInterface], optional): An instance of a custom cache implementation. Defaults to None.
            cache_options (Optional[dict], optional): Options to pass to the default cache implementation. Defaults to None.
            json_loads (Optional[Callable[[str], dict]], optional): A custom function to use for loading JSON data. Defaults to None.
            cache_on_error (bool, optional): Whether to cache API responses on error. Defaults to True.
            log_api_errors (bool, optional): Whether to log API errors. Defaults to True.
            raise_exc_on_error (bool, optional): Whether to raise an exception on API errors. Defaults to True.
        """
        self.private_key: str = private_key

        self.request_options: dict = self.get_default_request_options()
        if request_options:
            self.request_options.update(request_options)

        if cache_instance:
            self.cache: CacheInterface = cache_instance
        else:
            self.cache_options: dict = self.get_default_cache_options()
            if cache_options:
                self.cache_options.update(cache_options)

            self.cache: CacheInterface = DefaultCache(**self.cache_options)

        self.json_loads: Callable[[str], dict] = json.loads
        if json_loads:
            self.json_loads: Callable[[str], dict] = json_loads

        self.session: requests.Session = requests.Session()

        self.cache_on_error: bool = cache_on_error
        self.log_api_errors: bool = log_api_errors
        self.raise_exc_on_error: bool = raise_exc_on_error

    def __repr__(self) -> str:
        return f"ParityVendAPI('{self.private_key[:6]}...')"

    @staticmethod
    def get_default_request_options() -> dict:
        """
        Get the default request options for the API client.

        Returns:
            dict: A dictionary containing the default request options.
        """
        return {
            "headers": {
                "User-Agent": "Python ParityVend API Client/1.0.0 (+https://www.ambeteco.com/ParityVend/docs/index.html)"
            }
        }

    @staticmethod
    def get_default_cache_options() -> dict:
        """
        Get the default cache options for the API client.

        Returns:
            dict: A dictionary containing the default cache options.
        """
        return {"maxsize": 4096, "ttl": 24 * 60 * 60}

    def api_request(
        self, method: str, url: str, request_options: dict
    ) -> Union[dict, str, None]:
        """
        Make a request to the ParityVend API.

        Args:
            method (str): The HTTP method to use (e.g., 'get', 'post', 'put', 'delete').
            url (str): The URL to send the request to.
            request_options (dict): Additional options to pass to the requests library.

        Raises:
            APIError: If the API returns a non-200 status code or an invalid JSON payload.
            ConnectionError: If there is an error connecting to the API.
            ProcessingError: If there is an error with the input data.

        Returns:
            Union[dict, str, None]: The response from the API, either as a dictionary (for JSON responses), a string (for non-JSON responses), or None (if there was an error).
        """
        try:
            r = self.session.request(method, url, **request_options)

            if r.status_code != 200:
                logger.error(
                    f"ParityVend API ({method.upper()}: {url}) returned non-200 status code ({r.status_code=}). See API response below:\n{r.text}\n"
                )
                raise APIError("ParityVend API returned non-200 status code.")

            if r.headers["Content-Type"] == "application/json":
                result = self.json_loads(r.text)

                if self.raise_exc_on_error and result["status"] == "error":
                    raise ProcessingError(
                        f"ParityVend API ({url}) returned error:\n{result}\n"
                    )

                return result
            return r.text

        except requests.exceptions.RequestException:
            raise ConnectionError(
                "Not able to reach the ParityVend API. Check your internet connection."
            )

        except json.JSONDecodeError:
            logger.error(
                f"ParityVend API ({method.upper()}: {url}) returned invalid JSON payload ({r.status_code=}). See API response below:\n{r.text}\n"
            )
            raise APIError("ParityVend API returned invalid JSON payload.")

    def base_call(
        self,
        method: str,
        endpoint_name: str,
        path: str,
        input_vars: dict,
        cache_key: tuple,
        timeout: Union[int, float, None] = None,
        cache: bool = True,
    ) -> Union[dict, str, None]:
        """
        Make a base call to the ParityVend API.

        Args:
            method (str): The HTTP method to use (e.g., 'get', 'post', 'put', 'delete').
            endpoint_name (str): The name of the endpoint being called.
            path (str): The path to the endpoint, including any placeholders for variables.
            input_vars (dict): A dictionary of variables to substitute into the path.
            cache_key (tuple): A tuple representing the cache key for the request.
            timeout (Union[int, float, None], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Raises:
            QuotaExceededError: If the API returns an 'over_quota' error.

        Returns:
            Union[dict, str, None]: The response from the API, either as a dictionary (for JSON responses), a string (for non-JSON responses), or None (if there was an error).
        """
        try:
            if cache:
                cached_response = self.cache[cache_key]
                return cached_response
        except KeyError:
            pass

        request_options = {**self.request_options}
        if isinstance(timeout, (int, float)):
            request_options["timeout"] = timeout

        variables = {
            "private_key": self.private_key,
            **input_vars,
        }

        formatted_path = path.format_map(variables)
        url = f"{API_URL}{formatted_path}"
        result = self.api_request(method, url, request_options)

        if not result:
            return

        if isinstance(result, str):
            self.cache[cache_key] = result
            return result

        if result.get("error_name") == "over_quota":
            raise QuotaExceededError(
                "Your account has exceeded the quota. Upgrade your billing plan to continue. View more information: https://www.ambeteco.com/ParityVend/docs/debugging_guide.html#over-quota"
            )

        if result.get("status") == "error":
            if self.log_api_errors:
                logger.error(
                    f"ParityVend API ({endpoint_name}) returned error:\n{result}\n"
                )

            if self.cache_on_error and result.get("error_name") in (
                "not_identifed",
                "incorrect_request",
            ):
                self.cache[cache_key] = result
        else:
            self.cache[cache_key] = result

        return result

    def get_country_from_ip(
        self,
        ip: Union[str, bytes, IPv4Address, IPv6Address],
        timeout: Optional[Union[int, float]] = None,
        cache: bool = True,
    ) -> Country:
        """
        Get the country associated with an IP address. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-country-from-ip-(private_key)-

        Args:
            ip (Union[str, bytes, IPv4Address, IPv6Address]): The IP address to look up.
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Country: An object representing the country associated with the IP address.
        """
        ip = self.auto_convert_ip(ip)

        result = self.base_call(
            "get",
            "get-country-from-ip",
            "/backend/get-country-from-ip/{private_key}/{ip}/",
            {"ip": ip},
            ("get-country-from-ip", ip),
            timeout,
            cache,
        )

        return COUNTRIES[result["country"]]

    def get_discount_from_ip(
        self,
        ip: Union[str, bytes, IPv4Address, IPv6Address],
        base_currency: Union[str, bytes] = "USD",
        timeout: Optional[Union[int, float]] = None,
        cache: bool = True,
    ) -> Response:
        """
        Get the discount information associated with an IP address. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discount-from-ip-(private_key)-(opt.-base_currency)-

        Args:
            ip (Union[str, bytes, IPv4Address, IPv6Address]): The IP address to look up.
            base_currency (Union[str, bytes], optional): The base currency to use for exchange rates. Defaults to "USD".
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Response: An object containing the discount information for the IP address.
        """
        ip = self.auto_convert_ip(ip)
        base_currency = self.auto_convert_to_str(base_currency).upper()

        result = self.base_call(
            "get",
            "get-discount-from-ip",
            "/backend/get-discount-from-ip/{private_key}/{ip}/{base_currency}/",
            {"ip": ip, "base_currency": base_currency},
            ("get-discount-from-ip", ip, base_currency),
            timeout,
            cache,
        )

        if result["country"]:
            result["country"] = COUNTRIES[result["country"]["code"]]

        return Response(result)

    def get_banner_from_ip(
        self,
        ip: Union[str, bytes, IPv4Address, IPv6Address],
        base_currency: Union[str, bytes] = "USD",
        timeout: Optional[Union[int, float]] = None,
        cache: bool = True,
    ) -> Union[str, Response]:
        """
        Get an HTML banner for the discount information associated with an IP address. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-banner-from-ip-(private_key)-(opt.-base_currency)-

        Args:
            ip (Union[str, bytes, IPv4Address, IPv6Address]): The IP address to look up.
            base_currency (Union[str, bytes], optional): The base currency to use for exchange rates. Defaults to "USD".
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Union[str, Response]: Either a string containing the HTML banner, or a Response object if no banner is available.
        """
        ip = self.auto_convert_ip(ip)
        base_currency = self.auto_convert_to_str(base_currency).upper()

        result = self.base_call(
            "get",
            "get-banner-from-ip",
            "/backend/get-banner-from-ip/{private_key}/{ip}/{base_currency}/",
            {"ip": ip, "base_currency": base_currency},
            ("get-banner-from-ip", ip, base_currency),
            timeout,
            cache,
        )

        if isinstance(result, str):
            return result
        return Response(result)

    def get_discount_with_html_from_ip(
        self,
        ip: Union[str, bytes, IPv4Address, IPv6Address],
        base_currency: Union[str, bytes] = "USD",
        timeout: Optional[Union[int, float]] = None,
        cache: bool = True,
    ) -> Response:
        """
        Get the discount information and the HTML banner associated with an IP address. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discount-with-html-from-ip-(private_key)-(opt.-base_currency)-

        Args:
            ip (Union[str, bytes, IPv4Address, IPv6Address]): The IP address to look up.
            base_currency (Union[str, bytes], optional): The base currency to use for exchange rates. Defaults to "USD".
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Response: An object containing the discount information and HTML banner for the IP address.
        """
        ip = self.auto_convert_ip(ip)
        base_currency = self.auto_convert_to_str(base_currency).upper()

        result = self.base_call(
            "get",
            "get-discount-with-html-from-ip",
            "/backend/get-discount-with-html-from-ip/{private_key}/{ip}/{base_currency}/",
            {"ip": ip, "base_currency": base_currency},
            ("get-discount-with-html-from-ip", ip, base_currency),
            timeout,
            cache,
        )

        if result["country"]:
            result["country"] = COUNTRIES[result["country"]["code"]]

        return Response(result)

    def get_quota_info(
        self, timeout: Optional[Union[int, float]] = None, cache: bool = False
    ) -> Response:
        """
        Get information about the account's API quota. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-quota-info-(private_key)-

        Args:
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to False.

        Returns:
            Response: An object containing the account's quota information.
        """
        result = self.base_call(
            "get",
            "get-quota-info",
            "/backend/get-quota-info/{private_key}/",
            {},
            ("get-quota-info",),
            timeout,
            cache,
        )

        return Response(result)

    def get_discounts_info(
        self, timeout: Optional[Union[int, float]] = None, cache: bool = True
    ) -> Response:
        """
        Get information about all the discounts configured for the current project. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-discounts-info-(private_key)-

        Args:
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Response: An object containing the discount information for the current project.
        """
        result = self.base_call(
            "get",
            "get-discounts-info",
            "/backend/get-discounts-info/{private_key}/",
            {},
            ("get-discounts-info",),
            timeout,
            cache,
        )

        result["discounts"] = Discounts(result["discounts"])
        return Response(result)

    def get_exchange_rate_info(
        self,
        base_currency: Union[str, bytes] = "USD",
        timeout: Optional[Union[int, float]] = None,
        cache: bool = True,
    ) -> Response:
        """
        Get the current exchange rates. Only available to accounts on paid plans. View the API docs here: https://www.ambeteco.com/ParityVend/docs/api_reference.html#get--backend-get-exchange-rate-info-(private_key)-(opt.-base_currency)-

        Args:
            base_currency (Union[str, bytes], optional): The base currency to use for exchange rates. Defaults to "USD".
            timeout (Optional[Union[int, float]], optional): The timeout value for the request. Defaults to None.
            cache (bool, optional): Whether to cache the response. Defaults to True.

        Returns:
            Response: An object containing the exchange rates information.
        """
        base_currency = self.auto_convert_to_str(base_currency).upper()

        result = self.base_call(
            "get",
            "get-exchange-rate-info",
            "/backend/get-exchange-rate-info/{private_key}/{base_currency}/",
            {"base_currency": base_currency},
            ("get-exchange-rate-info", base_currency),
            timeout,
            cache,
        )

        return Response(result)

    @staticmethod
    def auto_convert_ip(ip: Union[str, bytes, IPv4Address, IPv6Address]) -> str:
        if isinstance(ip, str):
            return ip

        if isinstance(ip, bytes):
            return ip.decode("u8")

        if isinstance(ip, (IPv4Address, IPv6Address)):
            return ip.exploded

        raise TypeError(
            f'"ip" is of invalid type "{type(ip)}". "str", "bytes", "ipaddress.IPv4Address" or "ipaddress.IPv6Address" was expected.'
        )

    @staticmethod
    def auto_convert_to_str(text: Union[str, bytes]) -> str:
        if isinstance(text, str):
            return text

        if isinstance(text, bytes):
            return text.decode("u8")

        raise TypeError(
            f'"{text}" is of invalid type "{type(text)}". "str" or "bytes" was expected.'
        )
