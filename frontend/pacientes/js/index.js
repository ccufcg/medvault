let web3, contract, accounts;
let pacientesOffchain = JSON.parse(localStorage.getItem("pacientes")) || {};

(async () => {
  const config = await loadConfig();
  web3 = await initWeb3();
  accounts = await web3.eth.getAccounts();
  contract = await loadContract(web3, config, "Pacientes");
})();

function salvarPacienteOffchain(cpf, nome, wallet) {
  if (!pacientesOffchain[cpf]) pacientesOffchain[cpf] = [];
  pacientesOffchain[cpf].push({ nome, wallet });
  localStorage.setItem("pacientes", JSON.stringify(pacientesOffchain));
}

async function cadastrarPaciente() {
  console.log("Tentando registrar paciente...");

  const nomeInput = document.getElementById("cadNome");
  const cpfInput = document.getElementById("cadCpf");
  const errorNome = document.getElementById("errorNome");
  const errorCpf = document.getElementById("errorCpf");

  nomeInput.classList.remove("input-error");
  cpfInput.classList.remove("input-error");
  errorNome.textContent = "";
  errorCpf.textContent = "";

  const nome = nomeInput.value.trim();
  const cpf = cpfInput.value.trim();

  let valid = true;

  if (!nome) {
    nomeInput.classList.add("input-error");
    errorNome.textContent = "Campo obrigatório";
    valid = false;
  }

  if (!cpf) {
    cpfInput.classList.add("input-error");
    errorCpf.textContent = "Campo obrigatório";
    valid = false;
  }

  if (!valid) return;

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
    new QRCode(document.getElementById("qrcode"), {
      text: newWallet.address,
      width: 150,
      height: 150,
      colorDark: "#2c3e50",
      colorLight: "#ffffff",
      correctLevel: QRCode.CorrectLevel.H,
    });

    nomeInput.value = "";
    cpfInput.value = "";
  } catch (err) {
    console.log(err);
    alert("Erro ao registrar paciente: " + err.message);
  }
}

async function verificarDiretor() {
  const account = accounts[0] || "";
  return account.toLowerCase() === "0xfe3b557e8fb62b89f4916b721be55ceb828dbd73";
}

async function consultarPorWallet() {
  const wallet = document.getElementById("consultaWallet").value.trim();

  const isDiretor = await verificarDiretor();
  if (!isDiretor) {
    mostrarAlerta(
      "Acesso negado: somente o Diretor Médico pode consultar pacientes."
    );
    return;
  }

  let resultado = null;

  for (const cpf in pacientesOffchain) {
    for (const p of pacientesOffchain[cpf]) {
      if (p.wallet === wallet) {
        resultado = { nome: p.nome, cpf, wallet };
        break;
      }
    }
  }

  document.getElementById("consultaWalletOut").textContent = resultado
    ? JSON.stringify(resultado, null, 2)
    : "Não encontrado";
}

async function consultarPorCpf() {
  const cpf = document.getElementById("consultaCpf").value.trim();

  const isDiretor = await verificarDiretor();
  if (!isDiretor) {
    mostrarAlerta(
      "Acesso negado: somente o Diretor Médico pode listar wallets."
    );
    return;
  }

  const resultado = pacientesOffchain[cpf] || [];

  document.getElementById("consultaCpfOut").textContent =
    resultado.length > 0
      ? JSON.stringify(resultado, null, 2)
      : "Nenhuma wallet registrada";
}

function mostrarAlerta(mensagem) {
  document.getElementById("alertText").textContent = mensagem;
  document.getElementById("alertModal").style.display = "block";
}

function fecharModal() {
  document.getElementById("alertModal").style.display = "none";
}

window.cadastrarPaciente = cadastrarPaciente;
window.consultarPorWallet = consultarPorWallet;
window.consultarPorCpf = consultarPorCpf;
