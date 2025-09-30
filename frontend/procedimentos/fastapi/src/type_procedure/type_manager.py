from web3.contract import Contract

from eth_typing import Address
from fastapi.exceptions import HTTPException

from src.settings import Settings
from src.type_procedure.model import (
    TypeProcedure,
    TypeProcedureCreate,
)
from src.model import TransactionCreated
from src.web3.http import Web3Manager


class TypeManager:

    w3_manager: Web3Manager
    type_contract: Contract
    admin_address: Address

    def __init__(self, w3_manager: Web3Manager) -> None:
        self.w3_manager = w3_manager
        address = self.w3_manager.checksun_address(Settings.type_contract_address)
        self.admin_address = self.w3_manager.checksun_address(Settings.admin_address)  # type: ignore
        self.type_contract = w3_manager.get_contract(
            address=address, info=Settings.type_contract_info
        )

    def register_type_procedure(
        self, register_dto: TypeProcedureCreate
    ) -> TransactionCreated:

        nonce = self.w3_manager.get_transaction_count()

        transaction = self.type_contract.functions.cadastraTipo(
            register_dto.tipo, register_dto.categoria_profissional_id
        ).build_transaction(
            {
                "nonce": nonce,
                "gasPrice": self.w3_manager.gas_price,
                "from": self.admin_address,
            }
        )

        transaction_signed = self.w3_manager.sign_transaction(transaction)

        try:
            transaction_hash = self.w3_manager.send_raw_transaction(transaction_signed)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        return TransactionCreated(
            transaction_hash=transaction_hash.hex(),
            transaction_url=f"http://127.0.0.1:5000/tx/{transaction_hash.hex()}",
            transaction_logs_url=f"http://127.0.0.1:8080/util/logs/{transaction_hash.hex()}",
        )

    def get_type_procedure(self, id: int) -> TypeProcedure:
        type_procedure_tuple = self.type_contract.functions.getTipo(id).call()
        return TypeProcedure(
            id=id,
            tipo=type_procedure_tuple[1],  # type: ignore
            categoria_profissional_id=type_procedure_tuple[2],
        )

    def delete_type_procedure(self, id: int) -> TransactionCreated:
        nonce = self.w3_manager.get_transaction_count()

        transaction = self.type_contract.functions.deleteTipo(
            id,
        ).build_transaction(
            {
                "nonce": nonce,
                "gasPrice": self.w3_manager.gas_price,
                "from": self.admin_address,
            }
        )

        transaction_signed = self.w3_manager.sign_transaction(transaction)

        try:
            transaction_hash = self.w3_manager.send_raw_transaction(transaction_signed)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

        return TransactionCreated(
            transaction_hash=transaction_hash.hex(),
            transaction_url=f"http://127.0.0.1:5000/tx/{transaction_hash.hex()}",
            transaction_logs_url=f"http://127.0.0.1:8080/util/logs/{transaction_hash.hex()}",
        )
