A helper library to sign and send bundles to the Skip Relay.

PyPi: https://pypi.org/project/skip-python/0.1.0/

Github: https://github.com/skip-mev/skip-py

# Quick Start

## Prerequisite

In the latest release, skip-python requires:

- Python 3.10 or later

Check your python version by entering:

```bash
python3 --version
```

## Installation

There are 2 ways to use skip-python: `pip`, or `git clone`.

### via `pip`

```bash
pip install skip-python
```

### via `git clone`

``` bash
git clone https://github.com/skip-mev/skip-py.git
```

After cloning, you can move the skip folder into your respective development repo and import the helper library.

## Usage

Import the package with:
```bash
import skip
```

Alternatively, you can import specific functions to use:
```bash
from skip import sign_bundle, send_bundle, sign_and_send_bundle
```
