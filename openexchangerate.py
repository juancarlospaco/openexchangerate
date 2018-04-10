#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""OpenExchangeRates API Client for Python 3.6+.

Get your API Key for Free at https://openexchangerates.org/account/app-ids."""


import decimal
from collections import namedtuple
from datetime import datetime
from json import dumps, loads  # uJSON dont support parse_int, parse_float args
from types import MappingProxyType as frozendict
from urllib.parse import urlencode
from urllib.request import urlopen


__version__ = "1.5.5"
__all__ = ("OpenExchangeRatesClient", )


class _RoundedFloat(float):
    """Float that rounds to 2 when repr it, Private."""
    __slots__ = ()

    def __str__(self):
        value = str(round(self, 2))
        if value == "0.0":  # For Bitcoin,Gold,etc.
            value = str(round(self, 6))
        return value


class OpenExchangeRates(object):

    """Client for openexchangerate.org."""

    __slots__ = ("api_key", "timeout", "use_float", "round_float",
                 "base", "local_base", "tipe", "html_table_header")
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
        self.use_float: bool = use_float
        self.round_float: bool = round_float
        self.html_table_header: bool = True
        self.tipe = _RoundedFloat                    # Floats, Round.
        if self.use_float and not self.round_float:
            self.tipe = float                        # Floats, Not Round.
        elif not self.use_float:
            self.tipe = decimal.Decimal              # Decimal, Not Round.

    def _parsed_response(self, response):
        data = loads(response, parse_int=self.tipe,
                     parse_float=self.tipe)['rates']

        if self.local_base:
            data = self._local_conversion(data, self.local_base)

        return namedtuple(
            "OpenExchangeRates", "dict frozendict html namedtuple")(
            data, frozendict(data), self.html(data),
            namedtuple("OpenExchangeRates", data.keys())(*data.values()))

    def _local_conversion(self, data, local_base):
        """Change base using local conversion,offline,useful for free plan."""
        new_rates = {}
        for curr, value in data.items():
            new_rates[curr] = round(value / data[local_base], 8)
        return new_rates

    def latest(self):
        """Fetches latest exchange rate data from openexchangerates."""
        url = (f"{ self.ENDPOINT_LATEST }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        response = urlopen(url, timeout=self.timeout).read()
        return self._parsed_response(response)

    def currencies(self):
        """Fetches current currency data from openexchangerates."""
        url = (f"{ self.ENDPOINT_CURRENCIES }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        data = loads(urlopen(url, timeout=self.timeout).read())
        return namedtuple("OpenExchangeRates", "dict frozendict namedtuple")(
            data, frozendict(data),
            namedtuple("OpenExchangeRates", data.keys())(*data.values()))

    def historical(self, since_date: datetime):
        """Fetches historical exchange rate data from openexchangerates."""
        if isinstance(since_date, datetime):
            since_date = since_date.strftime(r'%Y-%m-%d')
        url = (f"{ self.ENDPOINT_HISTORICAL % since_date }?"
               f"{ urlencode({'app_id': self.api_key, 'base': self.base}) }")
        response = urlopen(url, timeout=self.timeout).read()
        return self._parsed_response(response)

    def html(self, prices_data_dict: dict):
        names_get = self.currencies().frozendict.get
        prices = tuple(enumerate(prices_data_dict.items()))
        row = "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>"
        h = "<thead><th>#</th><th>Code</th><th>Price</th><th>Name</th></thead>"

        rows = [row.format(index, mony[0], mony[1], names_get(mony[0], "???"))
                for index, mony in prices
                if mony[0] not in ("EUR", "USD")]  # Skip Dollar and Euro.

        prio = [row.format(index, mony[0], mony[1], names_get(mony[0], "???"))
                for index, mony in prices
                if mony[0] in ("EUR", "USD")]  # Move Dollar and Euro at Top.

        return (f"<table>{ h if self.html_table_header else ''}"
                f"<tbody>{' '.join(prio + rows)}</tbody></table>")

    def __enter__(self):
        return self.latest()

    def __exit__(self, exception_type, exception_values, tracebacks, *args):
        pass

    def __iter__(self):
        return iter(self.latest().dict.items())

    def __repr__(self):
        return (f'{self.__class__.__name__}(api_key:str={self.api_key}, '
                f'timeout:int={self.timeout}, use_float:bool={self.use_float},'
                f' round_float:bool={self.round_float}, base:str={self.base}, '
                f'local_base:str={self.local_base}, tipe:type={self.tipe})')

    def __str__(self):
        if self.use_float:  # decimal.Decimal is not JSON Serializable.
            return dumps(self.latest().dict, sort_keys=True, indent=4).strip()
