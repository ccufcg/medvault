from web3.contract import Contract

from fastapi.exceptions import HTTPException

from src.settings import Settings
from src.type_procedure.model import (
    TypeProcedure,
    TypeProcedureCreate,
    TypeProcedureDelete,
    TypeProcedureGet,
)
from src.transaction import TransactionCreated
from src.web3_manager import Web3Manager


class TypeManager:

    w3_manager: Web3Manager
    type_contract: Contract

    def __init__(self, w3_manager: Web3Manager) -> None:
        self.w3_manager = w3_manager
        self.type_contract = w3_manager.get_contract(
            address=Settings.type_contract_address, info=Settings.type_contract_info
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
                "gas": Settings.type_register_gas,
                "gasPrice": self.w3_manager.to_wey(
                    Settings.type_register_price_per_gas
                ),
            }  # type: ignore
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

    def get_type_procedure(self, get_dto: TypeProcedureGet) -> TypeProcedure:
        type_procedure_tuple = self.type_contract.functions.getTipo(get_dto.id).call()
        return TypeProcedure(
            id=get_dto.id,
            tipo=type_procedure_tuple[1],
            categoria_profissional_id=type_procedure_tuple[2],
        )

    def delete_type_procedure(
        self, delete_dto: TypeProcedureDelete
    ) -> TransactionCreated:
        nonce = self.w3_manager.get_transaction_count()

        transaction = self.type_contract.functions.deleteTipo(
            delete_dto.id,
        ).build_transaction(
            {
                "nonce": nonce,
                "gas": Settings.type_register_gas,
                "gasPrice": self.w3_manager.to_wey(
                    Settings.type_register_price_per_gas
                ),
            }  # type: ignore
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

    def verify_existence_type_procedure(self, get_dto: TypeProcedureGet) -> bool:
        type_procedure_tuple = self.type_contract.functions.verificarTipoProcedimento(
            get_dto.id
        ).call()
        return type_procedure_tuple[0]
