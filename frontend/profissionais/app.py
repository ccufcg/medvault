from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from web3 import Web3
from contract import address, abi

w3 = Web3(Web3.HTTPProvider("https://sepolia.drpc.org"))
contract = w3.eth.contract(address=address, abi=abi)

# Initialize FastAPI app
app = FastAPI(
    title="MedVault - Profissionais Frontend",
    description="Frontend interface for professional management system",
    version="1.0.0",
)


# Pydantic models for API requests/responses
class NovoProfissionalRequest(BaseModel):
    wallet: str = Field(..., description="Wallet address of the professional")
    idLegado: int = Field(..., description="Legacy ID of the professional")
    nome: str = Field(..., description="Name of the professional")
    categoria: int = Field(..., description="Category (0=Medico, 1=Enfermeiro)")
    registro: str = Field(..., description="Professional registration number")
    ativo: bool = Field(True, description="Whether the professional should be active")


class ProfissionalResponse(BaseModel):
    wallet: str
    id_legado: int
    nome: str
    categoria: int
    registro: str
    ativo: bool


class TransactionResponse(BaseModel):
    transaction_hash: str
    message: str


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("index.html")


@app.get("/styles.css")
async def serve_styles():
    return FileResponse("styles.css", media_type="text/css")


@app.get("/scripts.js")
async def serve_scripts():
    return FileResponse("scripts.js", media_type="application/javascript")


@app.get("/api/profissionais")
async def get_all_profissionais():
    contract = w3.eth.contract(address=address, abi=abi)
    res = contract.functions.getAllProfissionais().call()

    return map(
        lambda p: ProfissionalResponse(
            wallet=p[0],
            id_legado=p[1],
            nome=p[2],
            categoria=p[3],
            registro=p[4],
            ativo=p[5],
        ),
        res,
    )


@app.get("/api/profissionais/{wallet}")
async def get_profissional(wallet: str):
    contract = w3.eth.contract(address=address, abi=abi)
    wallet = w3.to_checksum_address(wallet)
    res = contract.functions.getProfissional(wallet).call()
    return ProfissionalResponse(
        wallet=res[0],
        id_legado=res[1],
        nome=res[2],
        categoria=res[3],
        registro=res[4],
        ativo=res[5],
    )


@app.post("/api/profissionais", response_model=TransactionResponse)
async def criar_profissional(
    request: NovoProfissionalRequest,
):
    try:
        wallet_checksum = w3.to_checksum_address(request.wallet)

        transaction = contract.functions.novoProfissional(
            wallet=wallet_checksum,
            idLegado=request.idLegado,
            nome=request.nome,
            categoria=request.categoria,
            registro=request.registro,
            ativo=request.ativo,
        ).build_transaction(
            {
                "from": "0x5C8378C0Bc231553149266EED53C013170d0D9de",
                "gas": 300000,
                "gasPrice": w3.eth.gas_price,
                "nonce": w3.eth.get_transaction_count(
                    "0x5C8378C0Bc231553149266EED53C013170d0D9de"
                ),
            }
        )
        signed_txn = w3.eth.account.sign_transaction(
            transaction,
            "0x5f874c8d056f19746b456a5046724e00b909e23560b5c540812a35701a9690b0",
        )
        transaction_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

        return TransactionResponse(
            transaction_hash=transaction_hash.hex(),
            message="Profissional cadastrado. Consulte o estado no contrato para confirmação.",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    print("Starting MedVault Profissionais Frontend...")
    print("Available endpoints:")
    print("  - Main page: http://localhost:8000/")
    print("  - Styles: http://localhost:8000/styles.css")
    print("  - Health check: http://localhost:8000/health")
    print("  - API info: http://localhost:8000/api/info")
    print("\nPress Ctrl+C to stop the server")

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info",
    )
