"""
Example usage of the ProfissionalManager Web3 interface.
This script demonstrates how to interact with the contract using Python Web3.
"""

import asyncio
from web3_interface import ProfissionalManagerInterface, ContractError, get_categoria_name, get_categoria_number
from config import Config


async def main():
    """Main example function."""
    print("=== MedVault Profissionais Web3 Interface Example ===\n")
    
    try:
        # Initialize the Web3 interface
        print("1. Initializing Web3 interface...")
        Config.validate()
        interface = ProfissionalManagerInterface(**Config.get_web3_config())
        print(f"   ✓ Connected to blockchain at {Config.RPC_URL}")
        print(f"   ✓ Contract address: {interface.contract_address}")
        print(f"   ✓ Admin account: {interface.default_account}")
        
        # Test blockchain connection
        print("\n2. Testing blockchain connection...")
        latest_block = interface.w3.eth.block_number
        print(f"   ✓ Latest block: {latest_block}")
        
        # Example wallet addresses (replace with actual addresses)
        example_wallet_1 = "0x1234567890123456789012345678901234567890"
        example_wallet_2 = "0x0987654321098765432109876543210987654321"
        
        print(f"\n3. Example operations with wallet: {example_wallet_1}")
        
        # Try to get professional (might fail if not registered)
        try:
            profissional = interface.get_profissional(example_wallet_1)
            print(f"   ✓ Professional found:")
            print(f"     - Name: {profissional.nome}")
            print(f"     - Category: {get_categoria_name(profissional.categoria)}")
            print(f"     - Active: {profissional.ativo}")
            print(f"     - Registration: {profissional.registro}")
        except ContractError as e:
            print(f"   ⚠ Professional not found: {e.message}")
        
        # Check if professional is active
        try:
            is_ativo = interface.is_profissional_ativo(example_wallet_1)
            print(f"   ✓ Professional active status: {is_ativo}")
        except ContractError as e:
            print(f"   ⚠ Could not check active status: {e.message}")
        
        # Get professionals by category
        print(f"\n4. Getting professionals by category...")
        for categoria in [0, 1]:  # Medico, Enfermeiro
            try:
                profissionais = interface.get_profissionais_por_categoria(categoria, only_active=True)
                print(f"   ✓ {get_categoria_name(categoria)} professionals (active): {len(profissionais)}")
                if profissionais:
                    print(f"     - Sample addresses: {profissionais[:3]}")
            except ContractError as e:
                print(f"   ⚠ Error getting {get_categoria_name(categoria)} professionals: {e.message}")
        
        # Get latest events
        print(f"\n5. Getting latest events...")
        try:
            events = interface.get_latest_profissional_events(limit=5)
            print(f"   ✓ Found {len(events)} recent events")
            for i, event in enumerate(events):
                print(f"     {i+1}. {event['event']} - Block {event['blockNumber']}")
        except ContractError as e:
            print(f"   ⚠ Error getting events: {e.message}")
        
        # Example of creating a new professional (commented out to avoid actual transactions)
        print(f"\n6. Example of creating a new professional (commented out):")
        print("   # Uncomment the following code to actually create a professional:")
        print("   # try:")
        print("   #     tx_hash, profissional = interface.novo_profissional(")
        print("   #         wallet='0xNewWalletAddress',")
        print("   #         id_legado=12345,")
        print("   #         nome='Dr. Example',")
        print("   #         categoria=get_categoria_number('medico'),")
        print("   #         registro='CRM123456',")
        print("   #         ativo=True")
        print("   #     )")
        print("   #     print(f'   ✓ Professional created with transaction: {tx_hash}')")
        print("   # except ContractError as e:")
        print("   #     print(f'   ⚠ Error creating professional: {e.message}')")
        
        print(f"\n=== Example completed successfully! ===")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nMake sure to:")
        print("1. Set up your .env file with correct configuration")
        print("2. Have a running Ethereum node (e.g., Ganache)")
        print("3. Deploy the ProfissionalManager contract")
        print("4. Update CONTRACT_ADDRESS in your .env file")


def demonstrate_api_endpoints():
    """Demonstrate how to use the API endpoints."""
    print("\n=== API Endpoints Usage Examples ===\n")
    
    print("1. Create a new professional:")
    print("   POST /api/profissionais")
    print("   Body: {")
    print('     "wallet": "0x1234...",')
    print('     "id_legado": 12345,')
    print('     "nome": "Dr. Example",')
    print('     "categoria": 0,')
    print('     "registro": "CRM123456",')
    print('     "ativo": true')
    print("   }")
    
    print("\n2. Get professional information:")
    print("   GET /api/profissionais/0x1234...")
    
    print("\n3. Check if professional is active:")
    print("   GET /api/profissionais/0x1234.../ativo")
    
    print("\n4. Activate a professional:")
    print("   POST /api/profissionais/0x1234.../ativar")
    
    print("\n5. Deactivate a professional:")
    print("   POST /api/profissionais/0x1234.../desativar")
    
    print("\n6. Get professionals by category:")
    print("   GET /api/profissionais/categoria/0?only_active=true")
    
    print("\n7. Get blockchain status:")
    print("   GET /api/blockchain/status")
    
    print("\n8. Get latest events:")
    print("   GET /api/events/latest?limit=10")


if __name__ == "__main__":
    print("MedVault Profissionais Web3 Interface")
    print("=====================================\n")
    
    print("Choose an option:")
    print("1. Run Web3 interface example")
    print("2. Show API endpoints examples")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(main())
    elif choice == "2":
        demonstrate_api_endpoints()
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")
