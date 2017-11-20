#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""OpenExchangeRates API Client for Python 3.6+.

Get your API Key for Free at https://openexchangerates.org/account/app-ids."""


import decimal
from collections import namedtuple
from json import dumps, loads  # uJSON dont support parse_int, parse_float args
from types import MappingProxyType as frozendict
from urllib.parse import urlencode
from urllib.request import urlopen


__version__ = "1.0.0"
__license__ = "GPLv3+ LGPLv3+"
__author__ = "Juan Carlos"
__email__ = "juancarlospaco@gmail.com"
__contact__ = "https://t.me/juancarlospaco"
__maintainer__ = "Juan Carlos"
__url__ = "https://github.com/juancarlospaco/openexchangerate#openexchangerate"
__all__ = ("OpenExchangeRatesClient", )


class _PrettyFloat(float):
    """Float that rounds to 2 when repr it, Private."""
    __slots__ = ()
    def __repr__(self):
        return str(round(self, 2))


class OpenExchangeRates(object):

    """Client for openexchangerate.org."""

    __slots__ = ("api_key", "timeout", "use_float",
                 "round_float", "base", "local_base", "tipe")
    BASE_URL = 'https://openexchangerates.org/api'
    ENDPOINT_LATEST = BASE_URL + '/latest.json'
    ENDPOINT_CURRENCIES = BASE_URL + '/currencies.json'
    ENDPOINT_HISTORICAL = BASE_URL + '/historical/%s.json'

    def __init__(self, api_key: str, timeout: int=60, use_float: bool=True,
                 round_float: bool=True, base: str='USD', local_base: str=None):

        self.api_key: str = str(api_key).strip()
        self.timeout: int = int(timeout)
        self.local_base: str = local_base
        self.base: str = str(base).upper()
        self.tipe = decimal.Decimal        # Decimal, Not Round.
        if use_float and not round_float:  # Floats, Not Round.
            self.tipe = float
        elif use_float and round_float:    # Floats, Round.
            self.tipe = _PrettyFloat

    def _parsed_response(self, response, local_base=None):
        data = loads(response, parse_int=self.tipe,
                     parse_float=self.tipe)['rates']

        if local_base:
            data = self._local_conversion(data, local_base)

        return namedtuple("OpenExchangeRates", "dict frozendict namedtuple")(
            data, frozendict(data),
            namedtuple("OpenExchangeRates", data.keys())(*data.values()))

    def _local_conversion(self, data, local_base):
        """Change base using local conversion,offline,useful for free plan."""
        new_rates = {}
        for curr, value in data.items():
            new_rates[curr] = round(value / data[local_base], 8)
        return new_rates

    def latest(self, base='USD', local_base=None):
        """Fetches latest exchange rate data from openexchangerates."""
        url = (f"{ self.ENDPOINT_LATEST }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        response = urlopen(url, timeout=self.timeout).read()
        return self._parsed_response(response, local_base)

    def currencies(self):
        """Fetches current currency data from openexchangerates."""
        url = (f"{ self.ENDPOINT_CURRENCIES }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        data = loads(urlopen(url, timeout=self.timeout).read())
        return namedtuple("OpenExchangeRates", "dict frozendict namedtuple")(
            data, frozendict(data),
            namedtuple("OpenExchangeRates", data.keys())(*data.values()))

    def historical(self, date, base='USD', local_base=None):
        """Fetches historical exchange rate data from openexchangerates."""
        url = (f"{ self.ENDPOINT_HISTORICAL % date.strftime(r'%Y-%m-%d') }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        response = urlopen(url, timeout=self.timeout).read()
        return self._parsed_response(response, local_base)

    def __enter__(self):
        return self.latest()

    def __exit__(self, exception_type, exception_values, tracebacks, *args):
        pass

    def __iter__(self):
        return iter(self.latest().dict.items())

    def __repr__(self):
        return (f'{self.__class__.__name__}(api_key={self.api_key}, '
                f'timeout={self.timeout}, base={self.base}, '
                f'local_base={self.local_base}, tipe={self.tipe})')
