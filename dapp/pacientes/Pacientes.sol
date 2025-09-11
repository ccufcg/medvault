// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/access/AccessControl.sol";

interface IPacientes {
    function existePaciente(address wallet) external view returns (bool);
}

contract Pacientes is AccessControl, IPacientes {

    bytes32 public constant DIRETOR_ROLE = keccak256("DIRETOR_ROLE");
    bytes32 public constant MEDICO_ROLE = keccak256("MEDICO_ROLE");

    constructor(address diretorMedico) {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(DIRETOR_ROLE, diretorMedico);
    }

    struct Procedimento {
    // Importar procedimento
        string nome;
    }

    struct Paciente {
        uint256 id;
        address idMedico;
        string nome;
        uint256 dataNascimento;
        bool pacienteAtivo;
    // Armazenar esses dois aqui é muito problemático pra função createPaciente() !!!
    // Procedimento[] procedimentos;
    // bytes32[] wallets; // Wallets são os mútiplos ids que teremos, logo, serão bytes32
    }


    mapping(address => Paciente) public pacientes;
    mapping(bytes32 => address) private idToPaciente;
    mapping(uint256 => address[]) private pacienteWallets;
    mapping(uint256 => bytes32[]) private pacienteProcedimentos;

    uint256 private idCounter;


    event PacienteRegistrado(uint256 indexed id, address indexed wallet);
    event PacienteDesativado(uint256 indexed id, address indexed wallet);
    event PacienteAtualizado(uint256 indexed id, address novoMedico);
    event WalletAssociada(uint256 indexed id, address wallet);
    event ProcedimentoRegistrado(uint256 indexed idPaciente, uint256 idProcedimento);
    event Reidentificacao(address diretor, address wallet, uint256 idPaciente);
    event NotificacaoMedico(uint256 indexed idPaciente, string motivo);

    modifier onlyDiretorMedico() {
        require(hasRole(DIRETOR_ROLE, msg.sender), "Nao autorizado apenas o Diretor pode realizar essa operacao");
        _;
    }

    modifier onlyMedico() {
        require(hasRole(MEDICO_ROLE, msg.sender), "Nao autorizado apenas o Medico pode realizar essa operacao");
        _;
    }

    function createPaciente(string memory _nome, uint256 _dataNascimento) public onlyMedico {
        idCounter++;
        address generatedId = address(uint160(uint256(keccak256(abi.encodePacked(msg.sender, idCounter, block.timestamp)))));

        pacientes[generatedId] = Paciente({
            id: idCounter,
            idMedico: msg.sender,
            nome: _nome,
            dataNascimento: _dataNascimento,
            pacienteAtivo: true
        });

        bytes32 pacienteKey = bytes32(uint256(uint160(generatedId)));
        idToPaciente[pacienteKey] = generatedId;
        pacienteWallets[idCounter].push(generatedId);

        emit PacienteRegistrado(idCounter, generatedId);
        emit WalletAssociada(idCounter, generatedId);
    }

    function desativarPaciente(bytes32 _id) public onlyDiretorMedico {
        address pacienteAddress = idToPaciente[_id];
        require(pacienteAddress != address(0), "Nao existe paciente com ID informado");
        pacientes[pacienteAddress].pacienteAtivo = false;

        emit PacienteDesativado(pacientes[pacienteAddress].id, pacienteAddress);
    }

    function atualizarPaciente(address _wallet, address _novoMedico) public onlyDiretorMedico {
        require(pacientes[_wallet].id != 0, "Paciente nao existe");
        pacientes[_wallet].idMedico = _novoMedico;

        emit PacienteAtualizado(pacientes[_wallet].id, _novoMedico);
    }

    function notificarMedico(uint256 pacienteId, string memory motivo) public onlyDiretorMedico {
        emit NotificacaoMedico(pacienteId, motivo);
    }


    function existePaciente(address wallet) public view override returns (bool) {
        return pacientes[wallet].id != 0;
    }

    function getPaciente(address wallet) public view returns (Paciente memory) {
        require(existePaciente(wallet), "Paciente nao existe");
        return pacientes[wallet];
    }

    function registrarProcedimento(uint256 pacienteId, bytes32 procedimentoId) public onlyMedico {
        pacienteProcedimentos[pacienteId].push(procedimentoId);
        emit ProcedimentoRegistrado(pacienteId, uint256(procedimentoId));
    }

}
