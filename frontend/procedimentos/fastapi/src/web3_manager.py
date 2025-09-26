from eth_account import Account
from eth_typing import Address
from fastapi.exceptions import HTTPException
from web3 import Web3, HTTPProvider
from web3.contract import Contract
from web3.exceptions import TimeExhausted

from json import loads
from src.transaction import TransactionGet
from src.settings import Settings


class Web3Manager:

    w3: Web3
    admin_account: Account

    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(Settings.provider))
        self.admin_account = Account.from_key(Settings.admin_private_key)

    def get_contract(self, address: Address, info: dict) -> Contract:
        return self.w3.eth.contract(address=address, abi=info)

    def get_transaction_count(self):
        return self.w3.eth.get_transaction_count(self.admin_account.address)  # type: ignore

    def to_wey(self, value: str):
        return self.w3.to_wei(value, "gwey")

    def is_adress(self, address: Address) -> bool:
        return self.w3.is_address(address)

    def checksun_address(self, address: Address) -> str:
        return self.w3.to_checksum_address(address)

    def sign_transaction(self, transaction) -> bytes:
        return self.w3.eth.account.sign_transaction(
            transaction, private_key=self.admin_account.key  # type: ignore
        )

    def send_raw_transaction(self, raw_transaction: bytes) -> bytes:
        return self.w3.eth.send_raw_transaction(raw_transaction)

    def get_transaction_receipt(self, transaction_hash) -> TransactionGet:
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(
                transaction_hash=transaction_hash, timeout=128
            )

            if receipt["status"] == 0:
                return TransactionGet(
                    status="error",
                    transaction_hash=transaction_hash,
                    receipt=loads(Web3.to_json(dict(receipt))),
                )
            return TransactionGet(
                status="sucess",
                transaction_hash=transaction_hash,
                receipt=loads(Web3.to_json(dict(receipt))),
            )
        except TimeExhausted:
            raise HTTPException(
                status_code=408,
                detail="Timeout. A transação está demorando para ser minerada ou o hash é inválido.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar recibo. Verifique se o hash da transação é válido e se o evento está sendo decodificado corretamente. Detalhe: {str(e)}",
            )
