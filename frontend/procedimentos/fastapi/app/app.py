from fastapi import FastAPI

from src.web3.http import Web3Manager as Web3Http
from src.type_procedure.type_manager import TypeManager
from src.procedure.procedure_manager import ProcedureManager
from src.procedure.model import Procedure, ProcedureAddMaterial, ProcedureCreate
from src.type_procedure.model import (
    TypeProcedure,
    TypeProcedureCreate,
)
from src.model import TransactionCreated, TransactionGet

app = FastAPI()

web3_manager = Web3Http()
type_manager = TypeManager(web3_manager)
procedure_manager = ProcedureManager(web3_manager)


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


@app.post("/procedure")
def post_procedure(procedure_dto: ProcedureCreate) -> TransactionCreated:
    return procedure_manager.register_procedure(procedure_dto)


@app.post("/procedure/material")
def post_procedure_material(material_dto: ProcedureAddMaterial) -> TransactionCreated:
    return procedure_manager.add_material(material_dto)


@app.get("/procedure/{id}")
def get_procedure(id: int) -> Procedure:
    return procedure_manager.get_procedure(id)


@app.websocket("/dashboard")
async def dashboard():
    return procedure_manager.dashboard()


@app.get("/logs/{tx}")
def get_transaction_receipt(tx: str) -> TransactionGet:
    return web3_manager.get_transaction_receipt(tx)
