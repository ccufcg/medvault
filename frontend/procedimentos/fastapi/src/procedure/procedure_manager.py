from web3.contract import Contract

from eth_typing import Address
from fastapi.exceptions import HTTPException

from src.settings import Settings
from src.procedure.model import Procedure, ProcedureCreate, ProcedureAddMaterial
from src.model import TransactionCreated
from src.web3.http import Web3Manager


class ProcedureManager:

    w3_manager: Web3Manager
    procedure_contract: Contract
    admin_address: Address

    def __init__(self, w3_manager: Web3Manager) -> None:
        self.w3_manager = w3_manager
        address = self.w3_manager.checksun_address(Settings.procedure_contract_address)
        self.admin_address = self.w3_manager.checksun_address(Settings.admin_address)  # type: ignore
        self.procedure_contract = w3_manager.get_contract(
            address=address, info=Settings.type_contract_info
        )

    def register_procedure(self, register_dto: ProcedureCreate) -> TransactionCreated:

        nonce = self.w3_manager.get_transaction_count()

        transaction = self.procedure_contract.functions.cadastrarProcedimento(
            register_dto.id_paciente,
            register_dto.id_procedimento_anterior,
            register_dto.tipo_procedimento_id,
            register_dto.intercorrencia,
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

    def get_procedure(self, id: int) -> Procedure:
        procedure_tuple = self.procedure_contract.functions.getTipo(id).call()
        return Procedure(
            id=id,
            id_paciente=procedure_tuple[1],
            id_profissional=procedure_tuple[2],
            id_procedimento_anterior=procedure_tuple[3],
            materiais=procedure_tuple[4],
            tipo=procedure_tuple[5],
            intercorrencia=procedure_tuple[6],
        )

    def add_material(self, material_dto: ProcedureAddMaterial) -> TransactionCreated:

        nonce = self.w3_manager.get_transaction_count()

        transaction = self.procedure_contract.functions.adicionaMaterial(
            material_dto.id_procedimento,
            material_dto.estoque_id,
            material_dto.quantidade,
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
