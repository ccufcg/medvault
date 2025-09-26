async function loadConfig() {
  const response = await fetch("config/default.json");
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
