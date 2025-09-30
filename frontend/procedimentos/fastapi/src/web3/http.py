from eth_typing import Address
from fastapi.exceptions import HTTPException
from web3 import Web3, HTTPProvider
from web3.contract.contract import Contract, ContractEvent
from web3.exceptions import TimeExhausted

from json import loads
from typing import Any

from src.model import TransactionGet
from src.settings import Settings


class Web3Manager:

    w3: Web3

    def __init__(self) -> None:
        self.w3 = Web3(HTTPProvider(Settings.provider))
        assert self.w3.is_connected()
        self.gas_price = self.w3.eth.gas_price

    def get_contract(self, address: Address, info: Any) -> Contract:
        return self.w3.eth.contract(address=address, abi=info)

    def get_transaction_count(self):
        return self.w3.eth.get_transaction_count(Settings.admin_address)  # type: ignore

    def is_adress(self, address: Address) -> bool:
        return self.w3.is_address(address)

    def checksun_address(self, address: Address) -> Address:
        return self.w3.to_checksum_address(address)  # type: ignore

    def get_block_filter(self, address: Address):
        return self.w3.eth.filter({"fromBlock": "latest", "address": address})

    def wait_for_transaction_receipt(self, event):
        return self.w3.eth.wait_for_transaction_receipt(event["transactionHash"])

    def sign_transaction(self, transaction):
        return self.w3.eth.account.sign_transaction(
            transaction, private_key=Settings.admin_private_key
        )

    def send_raw_transaction(self, raw_transaction):
        return self.w3.eth.send_raw_transaction(raw_transaction.raw_transaction)

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
