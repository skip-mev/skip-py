import httpx

from hashlib import sha256
from base64 import b64encode
from cosmpy.crypto.keypairs import PrivateKey


def sign_bundle(bundle: list[bytes], 
                private_key: bytes) -> tuple[list[str], bytes]:
    """Signs a bundle of transactions and returns the signed bundle and the signature.

    Args:
        bundle (list[bytes]): A list of transaction bytes to sign. 
            The list of transaction must be in the order as the desired bundle.
            Transaction bytes can be obtained from mempool txs (tx) by applying base64.b64decode(tx)
        private_key (bytes): The private key to sign the bundle with in bytes.

    Returns:
        tuple[list[str], bytes]: A tuple of the signed bundle and the signature.
    """
    
    # Create digest of flattened bundle
    bundle_digest = sha256(b''.join(bundle)).digest()
    
    # Create private key object to sign with
    priv_key = PrivateKey(private_key)
    
    # Sign digest of bundle
    bundle_signature = priv_key.sign_digest(bundle_digest)
    
    # Create b64 encoded bundle
    base64_encoded_bundle = [b64encode(tx).decode('utf-8') for tx in bundle]
    
    # Return b64 encoded bundle and signature
    return base64_encoded_bundle, bundle_signature


def send_bundle(b64_encoded_signed_bundle: list[str], 
                bundle_signature: bytes, 
                public_key: str, 
                rpc_url: str, 
                desired_height: int,
                sync: bool,
                timeout: float | None = 10) -> httpx.Response:
    """Sends a signed bundle to the Skip Relay.

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
    
    # Choose broadcast method based on sync boolean
    if sync:
        method = 'broadcast_bundle_sync'
    else:
        method = 'broadcast_bundle_async'
    
    # Create data parameter for RPC request
    data = {'jsonrpc': '2.0',
            'method': method,
            'params': [b64_encoded_signed_bundle, 
                       str(desired_height), 
                       public_key, 
                       b64encode(bundle_signature).decode("utf-8")],
            'id': 1}

    # Send post request to RPC with data, get response
    response = httpx.post(rpc_url, json=data, timeout=timeout, follow_redirects=True)
    
    # Return response
    return response


def sign_and_send_bundle(bundle: list[bytes], 
                         private_key: bytes, 
                         public_key: str, 
                         rpc_url: str, 
                         desired_height: int,
                         sync: bool,
                         timeout: float | None = 10) -> httpx.Response:
    """Signs and sends a bundle to the Skip Relay.

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
        httpx.Response: The response from the Skip Relay.
    """
    
    # Sign bundle
    b64_encoded_signed_bundle, bundle_signature = sign_bundle(bundle, private_key)
    
    # Send bundle
    response = send_bundle(b64_encoded_signed_bundle, 
                           bundle_signature, 
                           public_key, 
                           rpc_url, 
                           desired_height, 
                           sync,
                           timeout)
    
    # Return response
    return response


def send_secure_transaction(transaction: str,
                            rpc_url: str,
                            timeout: float | None = 10) -> httpx.Response:
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

    # Create data parameter for RPC request
    data = {'jsonrpc': '2.0',
            'method': 'broadcast_tx_sync',
            'params': [transaction],
            'id': 1}

    # Send post request to RPC with data, get response
    response = httpx.post(rpc_url, json=data, timeout=timeout, follow_redirects=True)

    # Return response
    return response
