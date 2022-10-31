A helper library to sign and send bundles to the Skip Relay in Python.

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
``` python
import skip
```

Alternatively, you can import specific functions to use like so:
``` python
from skip import sign_bundle, send_bundle, sign_and_send_bundle
```

This helper library exposes three functions: `sign_bundle`, `send_bundle`, and `sign_and_send_bundle`.

## Example Usage

``` python

import skip
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

tx_bytes = b'\n\x90\x01\n\x8d\x01\n\x1c/cosmos.bank.v1beta1.MsgSend\x12m\n+juno1zhqrfu9w3sugwykef3rq8t0vlxkz72vwnnptts\x12+juno1ptcltmzllgu0am4c0wmgdlkv5y7r5grsn9h76m\x1a\x11\n\x05junox\x12\x0810000000\x12d\nP\nF\n\x1f/cosmos.crypto.secp256k1.PubKey\x12#\n!\x03H\x14l=[\x1f\xf6bg*,\n\x954\xcc9\x8e\xd2\x0eF\x8dz\x9b\xfdXec\xe7\xbeo\x16\x95\x12\x04\n\x02\x08\x01\x18\x07\x12\x10\n\n\n\x05junox\x12\x010\x10\xa0\x8d\x06\x1a@\x82MzmjC#\xba\xec`\xd0\xde-p\xb6\xba\x1d1\xe5\xdc\r,\x0e59\x88b\x05\x02\xf8]Nf\xd5`\xd0u4V\xfc#\xf2R\xad\xa3\xfe\xaf\x85\xf6\xac\x9a\x8f\x11\xb2\xfaYM#m\xbd\xd4Ozd'

wallet = LocalWallet(PrivateKey('<base64 encoded private key>'), prefix="juno")

response = skip.sign_and_send_bundle(bundle=[tx_bytes], 
                                     private_key=wallet.signer().private_key_bytes,
                                     public_key=wallet.signer().public_key,
                                     rpc_url="http://juno-1-api.skip.money:26657/",
                                     desired_height=0,
                                     sync=True)
```
For a more detailed/runnable example, check out: 
https://github.com/skip-mev/skip-py/blob/main/examples/example.py

## sign_bundle

`sign_bundle` Signs a bundle of transactions and returns the signed bundle and the signature.

``` python
sign_bundle(bundle: list[bytes], private_key: bytes) -> tuple[list[str], bytes]
"""
Args:
    bundle (list[bytes]): A list of transaction bytes to sign. 
        The list of transaction must be in the order as the desired bundle.
        Transaction bytes can be obtained from mempool txs (tx) by applying base64.b64decode(tx)
    private_key (bytes): The private key to sign the bundle with in bytes.

Returns:
    tuple[list[str], bytes]: A tuple of the signed bundle and the signature.
"""
```

## send_bundle

`send_bundle` Sends a signed bundle to the Skip Relay.

``` python
send_bundle(b64_encoded_signed_bundle: list[str], 
            bundle_signature: bytes, 
            public_key: str, 
            rpc_url: str, 
            desired_height: int, 
            sync: bool) -> httpx.Response
"""
Args:
    b64_encoded_signed_bundle (list[str]): A list of base64 encoded signed transactions.
        The list of transaction must be in the order as the desired bundle.
    bundle_signature (bytes): The signature applied to the bundle.
    public_key (str): The base64 encoded public key of the private key used to sign the bundle.
    rpc_url (str): The URL of the Skip Relay RPC.
    desired_height (int): The desired height for the bundle to be included in. 
        Height of 0 can be used to include the bundle in the next block.
    sync (bool): A flag to indicate if the broadcast should be synchronous or not.

Returns:
    httpx.Response: The response from the Skip Relay.
"""
```

## sign_and_send_bundle

`sign_and_send_bundle` Signs and sends a bundle to the Skip Relay (a wrapper function combining sign_bundle and send_bundle)

``` python
sign_and_send_bundle(bundle: list[bytes], 
                     private_key: bytes, 
                     public_key: str, 
                     rpc_url: str, 
                     desired_height: int,
                     sync: bool) -> httpx.Response
"""
Args:
    bundle (list[bytes]): A list of transaction bytes to sign.
        The list of transaction must be in the order as the desired bundle.
        Transaction bytes can be obtained from mempool txs (tx) by applying base64.b64decode(tx)
    private_key (bytes): The private key to sign the bundle with in bytes.
    public_key (str): The base64 encoded public key of the private key used to sign the bundle.
    rpc_url (str): The URL of the Skip Relay RPC.
    desired_height (int): The desired height for the bundle to be included in.
    sync (bool): A flag to indicate if the broadcast should be synchronous or not.

Returns:
    str: The response from the Skip Relay.
"""
```