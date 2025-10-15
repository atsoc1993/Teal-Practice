from algokit_utils import AlgorandClient, AppCallParams, SigningAccount
from algosdk.transaction import OnComplete
from dotenv import load_dotenv, set_key
import typing as t
import os

load_dotenv('./.env')

sk = os.getenv('sk')
pk = os.getenv('pk')
signing_account = SigningAccount(
    private_key=sk,
    address=pk
)

algorand = AlgorandClient.testnet()

app_id = int(os.getenv('app_id'))

txn_response = algorand.send.app_call(
    AppCallParams(
        sender=signing_account.address,
        signer=signing_account.signer,
        args=[(5).to_bytes(4, 'big')],
        app_id=app_id,
        on_complete=OnComplete.NoOpOC
    )
)

print(txn_response.tx_id)

