import skip

from base64 import b64encode
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins
from cosmpy.aerial.client import LedgerClient, NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.aerial.tx import Transaction, SigningCfg
from cosmpy.crypto.keypairs import PrivateKey
from cosmpy.protos.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from cosmpy.protos.cosmos.base.v1beta1.coin_pb2 import Coin

# EDIT VARIABLES - Default values are for Juno Mainnet
GRPC_URL  = "grpc+https://juno-grpc.lavenderfive.com:443/"
SKIP_RPC_URL = "http://juno-1-api.skip.money/"
ADDRESS_PREFIX = "juno"

# REQUIRES YOUR OWN MNEMONIC TO BE SET
MNEMONIC = ""

def main():
    # Create network config and client
    cfg = NetworkConfig(
        chain_id="juno-1",
        url=GRPC_URL,
        fee_minimum_gas_price=0.0025,
        fee_denomination="ujuno",
        staking_denomination="ujuno",
    )
    client = LedgerClient(cfg)

    # Create wallet from mnemonic
    seed_bytes = Bip39SeedGenerator(MNEMONIC).Generate()
    bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.COSMOS).DeriveDefaultPath()
    wallet = LocalWallet(PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes()), prefix=ADDRESS_PREFIX)
    
    # Get Private Key Object
    private_key = wallet.signer()
    
    # Create send transaction, get tx bytes and encoded tx
    tx_bytes, encoded_tx = create_send_tx(client=client, 
                                          wallet=wallet, 
                                          denom="ujuno", 
                                          amount=1, 
                                          from_address=str(wallet.address()), 
                                          to_address="juno1dxays0mrk84uyr8ztr93e6ext9qutcgxhq5lvv", 
                                          gas_limit=100000)
    
    # Sign and send bundle to Skip Relay
    response = skip.sign_and_send_bundle(bundle=[tx_bytes], 
                                         private_key=private_key.private_key_bytes,
                                         public_key=private_key.public_key,
                                         rpc_url=SKIP_RPC_URL,
                                         desired_height=0,
                                         sync=True)
    
    # Print json response
    print(response.json())


def create_send_tx(client, 
                   wallet, 
                   denom: str, 
                   amount: int, 
                   from_address: str, 
                   to_address: str, 
                   gas_limit: int, 
                   ) -> tuple[bytes, str]:
    # Create send messsage
    msg_send = MsgSend()
    msg_send.from_address = from_address
    msg_send.to_address = to_address
    coin = Coin()
    coin.denom = denom
    coin.amount = str(amount)
    msg_send.amount.append(coin)

    # Add message to transaction
    tx = Transaction()
    tx.add_message(msg_send)

    # Set fee
    fee = "0ujuno"

    # Get account
    account = client.query_account(str(wallet.address()))

    # Seal, Sign, and Complete Tx
    tx.seal(signing_cfgs=[SigningCfg.direct(wallet.public_key(), account.sequence)], fee = fee, gas_limit=gas_limit)
    tx.sign(wallet.signer(), client.network_config.chain_id, account.number)
    tx.complete()

    # Get tx bytes
    tx_bytes = tx.tx.SerializeToString()

    # Get b64 encoded tx
    encoded_tx = b64encode(tx_bytes).decode("utf-8")
    
    # Return tx bytes and encoded tx
    return tx_bytes, encoded_tx


if __name__ == "__main__":
    main()