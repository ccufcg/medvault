# MedVault Profissionais Web3 Interface

This directory contains a complete Python Web3 interface for interacting with the ProfissionalManager smart contract. The interface provides both a direct Python API and a FastAPI web service for managing healthcare professionals on the blockchain.

## Features

- **Complete Contract Integration**: All contract functions are implemented
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Transaction Management**: Send transactions and track receipts
- **Event Monitoring**: Listen to contract events
- **REST API**: FastAPI endpoints for web integration
- **Configuration Management**: Environment-based configuration

## Files Overview

- `web3_interface.py` - Main Web3 interface class
- `contract_abi.py` - Contract ABI definition
- `config.py` - Configuration management
- `app.py` - FastAPI application with Web3 endpoints
- `example_usage.py` - Usage examples
- `requirements.txt` - Python dependencies

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the same directory:

```bash
python config.py
```

This will create a `.env` file with default values. Update it with your actual configuration:

```env
# Blockchain Configuration
RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=0xYourContractAddress
PRIVATE_KEY=0xYourPrivateKey

# Gas settings
GAS_LIMIT=300000
GAS_PRICE_MULTIPLIER=1.1

# Network settings
CHAIN_ID=1337

# Optional: Enable debug logging
DEBUG=false
```

### 3. Deploy Contract

Make sure you have deployed the ProfissionalManager contract and updated the `CONTRACT_ADDRESS` in your `.env` file.

## Usage

### Direct Python Interface

```python
from web3_interface import ProfissionalManagerInterface
from config import Config

# Initialize interface
interface = ProfissionalManagerInterface(**Config.get_web3_config())

# Create a new professional
tx_hash, profissional = interface.novo_profissional(
    wallet="0x1234567890123456789012345678901234567890",
    id_legado=12345,
    nome="Dr. Example",
    categoria=0,  # 0=Medico, 1=Enfermeiro
    registro="CRM123456",
    ativo=True
)

# Get professional information
profissional = interface.get_profissional("0x1234567890123456789012345678901234567890")

# Check if professional is active
is_ativo = interface.is_profissional_ativo("0x1234567890123456789012345678901234567890")

# Activate/deactivate professional
tx_hash = interface.ativar_profissional("0x1234567890123456789012345678901234567890")
tx_hash = interface.desativar_profissional("0x1234567890123456789012345678901234567890")

# Get professionals by category
medicos = interface.get_profissionais_por_categoria(0, only_active=True)
enfermeiros = interface.get_profissionais_por_categoria(1, only_active=True)
```

### FastAPI Web Service

Start the web service:

```bash
python app.py
```

The service will be available at `http://localhost:8000`

#### API Endpoints

**Professional Management:**
- `POST /api/profissionais` - Create new professional
- `GET /api/profissionais/{wallet}` - Get professional info
- `GET /api/profissionais/{wallet}/ativo` - Check if active
- `POST /api/profissionais/{wallet}/ativar` - Activate professional
- `POST /api/profissionais/{wallet}/desativar` - Deactivate professional
- `GET /api/profissionais/{wallet}/procedimentos` - Get procedures
- `GET /api/profissionais/categoria/{categoria}` - Get by category

**Blockchain Operations:**
- `GET /api/blockchain/status` - Check connection status
- `GET /api/transactions/{tx_hash}` - Get transaction receipt
- `GET /api/events/latest` - Get latest events

**System:**
- `GET /api/info` - API information
- `GET /health` - Health check

#### Example API Usage

**Create Professional:**
```bash
curl -X POST "http://localhost:8000/api/profissionais" \
  -H "Content-Type: application/json" \
  -d '{
    "wallet": "0x1234567890123456789012345678901234567890",
    "id_legado": 12345,
    "nome": "Dr. Example",
    "categoria": 0,
    "registro": "CRM123456",
    "ativo": true
  }'
```

**Get Professional:**
```bash
curl "http://localhost:8000/api/profissionais/0x1234567890123456789012345678901234567890"
```

**Check Blockchain Status:**
```bash
curl "http://localhost:8000/api/blockchain/status"
```

## Contract Functions

The interface implements all functions from the ProfissionalManager contract:

### Admin Functions (require private key)
- `novo_profissional()` - Register new professional
- `ativar_profissional()` - Activate professional
- `desativar_profissional()` - Deactivate professional

### View Functions (read-only)
- `get_profissional()` - Get professional information
- `is_profissional_ativo()` - Check if professional is active
- `verificar_profissional()` - Verify professional (alias)
- `get_procedimentos_do_profissional()` - Get associated procedures
- `get_profissionais_por_categoria()` - Get professionals by category

### Utility Functions
- `get_transaction_receipt()` - Get transaction receipt
- `wait_for_transaction()` - Wait for transaction confirmation
- `get_contract_events()` - Get contract events
- `get_latest_profissional_events()` - Get recent events

## Error Handling

The interface provides comprehensive error handling:

```python
from web3_interface import ContractError

try:
    profissional = interface.get_profissional("0xInvalidAddress")
except ContractError as e:
    print(f"Contract error: {e.message}")
    print(f"Error type: {e.error_type}")
```

## Categories

- `0` - Medico (Doctor)
- `1` - Enfermeiro (Nurse)

Use helper functions:
```python
from web3_interface import get_categoria_name, get_categoria_number

categoria_name = get_categoria_name(0)  # "Medico"
categoria_number = get_categoria_number("medico")  # 0
```

## Events

The contract emits the following events:
- `ProfissionalCadastrado` - When a new professional is registered
- `ProfissionalAtivado` - When a professional is activated
- `ProfissionalDesativado` - When a professional is deactivated

## Security Notes

- Keep your private key secure and never commit it to version control
- Use environment variables for sensitive configuration
- In production, use proper key management solutions
- Validate all inputs before sending transactions
- Monitor gas prices and set appropriate limits

## Troubleshooting

### Common Issues

1. **Connection Error**: Check your RPC URL and ensure the node is running
2. **Contract Not Found**: Verify the contract address is correct
3. **Transaction Failed**: Check gas limits and account balance
4. **Permission Denied**: Ensure you're using the admin private key

### Debug Mode

Enable debug mode in your `.env` file:
```env
DEBUG=true
```

This will provide more detailed logging information.

## Example Script

Run the example script to test the interface:

```bash
python example_usage.py
```

This will demonstrate all the main functionality and help you verify your setup.
