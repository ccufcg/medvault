from fastapi import FastAPI

from src.web3_manager import Web3Manager
from src.type_procedure.type_manager import TypeManager
from src.type_procedure.model import (
    TypeProcedure,
    TypeProcedureCreate,
    TypeProcedureDelete,
    TypeProcedureGet,
)
from src.transaction import TransactionCreated, TransactionGet

app = FastAPI()

web3_manager = Web3Manager()
type_manager = TypeManager(web3_manager)


@app.post("/type-procedure")
def post_type_procedure(
    type_procedure_create: TypeProcedureCreate,
) -> TransactionCreated:
    return type_manager.register_type_procedure(type_procedure_create)


@app.get("/type-procedure/{id}")
def get_type_procedure(id: int) -> TypeProcedure:
    return type_manager.get_type_procedure(id)


@app.delete("/type-procedure/{id}")
def delete_type_procedure(id: int) -> TransactionCreated:
    return type_manager.delete_type_procedure(id)


@app.get("/logs/{tx}")
def get_transaction_receipt(tx: str) -> TransactionGet:
    return web3_manager.get_transaction_receipt(tx)
