import functools
from typing import Dict, Optional, Union, Sequence

from .data import COUNTRIES_META


@functools.total_ordering
class Country(dict):
    """
    A class representing a country and its associated metadata.

    This class inherits from the `dict` class and provides an object-oriented interface ('dot notation') for
    accessing the country-related data, such as name, currency, and emoji flag.

    Args:
        code (Union[str, bytes]): The code representing the country (e.g., "US", "FR", "JP").

    Raises:
        ValueError: If an invalid country code is provided.

    Attributes:
        code (str): The ISO code representing the country.
        name (str): The name of the country.
        emoji_flag (str): The emoji flag representing the country.
        currency_code (str): The code representing the country's currency.
        currency_symbol (str): The symbol representing the country's currency.
        currency_localized (str): The localized representation of the country's currency.
    """

    __slots__ = (
        "code",
        "name",
        "emoji_flag",
        "currency_code",
        "currency_symbol",
        "currency_localized",
    )

    def __init__(self, code: Union[str, bytes]):
        try:
            if isinstance(code, bytes):
                code = code.decode("utf8")
            code = code.upper()
            meta = COUNTRIES_META[code]
        except (KeyError, TypeError, ValueError):
            raise ValueError(
                f'"Country" object received invalid country code "{code}".'
            )

        name, emoji_flag, currency_code, currency_symbol, currency_localized = meta

        self.code: str = code
        self.name: str = name
        self.emoji_flag: str = emoji_flag
        self.currency_code: str = currency_code
        self.currency_symbol: str = currency_symbol
        self.currency_localized: str = currency_localized

        super(Country, self).__init__(
            {
                "code": code,
                "name": name,
                "emoji_flag": emoji_flag,
                "currency_code": currency_code,
                "currency_symbol": currency_symbol,
                "currency_localized": currency_localized,
            }
        )

    def __repr__(self) -> str:
        return f"Country({self.code!r})"

    def __str__(self) -> str:
        return f"Country {self.name} ({self.code})"

    @staticmethod
    def _is_valid_operand(other) -> bool:
        return hasattr(other, "code") and isinstance(other, Country)

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.code == other.code

    def __lt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.code < other.code


class Response(dict):
    """
    A class representing a JSON response from an API.

    This class inherits from the `dict` class and provides an additional way to access
    its keys and nested dictionaries as attributes (via 'dot notation').

    Args:
        *args: Positional arguments, typically dictionaries or other objects that can be converted to dictionaries.
        **kwargs: Keyword arguments, typically key-value pairs that will be added to the dictionary.
    """

    def __init__(self, *args, **kwargs):
        super(Response, self).__init__(*args, **kwargs)

        for arg in args:
            if isinstance(arg, dict) and not isinstance(arg, Discounts):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        arg[k] = Response(v)

        if kwargs:
            for k, v in kwargs.items():
                if isinstance(v, dict):
                    kwargs[k] = Response(v)

    def __getattr__(self, attr):
        """
        Allows accessing dictionary keys as attributes ('dot notation').
        """
        value = self[attr]

        if isinstance(value, dict) and not isinstance(value, Discounts):
            return Response(value)
        else:
            return value

    def __repr__(self) -> str:
        return f"Response({super(Response, self).__repr__()})"


@functools.total_ordering
class Discount(dict):
    """
    A class representing a discount and its associated metadata.

    This class inherits from the `dict` class and provides an object-oriented interface ('dot notation') for
    accessing and managing discount-related data, such as the discount value, coupon code, and associated country.

    Args:
        country (Country): The `Country` object associated with the discount.
        coupon_code (Optional[str]): The coupon code associated with the discount.
        discount (Optional[float]): The discount value as a float between 0 and 1.
        raw_discount (Optional[Sequence]): A tuple containing the coupon code and discount value.

    Attributes:
        discount (float): The discount value as a float between 0 and 1.
        discount_str (str): The discount value as a string formatted as a percentage ('40.00%').
        coupon_code (str): The coupon code associated with the discount.
        country (Country): The `Country` object associated with the discount.
        raw_discount (Optional[Sequence]): The raw discount data used to initialize the object.
    """

    __slots__ = (
        "discount",
        "discount_str",
        "coupon_code",
        "country",
        "raw_discount",
    )

    def __init__(
        self,
        country: Country,
        coupon_code: Optional[str] = None,
        discount: Optional[float] = None,
        raw_discount: Optional[Sequence] = None,
    ):
        self.raw_discount = raw_discount

        if raw_discount:
            if isinstance(raw_discount, Discount):
                coupon_code = raw_discount.coupon_code
                discount = raw_discount.discount
            else:
                coupon_code, discount = raw_discount
            discount_str = f"{discount:.2%}"

            self.coupon_code: str = coupon_code
            self.discount: float = discount
            self.discount_str: str = discount_str
        else:
            self.discount: float = 0.0
            self.discount_str: str = "0.00%"
            self.coupon_code: str = ""

        self.country: Country = country

        super(Discount, self).__init__(
            {
                "discount": self.discount,
                "discount_str": self.discount_str,
                "coupon_code": self.coupon_code,
                "country": self.country,
                "raw_discount": self.raw_discount,
            }
        )

    def __repr__(self) -> str:
        return f"Discount({self.country!r}, {self.coupon_code!r}, {self.discount!r})"

    @staticmethod
    def _is_valid_operand(other) -> bool:
        return hasattr(other, "country") and isinstance(other, Discount)

    def __eq__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.country["code"] == other.country["code"]

    def __lt__(self, other) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.country["code"] < other.country["code"]


class Discounts(dict):
    """
    A class representing a collection of `Discount` objects.

    This class inherits from the `dict` class and provides a convenient way to manage and access
    discounts associated with different countries (via 'dot notation').

    Args:
        raw_discounts (dict): A dictionary containing raw discount data, where the keys are country codes
                               and the values are tuples of (coupon_code, discount_value).
    """

    def __init__(self, raw_discounts: dict):
        self.raw_discounts: dict = raw_discounts

        discounts = {
            key: Discount(get_country_by_code(key), raw_discount=value)
            for key, value in raw_discounts.items()
        }

        self.discounts: dict = discounts
        super(Discounts, self).__init__(discounts)

    def get_discount_by_country(self, country: Union[Country, str, bytes]) -> Discount:
        """
        Retrieves the `Discount` object associated with the given country.

        Args:
            country (Union[Country, str, bytes]): The country for which to retrieve the discount.
                                                   Can be a `Country` object, a country code string, or bytes.

        Returns:
            Discount: The `Discount` object associated with the given country.
        """
        country = self.auto_convert_country(country)
        return self.discounts[country]

    @staticmethod
    def auto_convert_country(country: Union[Country, str, bytes]) -> Country:
        if isinstance(country, Country):
            return country["code"]

        if isinstance(country, bytes):
            country = country.decode("utf8")

        return country.upper()

    def __repr__(self) -> str:
        return f"Discounts({self.discounts!r})"


def get_country_by_code(country_code: Union[str, bytes]) -> Country:
    """
    Retrieves the `Country` object associated with the given country code.

    Args:
        country_code (Union[str, bytes]): The country code for which to retrieve the `Country` object.

    Returns:
        Country: The `Country` object associated with the given country code.
    """
    if isinstance(country_code, bytes):
        country_code = country_code.decode("utf8")

    country_code = country_code.upper()
    return COUNTRIES.get(country_code)


COUNTRIES: Dict[str, Country] = {key: Country(key) for key in COUNTRIES_META}
