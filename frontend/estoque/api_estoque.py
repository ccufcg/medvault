from flask import Flask, request, jsonify, Blueprint
from web3 import Web3
import json, os

api_estoque = Blueprint("api_estoque",__name__)
w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL","http://127.0.0.1:8545")))

# Carregar ABI frontend\estoque\config
with open("estoque/config/contrato_estoque.idl") as f:
    abi_estoque = json.load(f)
with open("estoque/config/contrato_procedimento.idl") as f:
    abi_proc = json.load(f)

ADDR_ESTOQUE = os.getenv("0x8CdaF0CD259887258Bc13a92C0a6dA92698644C0")
ADDR_PROCED = os.getenv("0x345cA3e014Aaf5dcA488057592ee47305D9B3e10")
estoque = w3.eth.contract(address=ADDR_ESTOQUE, abi=abi_estoque)
proced = w3.eth.contract(address=ADDR_PROCED, abi=abi_proc)

def send_tx(contract_fn, private_key):
    #Assina e envia a transação usando a chave recebida na requisição
    account = w3.eth.account.from_key(private_key)
    tx = contract_fn.build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 500000,
        "gasPrice": w3.eth.gas_price
    })
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.rawTransaction)
    return w3.eth.wait_for_transaction_receipt(tx_hash)

@api_estoque.route("/api/itens", methods=["POST"])
def add_item():
    """
    POST /api/itens
    Headers:
        Authorization: Bearer <PRIVATE_KEY_HEX>
    Body JSON:
        {
          "idItemHospital": 101,
          "lote": "L001",
          "categoria": 0,
          "dataValidade": 1893456000,
          "altoCusto": false,
          "descricao": "Luvas descartáveis"
        }
    """
    # ----- Autenticação via header -----
    auth = request.headers.get("Authorization")
    if not auth or not auth.lower().startswith("bearer "):
        return {"error": "Authorization header ausente ou inválido"}, 401
    private_key = auth.split()[1].strip()
    print(private_key)
    data = request.get_json(force=True)
    campos = ["idItemHospital", "lote", "categoria",
              "dataValidade", "altoCusto", "descricao"]
    if not all(k in data for k in campos):
        return {"error": "Campos obrigatórios faltando"}, 400

    try:
        tx_receipt = send_tx(
            estoque.functions.addItem(
                int(data["idItemHospital"]),
                data["lote"],
                int(data["categoria"]),
                int(data["dataValidade"]),
                bool(data["altoCusto"]),
                data["descricao"]
            ),
            private_key
        )
        return {
            "status": "Item cadastrado",
            "txHash": tx_receipt.transactionHash.hex()
        }
    except Exception as e:
        return {"error": str(e)}, 500
@api_estoque.route("/", methods=["GET"])
def home():
    return jsonify({"msg": "ok"})

@api_estoque.route("/api/procedimentos/alto-custo", methods=["GET"])
def listar_proc_alto_custo():

    itens_alto = estoque.functions.listarItensAltoCusto().call()
    print(itens_alto)
    ids_alto = {item[0] for item in itens_alto}  # assume idHash no índice 0

    result = []
    proc_id = 1

    while True:
        try:
            # getProcedimento retorna (id, descricao, idsItens[])
            p = proced.functions.getProcedimento(proc_id).call()
        except Exception as e:
            # Qualquer outro erro encerra o loop de forma segura
            print(f"Erro ao buscar procedimento {proc_id}: {e}")
            break
        
        print(p)
        # p = (id, descricao, [idsItens])
        desc = p[1]
        itens_usados = p[2]
        usados_alto = [i for i in itens_usados if i in ids_alto]
        if usados_alto:
            result.append({
                "procedimentoId": proc_id,
                "descricao": desc,
                "itensAltoCustoUsados": usados_alto
            })

        proc_id += 1
    return jsonify(result)


if __name__ == "__main__":
    api_estoque.run(debug=True)