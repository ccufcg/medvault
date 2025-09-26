from pydantic import BaseModel

from typing import Literal, Any


class TransactionCreated(BaseModel):
    transaction_hash: str
    transaction_url: str
    transaction_logs_url: str


class TransactionGet(BaseModel):
    status: Literal["sucess", "error"]
    transaction_hash: str
    receipt: Any
