# openexchangerate

OpenExchangeRates API client for Python 3.7+, worldwide exchange prices + Bitcoin price.
Can be used as context manager or iterator. Namedtuple, dict and HTML outputs. No dependencies. Float or Decimal. Optional Timeout. Optional round. 1 file.


![screenshot](openexchangerates.png)


![screenshot](temp.png)


- [Example HTML output from `OpenExchangeRates(api_key).latest().html`](https://github.com/juancarlospaco/openexchangerate/blob/master/sample.html)


# Install

```bash
pip install openexchangerate
```


# Use

```python
from openexchangerate import OpenExchangeRates

client = OpenExchangeRates(api_key="21e7c27676972")

client.latest().namedtuple      # .dict for Dictionary, .html for HTML.
client.currencies().namedtuple  # .frozendict for Inmutable Dictionary.

for name, price in client:  # Iterator support.
    print(name, price)

with client as prices:  # Context Manager support.
    print(prices.frozendict)

```


# Tests

```
python -m unittest tests.py --verbose
```


# Description of OpenExchangeRates

##### OpenExchangeRates
<details>

`openexchangerate.OpenExchangeRates(api_key: str, timeout: int=60, use_float: bool=True,
             round_float: bool=True, base: str='USD', local_base: str=None)`

**Description:** Returns namedtuple or dict with current international exchange prices and Bitcoin price.

**Arguments:**
- `api_key` Your API Key, [you can get one for Free here](https://openexchangerates.org/account/app-ids), string type.
- `timeout` Timeout on Seconds for network connections, integer type, optional.
- `use_float` `True` for `float`, `False` for `decimal.Decimal`, boolean type, optional.
- `round_float` `True` to round floats to 2 decimals, using `round(float, 2)`, boolean type, optional.
- `base` Base currency, **Only for Pay accounts!**, defaults to `"USD"`, string type, optional.
- `local_base` Local Base currency, for Free accounts, to calculate values locally (offline), string type, optional.

**Keyword Arguments:** None.

**Returns:** namedtuple.

**Dependencies:** None.

**Source Code file:** https://github.com/juancarlospaco/openexchangerate/blob/master/openexchangerate.py

| State              | OS          | Description |
| ------------------ |:-----------:| -----------:|
| :white_check_mark: | **Linux**   | Works Ok    |
| :white_check_mark: | **Os X**    | Works Ok    |
| :white_check_mark: | **Windows** | Works Ok    |

**Usage Example:**

```python
>>> from openexchangerate import OpenExchangeRates
>>> OpenExchangeRates("21e7c27676972").latest()
```
</details>
