"""
Configuration settings for the ProfissionalManager Web3 interface.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for blockchain connection settings."""
    
    # Blockchain connection settings
    RPC_URL: str = os.getenv("RPC_URL", "http://localhost:8545")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")
    PRIVATE_KEY: Optional[str] = os.getenv("PRIVATE_KEY")
    
    # Gas settings
    GAS_LIMIT: int = int(os.getenv("GAS_LIMIT", "300000"))
    GAS_PRICE_MULTIPLIER: float = float(os.getenv("GAS_PRICE_MULTIPLIER", "1.1"))
    
    # Network settings
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", "1337"))
    
    # Debug settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        cls.RPC_URL = "https://sepolia.drpc.org"
        cls.CONTRACT_ADDRESS = "0x42699A7612A82f1d9C36148af9C77354759b210b"
        cls.PRIVATE_KEY = "0x5f874c8d056f19746b456a5046724e00b909e23560b5c540812a35701a9690b0"
        cls.GAS_LIMIT = 300000
        cls.GAS_PRICE_MULTIPLIER = 1.1
        cls.CHAIN_ID = 11155111
        cls.DEBUG = True
        
        if not cls.CONTRACT_ADDRESS:
            raise ValueError("CONTRACT_ADDRESS is required")
        
        if not cls.PRIVATE_KEY:
            raise ValueError("PRIVATE_KEY is required for admin operations")
        
        return True
    
    @classmethod
    def get_web3_config(cls) -> dict:
        """Get configuration for Web3 interface initialization."""
        return {
            "rpc_url": cls.RPC_URL,
            "contract_address": cls.CONTRACT_ADDRESS,
            "private_key": cls.PRIVATE_KEY
        }


DEFAULT_CONFIG = {
    "RPC_URL": "https://rpc.sepolia.dev",
    "CONTRACT_ADDRESS": "0x9D7f74d0C41E726EC95884E0e97Fa6129e3b5E99",
    "PRIVATE_KEY": "0x5B38Da6a701c568545dCfcB03FcB875f56beddC4",
    "GAS_LIMIT": 300000,
    "GAS_PRICE_MULTIPLIER": 1.1,
    "CHAIN_ID": 1337,
    "DEBUG": False
}


def create_env_file():
    """Create a .env file with default values."""
    env_content = """# Blockchain Configuration
# Update these values with your actual configuration

# Ethereum RPC URL (e.g., local Ganache, Infura, Alchemy, etc.)
RPC_URL=http://localhost:8545

# Contract address of the deployed ProfissionalManager contract
CONTRACT_ADDRESS=0x1234567890123456789012345678901234567890

# Private key for admin transactions (keep this secure!)
# This should be the private key of the contract owner/admin
PRIVATE_KEY=0x1234567890123456789012345678901234567890123456789012345678901234

# Gas settings
GAS_LIMIT=300000
GAS_PRICE_MULTIPLIER=1.1

# Network settings
CHAIN_ID=1337  # Ganache default, change for other networks

# Optional: Enable debug logging
DEBUG=false
"""
    
    env_file_path = os.path.join(os.path.dirname(__file__), ".env")
    
    if not os.path.exists(env_file_path):
        with open(env_file_path, "w") as f:
            f.write(env_content)
        print(f"Created .env file at {env_file_path}")
        print("Please update the values in .env with your actual configuration")
    else:
        print(f".env file already exists at {env_file_path}")


if __name__ == "__main__":
    create_env_file()
