import os, json
from pathlib import Path
from web3 import Web3


RPC_URL      = os.getenv("RPC_URL", "http://127.0.0.1:8545")
PRIVATE_KEY  = "0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3"             # admin que fez o deploy
ADDR_ESTOQUE = "0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0" # endereço do contrato Estoque

if not PRIVATE_KEY or not ADDR_ESTOQUE:
    raise SystemExit("Defina PRIVATE_KEY e ADDR_ESTOQUE no .env")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
ACCOUNT = w3.eth.account.from_key(PRIVATE_KEY)

# Caminho da ABI (relativo a este arquivo)
with open("estoque/config/contrato_estoque.idl") as f:
    abi_estoque = json.load(f)

estoque = w3.eth.contract(address=ADDR_ESTOQUE, abi=abi_estoque)

# ---------- helpers ----------
def send_tx(fn):
    nonce = w3.eth.get_transaction_count(ACCOUNT.address)
    tx = fn.build_transaction({
        "from": ACCOUNT.address,
        "nonce": nonce,
        "gas": 600_000,
        "gasPrice": w3.eth.gas_price
    })
    signed = ACCOUNT.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

def has_view(name):
    try:
        estoque.get_function_by_name(name)
        return True
    except ValueError:
        return False

# Descobre tipo do parâmetro "categoria" em addItem (string ou uint)
def categoria_param_type():
    fns = estoque.get_function_by_name("addItem")
    if not fns:
        raise RuntimeError("Função addItem não encontrada na ABI do Estoque.")
    add_item_abi = fns[0].abi
    # tenta localizar pelo nome do input
    idx = None
    for i, inp in enumerate(add_item_abi["inputs"]):
        if inp.get("name", "").lower() == "categoria":
            idx = i
            break
    if idx is None:
        # fallback: assume 3º argumento (id, lote, categoria, ...)
        idx = 2
    return add_item_abi["inputs"][idx]["type"]

CAT_PARAM_TYPE = categoria_param_type()

# Se o contrato tiver mapping publico categoriaValida(string) -> bool, usamos para evitar revert
HAS_CATEGORIA_VALIDA = has_view("categoriaValida")

# Mapeamento default caso addItem espere enum/uint
ENUM_INDEX = {
    "Antibiotico": 0,
    "Sutura": 1,
    "Anestesia": 2,
    "Vacina": 3,
    "Material Cirurgico": 4,
}

def ensure_categoria(nome: str):
    """Chama addCategoria(nome) se disponível e se ainda não existir."""
    # Se existir view categoriaValida(string) -> bool, checamos antes
    precisa_criar = True
    if HAS_CATEGORIA_VALIDA:
        try:
            if estoque.functions.categoriaValida(nome).call():
                precisa_criar = False
        except Exception:
            pass
    if precisa_criar:
        try:
            rc = send_tx(estoque.functions.addCategoria(nome))
            print(f"[OK] Categoria '{nome}' criada. tx={rc.transactionHash.hex()}")
        except Exception as e:
            # Se já existir, o require vai reverter; apenas avisa e segue
            print(f"[!] addCategoria('{nome}') falhou/ja existe: {e}")

def categoria_argumento(nome: str):
    """Converte a categoria para o tipo esperado por addItem."""
    if CAT_PARAM_TYPE.startswith("uint"):
        # contrato usa enum/uint
        if nome not in ENUM_INDEX:
            raise ValueError(f"Categoria '{nome}' não mapeada para enum.")
        return int(ENUM_INDEX[nome])
    # caso contrário, espera string
    return nome

# ---------- dados ----------
CATEGORIAS = [
    "Antibiotico",
    "Sutura",
    "Anestesia",
    "Vacina",
    "Material Cirurgico",
]

ITENS = [
    {
        "idItemHospital": 101,
        "lote": "L001",
        "categoria": "Antibiotico",
        "dataValidade": 1893456000,  # 2030-01-01
        "altoCusto": False,
        "descricao": "Amoxicilina 500mg"
    },
    {
        "idItemHospital": 102,
        "lote": "L002",
        "categoria": "Vacina",
        "dataValidade": 1893456000,
        "altoCusto": True,
        "descricao": "Vacina XYZ"
    },
    {
        "idItemHospital": 103,
        "lote": "L003",
        "categoria": "Material Cirurgico",
        "dataValidade": 1767225600,  # 2026-01-01
        "altoCusto": False,
        "descricao": "Luvas cirúrgicas"
    },
    {
        "idItemHospital": 104,
        "lote": "L004",
        "categoria": "Sutura",
        "dataValidade": 1767225600,
        "altoCusto": False,
        "descricao": "Fio de sutura 3-0"
    },
    {
        "idItemHospital": 105,
        "lote": "L005",
        "categoria": "Anestesia",
        "dataValidade": 1780000000,
        "altoCusto": True,
        "descricao": "Anestésico premium 2%"
    },
]

# ---------- main ----------
def main():
    if not w3.is_connected():
        raise SystemExit(f"Não conectou em {RPC_URL}")

    print(f"Usando conta: {ACCOUNT.address}")
    print(f"Contrato Estoque: {ADDR_ESTOQUE}")
    print(f"addItem espera categoria como: {CAT_PARAM_TYPE}")

    # 1) cria categorias (string) antes
    for c in CATEGORIAS:
        ensure_categoria(c)

    # 2) adiciona itens
    for item in ITENS:
        cat_arg = categoria_argumento(item["categoria"])
        fn = estoque.functions.addItem(
            int(item["idItemHospital"]),
            item["lote"],
            cat_arg,
            int(item["dataValidade"]),
            bool(item["altoCusto"]),
            item["descricao"],
        )
        rc = send_tx(fn)
        print(f"[OK] {item['descricao']} cadastrado. tx={rc.transactionHash.hex()}")

if __name__ == "_main_":
    main()