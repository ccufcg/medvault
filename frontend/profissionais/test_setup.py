"""
Test script to verify the Web3 interface setup.
This script checks if all dependencies are properly installed and configured.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import web3
        print(f"  ✓ web3 version: {web3.__version__}")
    except ImportError as e:
        print(f"  ❌ web3 import failed: {e}")
        return False
    
    try:
        import pydantic
        print(f"  ✓ pydantic version: {pydantic.__version__}")
    except ImportError as e:
        print(f"  ❌ pydantic import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("  ✓ python-dotenv imported successfully")
    except ImportError as e:
        print(f"  ❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from web3_interface import ProfissionalManagerInterface, ContractError
        print("  ✓ web3_interface imported successfully")
    except ImportError as e:
        print(f"  ❌ web3_interface import failed: {e}")
        return False
    
    try:
        from contract_abi import PROFISSIONAL_MANAGER_ABI
        print("  ✓ contract_abi imported successfully")
    except ImportError as e:
        print(f"  ❌ contract_abi import failed: {e}")
        return False
    
    try:
        from config import Config
        print("  ✓ config imported successfully")
    except ImportError as e:
        print(f"  ❌ config import failed: {e}")
        return False
    
    return True

def test_configuration():
    """Test configuration setup."""
    print("\nTesting configuration...")
    
    from config import Config
    
    # Check if .env file exists
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        print("  ✓ .env file exists")
    else:
        print("  ⚠ .env file not found - run 'python config.py' to create it")
        return False
    
    # Test configuration validation
    try:
        Config.validate()
        print("  ✓ Configuration validation passed")
        return True
    except ValueError as e:
        print(f"  ❌ Configuration validation failed: {e}")
        print("  Please update your .env file with correct values")
        return False

def test_web3_connection():
    """Test Web3 connection (if configured)."""
    print("\nTesting Web3 connection...")
    
    try:
        from config import Config
        Config.validate()
        
        from web3_interface import ProfissionalManagerInterface
        
        interface = ProfissionalManagerInterface(**Config.get_web3_config())
        
        # Test connection
        latest_block = interface.w3.eth.block_number
        print(f"  ✓ Connected to blockchain - Latest block: {latest_block}")
        print(f"  ✓ Contract address: {interface.contract_address}")
        print(f"  ✓ Admin account: {interface.default_account}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Web3 connection failed: {e}")
        print("  Please check your .env configuration and ensure:")
        print("    - Ethereum node is running")
        print("    - Contract is deployed")
        print("    - CONTRACT_ADDRESS is correct")
        print("    - PRIVATE_KEY is valid")
        return False

def main():
    """Main test function."""
    print("=== MedVault Profissionais Web3 Setup Test ===\n")
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test configuration
    if not test_configuration():
        all_passed = False
    
    # Test Web3 connection (only if configuration is valid)
    if all_passed:
        if not test_web3_connection():
            all_passed = False
    
    print("\n=== Test Results ===")
    if all_passed:
        print("✅ All tests passed! Your Web3 interface is ready to use.")
        print("\nNext steps:")
        print("1. Run 'python example_usage.py' to see usage examples")
        print("2. Start the web service with 'python app.py'")
        print("3. Visit http://localhost:8000/api/info for API documentation")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Create .env file: python config.py")
        print("3. Update .env with your blockchain configuration")
        print("4. Ensure your Ethereum node is running")
        print("5. Deploy the contract and update CONTRACT_ADDRESS")

if __name__ == "__main__":
    main()
