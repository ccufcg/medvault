# frontend/estoque/popularEstoque.py
import os, json
from pathlib import Path
from web3 import Web3

RPC_URL = os.getenv("RPC_URL", "http://127.0.0.1:8545")
PRIVATE_KEY  = "0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"
ADDR_ESTOQUE = "0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0"

w3 = Web3(Web3.HTTPProvider(RPC_URL))
ACCOUNT = w3.eth.account.from_key(PRIVATE_KEY)

# Carregar ABI
with open("estoque/config/contrato_estoque.idl") as f:
    abi_estoque = json.load(f)

estoque = w3.eth.contract(address=ADDR_ESTOQUE, abi=abi_estoque)

def send_tx(fn):
    tx = fn.build_transaction({
        "from": ACCOUNT.address,
        "nonce": w3.eth.get_transaction_count(ACCOUNT.address),
        "gas": 600000,
        "gasPrice": w3.eth.gas_price
    })
    signed = ACCOUNT.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

# Categorias e itens
CATEGORIAS = ["Antibiotico", "Sutura", "Anestesia", "Vacina", "Material Cirurgico"]

ITENS = [
    (101, "L001", "Antibiotico", 1893456000, False, "Amoxicilina 500mg"),
    (102, "L002", "Vacina",      1893456000, True,  "Vacina XYZ"),
    (103, "L003", "Material Cirurgico", 1767225600, False, "Luvas cirúrgicas"),
    (104, "L004", "Sutura",      1767225600, False, "Fio de sutura 3-0"),
    (105, "L005", "Anestesia",   1780000000, True,  "Anestésico premium 2%"),
]

def main():
    print(">> Criando categorias...")
    for c in CATEGORIAS:
        try:
            send_tx(estoque.functions.addCategoria(c))
            print(f"[ok] Categoria {c}")
        except Exception as e:
            print(e)
            print(f"[skip] Categoria {c} já existe")

    print(">> Populando estoque...")
    for (idHosp, lote, cat, validade, alto, desc) in ITENS:
        try:
            rc = send_tx(
                estoque.functions.addItem(idHosp, lote, cat, validade, alto, desc)
            )
            print(f"[ok] {desc} cadastrado. tx={rc.transactionHash.hex()}")
        except Exception as e:
            print(f"[!] Erro em {desc}: {e}")

if __name__ == "__main__":
    main()