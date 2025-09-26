from eth_typing import Address

from dotenv import load_dotenv

from json import load
from os import getenv
from typing import Any

TYPE_PROCEDURE_ABI_FILE = "helpers/type_procedure.idl"

with open(TYPE_PROCEDURE_ABI_FILE, "r") as f:
    TYPE_PROCEDURE_ABI = load(f)


class Settings:
    provider = getenv("PROVIDER")
    admin_private_key = getenv("ADMIN_PRIVATE_KEY")
    type_contract_address: Address = getenv("TYPE_PROCEDURE_ADDRESS")  # type: ignore
    type_register_gas: str = getenv("TYPE_REGISTER_GAS")  # type: ignore
    type_register_price_per_gas: Any = getenv("TYPE_REGISTER_PRICE_PER_GAS")  # type: ignore
    type_contract_info: Any = TYPE_PROCEDURE_ABI_FILE
