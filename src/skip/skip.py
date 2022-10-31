import httpx

from hashlib import sha256
from base64 import b64encode
from cosmpy.crypto.keypairs import PrivateKey


def sign_bundle(bundle: list[bytes], 
                private_key: bytes) -> tuple[list[str], bytes]:
    
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
                sync: bool) -> httpx.Response:
    
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
    response = httpx.post(rpc_url, json=data)
    
    # Return response
    return response


def sign_and_send_bundle(bundle: list[bytes], 
                         private_key: bytes, 
                         public_key: str, 
                         rpc_url: str, 
                         desired_height: int,
                         sync: bool) -> str:
    
    # Sign bundle
    b64_encoded_signed_bundle, bundle_signature = sign_bundle(bundle, private_key)
    
    # Send bundle
    response = send_bundle(b64_encoded_signed_bundle, 
                           bundle_signature, 
                           public_key, 
                           rpc_url, 
                           desired_height, 
                           sync)
    
    # Return response
    return response