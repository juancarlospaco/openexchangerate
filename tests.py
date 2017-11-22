#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Unittests for OpenExchangeRates Client for Python 3.6+."""


import decimal
import unittest
from collections import namedtuple
from random import randint
from types import MappingProxyType as frozendict

import openexchangerate
from httpretty import HTTPretty, httprettified


unittest.TestLoader.sortTestMethodsUsing = lambda _, x, y: randint(-1, 1)


class TestOpenExchangeRates(unittest.TestCase):

    maxDiff, __slots__ = None, ()

    _FIXTURE_CURRENCIES = """{
        "AED": "United Arab Emirates Dirham",
        "AFN": "Afghan Afghani",
        "ALL": "Albanian Lek",
        "USD": "United States Dollar"
    }"""

    _FIXTURE_LATEST = """{"rates": {
        "AED": 3.666311,
        "AFN": 51.2281,
        "ALL": 104.748751,
        "USD": 1}
    }"""

    _FIXTURE_HISTORICAL = """{"rates": {
        "AED": 3.666311,
        "AFN": 51.2281,
        "ALL": 104.748751,
        "USD": 1}
    }"""

    def setUp(self):
        self._date: str= f"201{randint(0, 7)}-{randint(1, 12)}-{randint(1, 25)}"

    def tearDown(self):
        del self._date

    @httprettified
    def test_historical_float(self):
        """Tests openexchangerate.OpenExchangeRateClient.historical()."""
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)))
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_HISTORICAL %
                               self._date,
                               body=self._FIXTURE_LATEST)
        historical = client.historical(self._date)

        self.assertIsInstance(historical, tuple)
        self.assertIsInstance(historical.dict, dict)
        self.assertIsInstance(historical.frozendict, frozendict)

        self.assertIn('AED', historical.dict)
        self.assertEqual(historical.dict['AED'], 3.666311)
        self.assertIn('AFN', historical.dict)
        self.assertEqual(historical.dict['AFN'], 51.2281)
        self.assertIn('ALL', historical.dict)
        self.assertEqual(historical.dict['ALL'], 104.748751)
        self.assertIn('USD', historical.dict)
        self.assertEqual(historical.dict['USD'], 1.0)

    @httprettified
    def test_historical_decimal(self):
        """Tests openexchangerate.OpenExchangeRateClient.historical()."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY',
                                                           use_float=False)
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_HISTORICAL %
                               self._date,
                               body=self._FIXTURE_LATEST)
        historical = client.historical(self._date)

        self.assertIsInstance(historical, tuple)
        self.assertIsInstance(historical.dict, dict)
        self.assertIsInstance(historical.frozendict, frozendict)

        self.assertIn('AED', historical.dict)
        self.assertEqual(historical.dict['AED'], decimal.Decimal('3.666311'))
        self.assertIn('AFN', historical.dict)
        self.assertEqual(historical.dict['AFN'], decimal.Decimal('51.2281'))
        self.assertIn('ALL', historical.dict)
        self.assertEqual(historical.dict['ALL'], decimal.Decimal('104.748751'))
        self.assertIn('USD', historical.dict)
        self.assertEqual(historical.dict['USD'], decimal.Decimal('1'))

    @httprettified
    def test_currencies_float(self):
        """Tests openexchangerate.OpenExchangeRateClient.currencies()."""
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)))
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_CURRENCIES,
                               body=self._FIXTURE_CURRENCIES)
        currencies = client.currencies()

        self.assertIsInstance(currencies, tuple)
        self.assertIsInstance(currencies.dict, dict)
        self.assertIsInstance(currencies.frozendict, frozendict)

        self.assertIn('AED', currencies.dict)
        self.assertIn('AFN', currencies.dict)
        self.assertIn('ALL', currencies.dict)
        self.assertIn('USD', currencies.dict)

    @httprettified
    def test_latest_float(self):
        """Tests openexchangerate.OpenExchangeRateClient.latest()."""
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)))
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        latest = client.latest()

        self.assertIsInstance(latest, tuple)
        self.assertIsInstance(latest.dict, dict)
        self.assertIsInstance(latest.frozendict, frozendict)

        self.assertIn('AED', latest.dict)
        self.assertEqual(latest.dict['AED'], 3.666311)
        self.assertIn('AFN', latest.dict)
        self.assertEqual(latest.dict['AFN'], 51.2281)
        self.assertIn('ALL', latest.dict)
        self.assertEqual(latest.dict['ALL'], 104.748751)
        self.assertIn('USD', latest.dict)
        self.assertEqual(latest.dict['USD'], 1.0)

    @httprettified
    def test_latest_decimal(self):
        """Tests openexchangerate.OpenExchangeRateClient.latest()."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY',
                                                           use_float=False)
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        latest = client.latest()

        self.assertIsInstance(latest, tuple)
        self.assertIsInstance(latest.dict, dict)
        self.assertIsInstance(latest.frozendict, frozendict)

        self.assertIn('AED', latest.dict)
        self.assertEqual(latest.dict['AED'], decimal.Decimal('3.666311'))
        self.assertIn('AFN', latest.dict)
        self.assertEqual(latest.dict['AFN'], decimal.Decimal('51.2281'))
        self.assertIn('ALL', latest.dict)
        self.assertEqual(latest.dict['ALL'], decimal.Decimal('104.748751'))
        self.assertIn('USD', latest.dict)
        self.assertEqual(latest.dict['USD'], decimal.Decimal('1'))

    @httprettified
    def test_latest_with_local_base_conversion_float(self):
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)), local_base='AED')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        latest_local_conversion = client.latest()

        self.assertIsInstance(latest_local_conversion, tuple)
        self.assertIsInstance(latest_local_conversion.dict, dict)
        self.assertIsInstance(latest_local_conversion.frozendict, frozendict)

        self.assertEqual(latest_local_conversion.dict['AED'], 1.0)
        self.assertEqual(latest_local_conversion.dict['AFN'], 13.97265535)
        self.assertEqual(latest_local_conversion.dict['ALL'], 28.57061253)
        self.assertEqual(latest_local_conversion.dict['USD'], 0.27275373)

    @httprettified
    def test_latest_with_local_base_conversion_decimal(self):
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', use_float=False, local_base='AED')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        latest_cn = client.latest()

        self.assertIsInstance(latest_cn, tuple)
        self.assertIsInstance(latest_cn.dict, dict)
        self.assertIsInstance(latest_cn.frozendict, frozendict)

        self.assertEqual(latest_cn.dict['AED'], decimal.Decimal('1'))
        self.assertEqual(latest_cn.dict['AFN'], decimal.Decimal('13.97265535'))
        self.assertEqual(latest_cn.dict['ALL'], decimal.Decimal('28.57061253'))
        self.assertEqual(latest_cn.dict['USD'], decimal.Decimal('0.27275373'))

    @httprettified
    def test_historical_with_local_base_conversion_float(self):
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)), local_base='AED')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_HISTORICAL %
                               self._date,
                               body=self._FIXTURE_HISTORICAL)
        historical_conversion = client.historical(self._date)

        self.assertIsInstance(historical_conversion, tuple)
        self.assertIsInstance(historical_conversion.dict, dict)
        self.assertIsInstance(historical_conversion.frozendict, frozendict)

        self.assertEqual(historical_conversion.dict['AED'], 1.0)
        self.assertEqual(historical_conversion.dict['AFN'], 13.97265535)
        self.assertEqual(historical_conversion.dict['ALL'], 28.57061253)
        self.assertEqual(historical_conversion.dict['USD'], 0.27275373)

    @httprettified
    def test_historical_with_local_base_conversion_decimal(self):
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', use_float=False, local_base='AED')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_HISTORICAL %
                               "2012-12-12",
                               body=self._FIXTURE_HISTORICAL)
        histo_cn = client.historical("2012-12-12")

        self.assertIsInstance(histo_cn, tuple)
        self.assertIsInstance(histo_cn.dict, dict)
        self.assertIsInstance(histo_cn.frozendict, frozendict)

        self.assertEqual(histo_cn.dict['AED'], decimal.Decimal('1.0'))
        self.assertEqual(histo_cn.dict['AFN'], decimal.Decimal('13.97265535'))
        self.assertEqual(histo_cn.dict['ALL'], decimal.Decimal('28.57061253'))
        self.assertEqual(histo_cn.dict['USD'], decimal.Decimal('0.27275373'))

    @httprettified
    def test_exception_latest(self):
        """Tests openexchangerate.OpenExchangeRateClientException()."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY')
        HTTPretty.register_uri(
            HTTPretty.GET, client.ENDPOINT_LATEST, status=404)
        with self.assertRaises(Exception):
            client.latest()

    @httprettified
    def test_exception_currencies(self):
        """Tests openexchangerate.OpenExchangeRateClientException()."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_CURRENCIES,
                               body=self._FIXTURE_CURRENCIES, status=404)
        with self.assertRaises(Exception):
            client.currencies()

    @httprettified
    def test_exception_historical(self):
        """Tests openexchangerate.OpenExchangeRateClient.historical()."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY')
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_HISTORICAL %
                               self._date,
                               body=self._FIXTURE_LATEST, status=404)
        with self.assertRaises(Exception):
            client.historical(self._date)

    def test_inmutable_class_attributes(self):
        """Tests OpenExchangeRateClient can not add attributes."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY')
        with self.assertRaises(AttributeError):
            client.bad_unwanted_attribute = "This should not happen."
            setattr(client, "bad_unwanted_attribute", "This should not happen")

    def test_repr(self):
        """Tests OpenExchangeRateClient can not add attributes."""
        client = openexchangerate.OpenExchangeRates('DUMMY_API_KEY')
        assert repr(client)  # str repr :)

    @httprettified
    def test_contextmanager(self):
        """Tests openexchangerate.OpenExchangeRateClient.latest()."""
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)))
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        with client as exchange_prices:
            self.assertIsInstance(exchange_prices, tuple)
            self.assertIsInstance(exchange_prices.dict, dict)
            self.assertIsInstance(exchange_prices.frozendict, frozendict)

            self.assertIn('AED', exchange_prices.dict)
            self.assertEqual(exchange_prices.dict['AED'], 3.666311)
            self.assertIn('AFN', exchange_prices.dict)
            self.assertEqual(exchange_prices.dict['AFN'], 51.2281)
            self.assertIn('ALL', exchange_prices.dict)
            self.assertEqual(exchange_prices.dict['ALL'], 104.748751)
            self.assertIn('USD', exchange_prices.dict)
            self.assertEqual(exchange_prices.dict['USD'], 1.0)

    @httprettified
    def test_iter(self):
        """Tests openexchangerate.OpenExchangeRateClient.latest()."""
        client = openexchangerate.OpenExchangeRates(
            'DUMMY_API_KEY', round_float=bool(randint(0, 1)))
        HTTPretty.register_uri(HTTPretty.GET, client.ENDPOINT_LATEST,
                               body=self._FIXTURE_LATEST)
        for item in client:
            self.assertIsInstance(item, tuple)
