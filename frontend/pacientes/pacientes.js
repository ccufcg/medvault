let web3, contract, accounts;
let pacientesOffchain = JSON.parse(localStorage.getItem("pacientes")) || {};

(async () => {
  const config = await loadConfig();
  web3 = await initWeb3();
  accounts = await web3.eth.getAccounts();
  contract = await loadContract(web3, config, "Pacientes");
})();

async function loadConfig() {
  const response = await fetch("config.json");
  return response.json();
}

async function initWeb3() {
  if (window.ethereum) {
    const web3 = new Web3(window.ethereum);
    await window.ethereum.request({ method: "eth_requestAccounts" });
    return web3;
  } else {
    alert("MetaMask não detectado!");
    throw new Error("MetaMask não encontrado");
  }
}

async function loadContract(web3, config, name) {
  const contractConfig = config.contracts[name];
  const abi = await (await fetch(contractConfig.abiFile)).json();
  return new web3.eth.Contract(abi, contractConfig.address);
}

function salvarPacienteOffchain(cpf, nome, wallet) {
  if (!pacientesOffchain[cpf]) {
    pacientesOffchain[cpf] = [];
  }
  pacientesOffchain[cpf].push({ nome, wallet });
  localStorage.setItem("pacientes", JSON.stringify(pacientesOffchain));
}

async function cadastrarPaciente() {
  const nome = document.getElementById("cadNome").value;
  const cpf = document.getElementById("cadCpf").value;

  if (!nome || !cpf) {
    alert("Preencha todos os campos!");
    return;
  }
  const newWallet = web3.eth.accounts.create();

  try {
    await contract.methods
      .registrarPacienteComWallet(newWallet.address, nome, Date.now())
      .send({ from: accounts[0] });

    salvarPacienteOffchain(cpf, nome, newWallet.address);

    document.getElementById(
      "cadOutput"
    ).textContent = `Paciente registrado com wallet: ${newWallet.address}`;

    document.getElementById("qrcode").innerHTML = "";
    new QRCode(document.getElementById("qrcode"), newWallet.address);
  } catch (err) {
    alert(err.message);
  }
}

function consultarPorWallet() {
  const wallet = document.getElementById("consultaWallet").value;
  let resultado = null;
  for (const cpf in pacientesOffchain) {
    for (const p of pacientesOffchain[cpf]) {
      if (p.wallet === wallet) {
        resultado = { nome: p.nome, cpf, wallet };
      }
    }
  }
  document.getElementById("consultaWalletOut").textContent = resultado
    ? JSON.stringify(resultado, null, 2)
    : "Não encontrado";
}

function consultarPorCpf() {
  const cpf = document.getElementById("consultaCpf").value;
  const resultado = pacientesOffchain[cpf] || [];
  document.getElementById("consultaCpfOut").textContent =
    resultado.length > 0
      ? JSON.stringify(resultado, null, 2)
      : "Nenhuma wallet registrada";
}
