"""
Web3 interface for interacting with the ProfissionalManager contract.
This module provides a Python interface to interact with the Solidity contract.
"""

import os
from typing import Dict, List, Optional, Tuple, Any
from web3 import Web3
from web3.exceptions import ContractLogicError, TransactionNotFound
from pydantic import BaseModel, Field
from contract_abi import PROFISSIONAL_MANAGER_ABI, CATEGORIA_MEDICO, CATEGORIA_ENFERMEIRO, ERROR_SELECTORS


class ProfissionalData(BaseModel):
    """Data model for a professional."""
    wallet: str = Field(..., description="Wallet address of the professional")
    id_legado: int = Field(..., description="Legacy ID of the professional")
    nome: str = Field(..., description="Name of the professional")
    categoria: int = Field(..., description="Category (0=Medico, 1=Enfermeiro)")
    registro: str = Field(..., description="Professional registration number")
    ativo: bool = Field(..., description="Whether the professional is active")


class ContractError(Exception):
    """Custom exception for contract-related errors."""
    def __init__(self, message: str, error_type: str = None):
        self.message = message
        self.error_type = error_type
        super().__init__(self.message)


class ProfissionalManagerInterface:
    """
    Interface for interacting with the ProfissionalManager contract.
    """
    
    def __init__(self, rpc_url: str, contract_address: str, private_key: str = None):
        """
        Initialize the Web3 interface.
        
        Args:
            rpc_url: Ethereum RPC URL (e.g., 'http://localhost:8545')
            contract_address: Address of the deployed ProfissionalManager contract
            private_key: Private key for transactions (optional, for read-only operations)
        """
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not self.w3.is_connected():
            raise ContractError("Failed to connect to Ethereum node")
        
        self.contract_address = Web3.to_checksum_address(contract_address)
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=PROFISSIONAL_MANAGER_ABI
        )
        
        self.private_key = private_key
        if private_key:
            self.account = self.w3.eth.account.from_key(private_key)
            self.default_account = self.account.address
        else:
            self.account = None
            self.default_account = None
    
    def _handle_contract_error(self, error: Exception) -> ContractError:
        """Handle contract errors and convert them to meaningful messages."""
        if isinstance(error, ContractLogicError):
            error_data = error.args[0]
            if isinstance(error_data, dict) and 'message' in error_data:
                message = error_data['message']
                # Try to identify the specific error type
                for error_name, selector in ERROR_SELECTORS.items():
                    if selector in message:
                        return ContractError(f"Contract error: {error_name}", error_name)
                return ContractError(f"Contract error: {message}")
            return ContractError(f"Contract logic error: {str(error)}")
        return ContractError(f"Transaction error: {str(error)}")
    
    def _send_transaction(self, function_call, gas_limit: int = 300000) -> str:
        """Send a transaction and return the transaction hash."""
        if not self.account:
            raise ContractError("Private key required for transactions")
        
        try:
            # Build transaction
            transaction = function_call.build_transaction({
                'from': self.default_account,
                'gas': gas_limit,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': self.w3.eth.get_transaction_count(self.default_account)
            })
            
            # Sign and send transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            return tx_hash.hex()
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def _call_view_function(self, function_call) -> Any:
        """Call a view function and return the result."""
        try:
            return function_call.call()
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def novo_profissional(
        self,
        wallet: str,
        id_legado: int,
        nome: str,
        categoria: int,
        registro: str,
        ativo: bool = True
    ) -> Tuple[str, ProfissionalData]:
        """
        Register a new professional.
        
        Args:
            wallet: Wallet address of the professional
            id_legado: Legacy ID
            nome: Name of the professional
            categoria: Category (0=Medico, 1=Enfermeiro)
            registro: Professional registration number
            ativo: Whether the professional should be active
            
        Returns:
            Tuple of (transaction_hash, profissional_data)
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            print("ui")
            
            # Call the contract function
            function_call = self.contract.functions.novoProfissional(
                wallet_checksum,
                id_legado,
                nome,
                categoria,
                registro,
                ativo
            )
            
            tx_hash = self._send_transaction(function_call)
            
            # Get the returned professional data
            profissional_data = ProfissionalData(
                wallet=wallet_checksum,
                id_legado=id_legado,
                nome=nome,
                categoria=categoria,
                registro=registro,
                ativo=ativo
            )
            
            return tx_hash, profissional_data
            
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def get_profissional(self, wallet: str) -> ProfissionalData:
        """
        Get professional information by wallet address.

        Args:
            wallet: Wallet address of the professional

        Returns:
            ProfissionalData object

        Raises:
            ValueError: If the professional does not exist or the contract call reverts.
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            # result = self._call_view_function(
            #     self.contract.functions.getProfissional(wallet_checksum)
            # )

            result = self.contract.functions.getProfissional(wallet_checksum).call()

            # Defensive: If the contract returns default/empty values, treat as not found
            # This depends on your contract's behavior. If it reverts, the except will catch.
            if (
                not result
                or (isinstance(result, (list, tuple)) and len(result) >= 6 and not result[5])
                and all(
                    (not result[i] if isinstance(result[i], str) else result[i] in [0, False, None])
                    for i in range(1, 5)
                )
            ):
                raise ValueError(f"Profissional not found for wallet {wallet_checksum}")

            return ProfissionalData(
                wallet=result[0],
                id_legado=result[1],
                nome=result[2],
                categoria=result[3],
                registro=result[4],
                ativo=result[5]
            )

        except Exception as e:
            # Enhanced error detection for contract reverts
            error_message = str(e).lower()
            if any(keyword in error_message for keyword in ["revert", "profissionalnaocadastrado", "execution reverted"]):
                raise ValueError(
                    f"Profissional not found or contract reverted for wallet {wallet}. "
                    f"Check if the wallet is registered."
                ) from e
            
            # Check for specific contract errors
            if hasattr(e, "args") and e.args:
                error_data = e.args[0]
                if isinstance(error_data, dict) and 'message' in error_data:
                    message = error_data['message'].lower()
                    if "profissionalnaocadastrado" in message:
                        raise ValueError(
                            f"Profissional not found for wallet {wallet}. "
                            f"The wallet has not been registered yet."
                        ) from e
            
            raise self._handle_contract_error(e)
    
    def is_profissional_ativo(self, wallet: str) -> bool:
        """
        Check if a professional is active.
        
        Args:
            wallet: Wallet address of the professional
            
        Returns:
            True if professional is active, False otherwise
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            return self._call_view_function(
                self.contract.functions.isProfissionalAtivo(wallet_checksum)
            )
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def ativar_profissional(self, wallet: str) -> str:
        """
        Activate a professional.
        
        Args:
            wallet: Wallet address of the professional
            
        Returns:
            Transaction hash
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            function_call = self.contract.functions.ativarProfissional(wallet_checksum)
            return self._send_transaction(function_call)
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def desativar_profissional(self, wallet: str) -> str:
        """
        Deactivate a professional.
        
        Args:
            wallet: Wallet address of the professional
            
        Returns:
            Transaction hash
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            function_call = self.contract.functions.desativarProfissional(wallet_checksum)
            return self._send_transaction(function_call)
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def verificar_profissional(self, wallet: str) -> bool:
        """
        Verify if a professional is active (alias for is_profissional_ativo).
        
        Args:
            wallet: Wallet address of the professional
            
        Returns:
            True if professional is active, False otherwise
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            return self._call_view_function(
                self.contract.functions.verificarProfissional(wallet_checksum)
            )
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def get_procedimentos_do_profissional(self, wallet: str) -> List[int]:
        """
        Get procedures associated with a professional.
        
        Args:
            wallet: Wallet address of the professional
            
        Returns:
            List of procedure IDs
        """
        try:
            wallet_checksum = Web3.to_checksum_address(wallet)
            return self._call_view_function(
                self.contract.functions.getProcedimentosDoProfissional(wallet_checksum)
            )
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def get_profissionais_por_categoria(
        self,
        categoria: int,
        only_active: bool = True
    ) -> List[str]:
        """
        Get professionals by category.
        
        Args:
            categoria: Category (0=Medico, 1=Enfermeiro)
            only_active: Whether to return only active professionals
            
        Returns:
            List of wallet addresses
        """
        try:
            result = self._call_view_function(
                self.contract.functions.getProfissionaisPorCategoria(categoria, only_active)
            )
            return [Web3.to_checksum_address(addr) for addr in result]
        except Exception as e:
            raise self._handle_contract_error(e)
    
    def get_transaction_receipt(self, tx_hash: str) -> Dict:
        """
        Get transaction receipt.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Transaction receipt dictionary
        """
        try:
            return self.w3.eth.get_transaction_receipt(tx_hash)
        except TransactionNotFound:
            raise ContractError(f"Transaction not found: {tx_hash}")
        except Exception as e:
            raise ContractError(f"Error getting transaction receipt: {str(e)}")
    
    def wait_for_transaction(self, tx_hash: str, timeout: int = 300) -> Dict:
        """
        Wait for transaction to be mined and return receipt.
        
        Args:
            tx_hash: Transaction hash
            timeout: Timeout in seconds
            
        Returns:
            Transaction receipt dictionary
        """
        try:
            return self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        except Exception as e:
            raise ContractError(f"Error waiting for transaction: {str(e)}")
    
    def get_contract_events(self, event_name: str, from_block: int = 0, to_block: str = 'latest') -> List[Dict]:
        """
        Get contract events.
        
        Args:
            event_name: Name of the event
            from_block: Starting block number
            to_block: Ending block number or 'latest'
            
        Returns:
            List of event logs
        """
        try:
            event_filter = getattr(self.contract.events, event_name).create_filter(
                fromBlock=from_block,
                toBlock=to_block
            )
            return event_filter.get_all_entries()
        except Exception as e:
            raise ContractError(f"Error getting events: {str(e)}")
    
    def get_latest_profissional_events(self, limit: int = 10) -> List[Dict]:
        """
        Get latest professional-related events.
        
        Args:
            limit: Maximum number of events to return
            
        Returns:
            List of event logs
        """
        try:
            # Get the latest block
            latest_block = self.w3.eth.block_number
            
            # Get events from the last 1000 blocks (adjust as needed)
            from_block = max(0, latest_block - 1000)
            
            events = []
            
            # Get ProfissionalCadastrado events
            cadastrado_events = self.get_contract_events('ProfissionalCadastrado', from_block)
            events.extend(cadastrado_events)
            
            # Get ProfissionalAtivado events
            ativado_events = self.get_contract_events('ProfissionalAtivado', from_block)
            events.extend(ativado_events)
            
            # Get ProfissionalDesativado events
            desativado_events = self.get_contract_events('ProfissionalDesativado', from_block)
            events.extend(desativado_events)
            
            # Sort by block number and return the latest
            events.sort(key=lambda x: x['blockNumber'], reverse=True)
            return events[:limit]
            
        except Exception as e:
            raise ContractError(f"Error getting latest events: {str(e)}")


# Utility functions
def get_categoria_name(categoria: int) -> str:
    """Get category name from category number."""
    if categoria == CATEGORIA_MEDICO:
        return "Medico"
    elif categoria == CATEGORIA_ENFERMEIRO:
        return "Enfermeiro"
    else:
        return f"Unknown ({categoria})"


def get_categoria_number(categoria_name: str) -> int:
    """Get category number from category name."""
    categoria_name = categoria_name.lower()
    if categoria_name in ["medico", "médico", "doctor"]:
        return CATEGORIA_MEDICO
    elif categoria_name in ["enfermeiro", "nurse"]:
        return CATEGORIA_ENFERMEIRO
    else:
        raise ValueError(f"Unknown category: {categoria_name}")
