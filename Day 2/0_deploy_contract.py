from algokit_utils import AppManager, AlgorandClient, AppCreateParams, SigningAccount, AppCreateSchema
from dotenv import load_dotenv, set_key
import os

load_dotenv('./.env')

sk = os.getenv('sk')
pk = os.getenv('pk')
signing_account = SigningAccount(
    private_key=sk,
    address=pk
)

algorand = AlgorandClient.testnet()
app_manager = AppManager(algod_client=algorand.client.algod)
approval_teal = open("Day 2/approval.teal").read()
clear_teal = open("Day 2/clear.teal").read()

compiled_approval = app_manager.compile_teal(approval_teal)
compiled_clear = app_manager.compile_teal(clear_teal)

# print(compiled_approval.compiled)
# print(compiled_clear.compiled)

state_schema = AppCreateSchema(
    global_ints=3,
    global_byte_slices=3,
    local_ints=0,
    local_byte_slices=0,
)

txn_response = algorand.send.app_create(
    AppCreateParams(
        sender=signing_account.address,
        signer=signing_account.signer,
        approval_program=compiled_approval.compiled_base64_to_bytes,
        clear_state_program=compiled_clear.compiled_base64_to_bytes,
        schema=state_schema
    )
)

print(txn_response.tx_id)
print(txn_response.app_id)
set_key('./.env', 'app_id', str(txn_response.app_id))