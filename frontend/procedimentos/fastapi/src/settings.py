from eth_typing import Address

from dotenv import load_dotenv

from json import load
from os import getenv
from typing import Any

load_dotenv()

TYPE_PROCEDURE_ABI_FILE = "helpers/type_procedure.json"
PROCEDURE_ABI_FILE = "helpers/procedure.json"


with open(TYPE_PROCEDURE_ABI_FILE, "r") as f:
    TYPE_PROCEDURE_ABI = load(f)

with open(PROCEDURE_ABI_FILE, "r") as f:
    PROCEDURE_ABI = load(f)


class Settings:
    provider = getenv("PROVIDER")
    admin_address = getenv("ADMIN_ADDRESS")
    admin_private_key = getenv("ADMIN_PRIVATE_KEY")
    type_contract_address: Address = getenv("TYPE_PROCEDURE_ADDRESS")  # type: ignore
    procedure_contract_address: Address = getenv("PROCEDURE_ADDRESS")  # type: ignore
    procedure_info: Any = PROCEDURE_ABI
    type_register_gas: str = getenv("TYPE_REGISTER_GAS")  # type: ignore
    type_contract_info: Any = TYPE_PROCEDURE_ABI
