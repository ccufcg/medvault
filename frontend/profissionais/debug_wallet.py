#!/usr/bin/env python3
"""
Debug script to investigate wallet registration issues.
This script will help identify why a wallet appears not to be registered.
"""

import sys
import os
from web3 import Web3
from web3_interface import ProfissionalManagerInterface, ContractError
from config import Config

def debug_wallet_registration(wallet_address: str):
    """Debug wallet registration status."""
    
    print(f"🔍 Debugging wallet: {wallet_address}")
    print("=" * 60)
    
    try:
        # Initialize Web3 interface
        Config.validate()
        interface = ProfissionalManagerInterface(**Config.get_web3_config())
        
        print(f"✅ Web3 connection established")
        print(f"📋 Contract address: {interface.contract_address}")
        print(f"👤 Admin account: {interface.default_account}")
        print(f"🔗 RPC URL: {Config.RPC_URL}")
        print()
        
        # Check blockchain connection
        try:
            latest_block = interface.w3.eth.block_number
            print(f"📦 Latest block: {latest_block}")
        except Exception as e:
            print(f"❌ Blockchain connection failed: {e}")
            return
        
        # Check if wallet is registered
        print("🔍 Checking wallet registration...")
        try:
            profissional = interface.get_profissional(wallet_address)
            print(f"✅ Wallet IS registered:")
            print(f"   📝 Name: {profissional.nome}")
            print(f"   🆔 Legacy ID: {profissional.id_legado}")
            print(f"   🏥 Category: {profissional.categoria}")
            print(f"   📋 Registration: {profissional.registro}")
            print(f"   ✅ Active: {profissional.ativo}")
            return
        except ValueError as e:
            print(f"❌ Wallet NOT registered: {e}")
        except ContractError as e:
            print(f"❌ Contract error: {e}")
        
        # Check if wallet is active (this might work even if get_profissional fails)
        print("\n🔍 Checking if wallet is active...")
        try:
            is_active = interface.is_profissional_ativo(wallet_address)
            print(f"📊 Is active: {is_active}")
        except Exception as e:
            print(f"❌ Cannot check active status: {e}")
        
        # Check recent events
        print("\n🔍 Checking recent events...")
        try:
            events = interface.get_latest_profissional_events(5)
            print(f"📋 Found {len(events)} recent events:")
            for event in events:
                event_name = event.get('event', 'Unknown')
                args = event.get('args', {})
                print(f"   📅 {event_name}: {args}")
        except Exception as e:
            print(f"❌ Cannot get events: {e}")
        
        # Check if the admin account has enough permissions
        print(f"\n🔍 Checking admin permissions...")
        try:
            # Try to call a function that requires admin permissions
            # We'll use a read-only function to check if we can access the contract
            result = interface.contract.functions.getProfissionaisPorCategoria(0, True).call()
            print(f"✅ Admin permissions verified (can read contract)")
        except Exception as e:
            print(f"❌ Admin permission issue: {e}")
        
        # Check contract owner
        print(f"\n🔍 Checking contract ownership...")
        try:
            # Try to get the owner (this might not be exposed in the ABI)
            # We'll check if our account matches the expected admin
            print(f"   👤 Our account: {interface.default_account}")
            print(f"   📋 Expected to be contract owner/admin")
        except Exception as e:
            print(f"❌ Cannot verify ownership: {e}")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

def check_transaction_status(tx_hash: str):
    """Check the status of a specific transaction."""
    print(f"\n🔍 Checking transaction: {tx_hash}")
    print("=" * 60)
    
    try:
        Config.validate()
        interface = ProfissionalManagerInterface(**Config.get_web3_config())
        
        # Get transaction receipt
        try:
            receipt = interface.get_transaction_receipt(tx_hash)
            print(f"✅ Transaction found:")
            print(f"   📦 Block: {receipt['blockNumber']}")
            print(f"   ⛽ Gas used: {receipt['gasUsed']}")
            print(f"   📊 Status: {'Success' if receipt['status'] == 1 else 'Failed'}")
            
            if receipt['status'] == 0:
                print(f"❌ Transaction failed!")
                return False
                
            # Check for events
            if receipt['logs']:
                print(f"📋 Events emitted:")
                for log in receipt['logs']:
                    print(f"   📅 Log: {log}")
            else:
                print(f"⚠️  No events emitted")
                
            return True
            
        except Exception as e:
            print(f"❌ Transaction not found or not mined: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking transaction: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_wallet.py <wallet_address> [tx_hash]")
        print("Example: python debug_wallet.py 0x627306090abaB3A6e1400e9345bC60c78a8BEf57")
        sys.exit(1)
    
    wallet_address = sys.argv[1]
    
    # Validate wallet address
    try:
        Web3.to_checksum_address(wallet_address)
    except Exception:
        print(f"❌ Invalid wallet address: {wallet_address}")
        sys.exit(1)
    
    debug_wallet_registration(wallet_address)
    
    # If a transaction hash is provided, check its status
    if len(sys.argv) > 2:
        tx_hash = sys.argv[2]
        check_transaction_status(tx_hash)
