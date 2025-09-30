from pydantic import BaseModel


class ProcedureCreate(BaseModel):
    id_paciente: str
    id_procedimento_anterior: int
    tipo_procedimento_id: int
    intercorrencia: bool


class MaterialUsed(BaseModel):
    estoque_id: int
    quantidade: int


class ProcedureAddMaterial(BaseModel):
    estoque_id: int
    quantidade: int
    id_procedimento: int


class Procedure(BaseModel):
    id: int
    id_paciente: str
    id_profissional: str
    id_procedimento_anterior: int
    materiais: MaterialUsed
    tipo: str
    intercorrencia: bool
