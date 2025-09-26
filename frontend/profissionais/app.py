from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
from pathlib import Path
from web3_interface import ProfissionalManagerInterface, ProfissionalData, ContractError
from config import Config

# Initialize FastAPI app
app = FastAPI(
    title="MedVault - Profissionais Frontend",
    description="Frontend interface for professional management system",
    version="1.0.0"
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

class ErrorResponse(BaseModel):
    error: str
    message: str
    error_type: Optional[str] = None

# Global Web3 interface instance
web3_interface: Optional[ProfissionalManagerInterface] = None

def get_web3_interface() -> ProfissionalManagerInterface:
    """Dependency to get Web3 interface instance."""
    global web3_interface
    if web3_interface is None:
        try:
            Config.validate()
            web3_interface = ProfissionalManagerInterface(**Config.get_web3_config())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize Web3 interface: {str(e)}")
    return web3_interface

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where this script is located
current_dir = Path(__file__).parent

# Web3 Contract API Endpoints
@app.post("/api/profissionais", response_model=TransactionResponse)
async def criar_profissional(
    request: NovoProfissionalRequest,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Create a new professional."""
    try:
        print("hi")
        tx_hash, profissional_data = interface.novo_profissional(
            wallet=request.wallet,
            id_legado=request.idLegado,
            nome=request.nome,
            categoria=request.categoria,
            registro=request.registro,
            ativo=request.ativo
        )
        return TransactionResponse(
            transaction_hash=tx_hash,
            message=f"Professional {request.nome} created successfully"
        )
    except ContractError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/profissionais/{wallet}", response_model=ProfissionalResponse)
async def obter_profissional(
    wallet: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get professional information by wallet address."""
    try:
        profissional = interface.get_profissional(wallet)
        return ProfissionalResponse(
            wallet=profissional.wallet,
            id_legado=profissional.id_legado,
            nome=profissional.nome,
            categoria=profissional.categoria,
            registro=profissional.registro,
            ativo=profissional.ativo
        )
    except ContractError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/profissionais/{wallet}/ativo")
async def verificar_profissional_ativo(
    wallet: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Check if a professional is active."""
    try:
        is_ativo = interface.is_profissional_ativo(wallet)
        return {"wallet": wallet, "ativo": is_ativo}
    except ContractError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/profissionais/{wallet}/ativar", response_model=TransactionResponse)
async def ativar_profissional(
    wallet: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Activate a professional."""
    try:
        tx_hash = interface.ativar_profissional(wallet)
        return TransactionResponse(
            transaction_hash=tx_hash,
            message=f"Professional {wallet} activated successfully"
        )
    except ContractError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/api/profissionais/{wallet}/desativar", response_model=TransactionResponse)
async def desativar_profissional(
    wallet: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Deactivate a professional."""
    try:
        tx_hash = interface.desativar_profissional(wallet)
        return TransactionResponse(
            transaction_hash=tx_hash,
            message=f"Professional {wallet} deactivated successfully"
        )
    except ContractError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/profissionais/{wallet}/procedimentos")
async def obter_procedimentos_profissional(
    wallet: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get procedures associated with a professional."""
    try:
        procedimentos = interface.get_procedimentos_do_profissional(wallet)
        return {"wallet": wallet, "procedimentos": procedimentos}
    except ContractError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/profissionais/categoria/{categoria}")
async def obter_profissionais_por_categoria(
    categoria: int,
    only_active: bool = True,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get professionals by category."""
    try:
        profissionais = interface.get_profissionais_por_categoria(categoria, only_active)
        return {
            "categoria": categoria,
            "only_active": only_active,
            "profissionais": profissionais,
            "count": len(profissionais)
        }
    except ContractError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/transactions/{tx_hash}")
async def obter_transacao(
    tx_hash: str,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get transaction receipt."""
    try:
        receipt = interface.get_transaction_receipt(tx_hash)
        return {
            "transaction_hash": tx_hash,
            "receipt": receipt
        }
    except ContractError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/events/latest")
async def obter_eventos_recentes(
    limit: int = 10,
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get latest professional-related events."""
    try:
        events = interface.get_latest_profissional_events(limit)
        return {
            "events": events,
            "count": len(events)
        }
    except ContractError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/blockchain/status")
async def status_blockchain(
    interface: ProfissionalManagerInterface = Depends(get_web3_interface)
):
    """Get blockchain connection status."""
    try:
        # Test connection
        latest_block = interface.w3.eth.block_number
        return {
            "connected": True,
            "latest_block": latest_block,
            "contract_address": interface.contract_address,
            "account": interface.default_account
        }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main HTML page."""
    html_file = current_dir / "index.html"
    if html_file.exists():
        return FileResponse(html_file)
    else:
        return HTMLResponse("<h1>File not found</h1><p>index.html not found in the current directory.</p>", status_code=404)

@app.get("/styles.css")
async def serve_styles():
    """Serve the CSS stylesheet."""
    css_file = current_dir / "styles.css"
    if css_file.exists():
        return FileResponse(css_file, media_type="text/css")
    else:
        return HTMLResponse("<h1>File not found</h1><p>styles.css not found in the current directory.</p>", status_code=404)

@app.get("/scripts.js")
async def serve_scripts():
    """Serve the JS script."""
    js_file = current_dir / "scripts.js"
    if js_file.exists():
        return FileResponse(js_file, media_type="application/javascript")
    else:
        return HTMLResponse("<h1>File not found</h1><p>scripts.js not found in the current directory.</p>", status_code=404)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Profissionais frontend is running"}

@app.get("/api/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "MedVault Profissionais Frontend",
        "version": "1.0.0",
        "description": "Frontend interface for professional management system with Web3 integration",
        "endpoints": {
            "main": "/",
            "styles": "/styles.css",
            "health": "/health",
            "info": "/api/info",
            "blockchain_status": "/api/blockchain/status",
            "profissionais": {
                "create": "POST /api/profissionais",
                "get": "GET /api/profissionais/{wallet}",
                "check_active": "GET /api/profissionais/{wallet}/ativo",
                "activate": "POST /api/profissionais/{wallet}/ativar",
                "deactivate": "POST /api/profissionais/{wallet}/desativar",
                "get_procedures": "GET /api/profissionais/{wallet}/procedimentos",
                "get_by_category": "GET /api/profissionais/categoria/{categoria}"
            },
            "transactions": {
                "get_receipt": "GET /api/transactions/{tx_hash}"
            },
            "events": {
                "get_latest": "GET /api/events/latest"
            }
        }
    }

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
        log_level="info"
    )
