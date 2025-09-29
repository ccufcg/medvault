// SPDX-License-Identifier: MIT
pragma solidity >=0.4.0 <0.9.0;

import "dapp/pacientes/IPacientes.sol";

contract PacientesNoAccessControl is IPacientesFull {

    address private owner;
    address public diretorMedico;
    mapping(address => bool) private medicos;

    mapping(uint256 => Paciente) public pacientes;
    mapping(uint256 => address[]) private pacienteWallets;
    mapping(address => uint256) private walletToPacienteId;
    mapping(uint256 => bytes32[]) private pacienteProcedimentos;
    
    uint256 private idCounter;

    modifier onlyDiretorMedico() {
        require(msg.sender == diretorMedico, "Nao autorizado, apenas o Diretor pode realizar essa operacao");
        _;
    }

    modifier onlyMedico() {
        require(medicos[msg.sender] || msg.sender == diretorMedico, "Nao autorizado, apenas o Medico pode realizar essa operacao");
        _;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function.");
        _;
    }

    constructor(address _diretorMedico) {
        owner = msg.sender;
        diretorMedico = _diretorMedico;
        medicos[msg.sender] = true; // For testing purposes
    }

    function addMedico(address _medico) public onlyOwner {
        medicos[_medico] = true;
    }

    function removeMedico(address _medico) public onlyOwner {
        medicos[_medico] = false;
    }

    function registrarPacienteComWallet(address _wallet, string memory _nome, uint256 _dataNascimento) public onlyMedico {
        require(_wallet != address(0), "Wallet invalida");
        idCounter++;

        pacientes[idCounter] = Paciente({
        id: idCounter,
        idMedico: msg.sender,
        nome: _nome,
        dataNascimento: _dataNascimento,
        pacienteAtivo: true
        });

        walletToPacienteId[_wallet] = idCounter;
        pacienteWallets[idCounter].push(_wallet);

        emit PacienteRegistrado(idCounter, _wallet);
        emit WalletAssociada(idCounter, _wallet);
    }

    function registrarPaciente(string memory _nome, uint256 _dataNascimento) public onlyMedico {
        idCounter++;
        address walletId = address(uint160(uint256(keccak256(abi.encodePacked(msg.sender, idCounter, block.timestamp)))));

        pacientes[idCounter] = Paciente({
            id: idCounter,
            idMedico: msg.sender,
            nome: _nome,
            dataNascimento: _dataNascimento,
            pacienteAtivo: true
        });

        walletToPacienteId[walletId] = idCounter;
        pacienteWallets[idCounter].push(walletId);

        emit PacienteRegistrado(idCounter, walletId);
        emit WalletAssociada(idCounter, walletId);
    }

    function desativarPaciente(uint256 _pacienteId) public onlyDiretorMedico {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");
        
        pacientes[_pacienteId].pacienteAtivo = false;

        emit PacienteDesativado(_pacienteId);
    }

    function atualizarPaciente(uint256 _pacienteId, address _novoMedico) public onlyDiretorMedico {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");
        pacientes[_pacienteId].idMedico = _novoMedico;

        emit PacienteAtualizado(pacientes[_pacienteId].id, _novoMedico);
    }

    function notificarMedico(uint256 _pacienteId, string memory _motivo) public onlyDiretorMedico {
        emit NotificacaoMedico(_pacienteId, _motivo);
    }

    function existePaciente(address _wallet) public view returns (bool) {
        return walletToPacienteId[_wallet] != 0;
    }

    function getPaciente(address _wallet) public view onlyDiretorMedico returns (Paciente memory) {
        uint256 pacienteId = walletToPacienteId[_wallet];
        require(pacienteId != 0, "Paciente nao existe");
        return pacientes[pacienteId];
    }

    function registrarProcedimento(uint256 _pacienteId, bytes32 _procedimentoId) public onlyMedico {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");
        pacienteProcedimentos[_pacienteId].push(_procedimentoId);
        emit ProcedimentoRegistrado(_pacienteId, _procedimentoId);
    }

    function adicionarWallet(uint256 _pacienteId) public onlyDiretorMedico returns (address novaWallet) {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");

        novaWallet = address(uint160(uint256(keccak256(abi.encodePacked(
            block.timestamp,
            _pacienteId,
            pacientes[_pacienteId].idMedico
        )))));

        walletToPacienteId[novaWallet] = _pacienteId;
        pacienteWallets[_pacienteId].push(novaWallet);

        emit WalletAssociada(_pacienteId, novaWallet);
    }

    function removerWallet(address _wallet) public onlyDiretorMedico {
        uint256 pacienteId = walletToPacienteId[_wallet];
        require(pacienteId != 0, "Wallet nao associada a nenhum paciente");
        
        address[] storage wallets = pacienteWallets[pacienteId];
        uint256 length = wallets.length;
        bool found = false;
        for (uint256 i = 0; i < length; i++) {
            if (wallets[i] == _wallet) {
                wallets[i] = wallets[length - 1];
                wallets.pop();
                found = true;
                break;
            }
        }
        require(found, "Wallet nao associada a este paciente.");

        delete walletToPacienteId[_wallet];
    }

    function listarWallets(uint256 _pacienteId) public view onlyDiretorMedico returns (address[] memory) {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");
        return pacienteWallets[_pacienteId];
    }
}
