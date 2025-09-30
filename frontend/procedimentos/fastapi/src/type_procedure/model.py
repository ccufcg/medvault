from pydantic import BaseModel


class TypeProcedure(BaseModel):
    id: int
    tipo: str
    categoria_profissional_id: int


class TypeProcedureCreate(BaseModel):
    tipo: str
    categoria_profissional_id: int
