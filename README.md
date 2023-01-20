A helper library to sign and send bundles to the Skip Relay in Python.

PyPi: https://pypi.org/project/skip-python/

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

## Example Usage

``` python

import skip
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.keypairs import PrivateKey

tx_bytes = b'<tx bytes>'

wallet = LocalWallet(PrivateKey('<base64 encoded private key>'), prefix="juno")

response = skip.sign_and_send_bundle(bundle=[tx_bytes], 
                                     private_key=wallet.signer().private_key_bytes,
                                     public_key=wallet.signer().public_key,
                                     rpc_url="http://juno-1-api.skip.money/",
                                     desired_height=0,
                                     sync=True)
```
For a more detailed/runnable example, check out:

https://github.com/skip-mev/skip-py/blob/main/examples/example.py

## Detailed Usage

Import the package with:
``` python
import skip
```

Alternatively, you can import specific functions to use like so:
``` python
from skip import sign_bundle, send_bundle, sign_and_send_bundle, send_secure_transaction
```

This helper library exposes four functions: `sign_bundle`, `send_bundle`, `sign_and_send_bundle`, and `send_secure_transaction`.

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
            sync: bool,
            timeout: float | None = 10) -> httpx.Response
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
    timeout (float | None): Number of seconds to wait before throwing a read timeout error
        for httpx. Default is 10 seconds.

Returns:
    httpx.Response: The response from the Skip Relay.
"""
```

## sign_and_send_bundle

`sign_and_send_bundle` Signs and sends a bundle to the Skip Relay (a wrapper function combining sign_bundle and send_bundle).

``` python
sign_and_send_bundle(bundle: list[bytes], 
                     private_key: bytes, 
                     public_key: str, 
                     rpc_url: str, 
                     desired_height: int,
                     timeout: float | None = 10) -> httpx.Response
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
    timeout (float | None): Number of seconds to wait before throwing a read timeout error
        for httpx. Default is 10 seconds.

Returns:
    httpx.Response: The response from the Skip Relay.
"""
```

## send_secure_transaction

`send_secure_transaction` Sends a transaction securely through Skip Secure. The transaction's memo must be equal to the transaction sender address.

``` python
send_secure_transaction(transaction: bytes,
                        rpc_url: str,
                        timeout: float | None = 10) -> httpx.Response
"""
Sends a transaction through Skip Secure.

Args:
    transaction (str): Base64 encoded signed transaction to send.
    rpc_url (str): The URL of the Skip Secure RPC.
    timeout (float | None): Number of seconds to wait before throwing a read timeout error
    for httpx. Default is 10 seconds.

Returns:
    httpx.Response: The response from Skip Secure.
"""
```
