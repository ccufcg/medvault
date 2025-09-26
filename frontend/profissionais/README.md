## Modulo Profissionais de Saúde

This module provides a complete Web3 interface for managing healthcare professionals on the blockchain.

### Features

- **Smart Contract Integration**: Full integration with the ProfissionalManager Solidity contract
- **Python Web3 Interface**: Direct Python API for contract interaction
- **REST API**: FastAPI web service with comprehensive endpoints
- **Professional Management**: Create, read, update, and manage healthcare professionals
- **Category Support**: Support for Medicos (Doctors) and Enfermeiros (Nurses)
- **Event Monitoring**: Track contract events and transactions
- **Error Handling**: Comprehensive error handling with meaningful messages

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Configuration**:
   ```bash
   python config.py  # Creates .env file
   # Edit .env with your blockchain configuration
   ```

3. **Test Setup**:
   ```bash
   python test_setup.py
   ```

4. **Run Examples**:
   ```bash
   python example_usage.py
   ```

5. **Start Web Service**:
   ```bash
   python app.py
   ```

### Files

- `web3_interface.py` - Main Web3 interface class
- `contract_abi.py` - Contract ABI definition
- `config.py` - Configuration management
- `app.py` - FastAPI application with Web3 endpoints
- `example_usage.py` - Usage examples
- `test_setup.py` - Setup verification script
- `README_WEB3.md` - Detailed Web3 documentation

### API Endpoints

The FastAPI service provides these endpoints:

- `POST /api/profissionais` - Create new professional
- `GET /api/profissionais/{wallet}` - Get professional info
- `GET /api/profissionais/{wallet}/ativo` - Check if active
- `POST /api/profissionais/{wallet}/ativar` - Activate professional
- `POST /api/profissionais/{wallet}/desativar` - Deactivate professional
- `GET /api/profissionais/categoria/{categoria}` - Get by category
- `GET /api/blockchain/status` - Check blockchain connection
- `GET /api/events/latest` - Get latest events

### Contract Functions

All ProfissionalManager contract functions are implemented:

**Admin Functions** (require private key):
- `novo_profissional()` - Register new professional
- `ativar_profissional()` - Activate professional
- `desativar_profissional()` - Deactivate professional

**View Functions** (read-only):
- `get_profissional()` - Get professional information
- `is_profissional_ativo()` - Check if professional is active
- `get_procedimentos_do_profissional()` - Get associated procedures
- `get_profissionais_por_categoria()` - Get professionals by category

### Configuration

Create a `.env` file with:

```env
RPC_URL=http://localhost:8545
CONTRACT_ADDRESS=0xYourContractAddress
PRIVATE_KEY=0xYourPrivateKey
GAS_LIMIT=300000
CHAIN_ID=1337
```

### Categories

- `0` - Medico (Doctor)
- `1` - Enfermeiro (Nurse)

### Documentation

For detailed documentation, see `README_WEB3.md`.

