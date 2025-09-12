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
        _grantRole(MEDICO_ROLE, msg.sender);// Para fins de teste de funcionamento dos métodos
    }

    struct Procedimento {
        // Importar procedimentos depois
        string nome;
    }

    struct Paciente {
        uint256 id;
        address idMedico;
        string nome;
        uint256 dataNascimento;
        bool pacienteAtivo;
    }

    mapping(uint256 => Paciente) public pacientes;
    mapping(uint256 => address[]) private pacienteWallets; // Comentário: New mapping to store all wallets for a patient
    mapping(address => uint256) private walletToPacienteId;
    mapping(uint256 => bytes32[]) private pacienteProcedimentos;

    uint256 private idCounter;

    event PacienteRegistrado(uint256 indexed id, address indexed walletId);
    event PacienteDesativado(uint256 indexed id);
    event PacienteAtualizado(uint256 indexed id, address novoMedico);
    event WalletAssociada(uint256 indexed id, address wallet);
    event ProcedimentoRegistrado(uint256 indexed idPaciente, bytes32 procedimentoId);
    event NotificacaoMedico(uint256 indexed idPaciente, string motivo);

    modifier onlyDiretorMedico() {
        require(hasRole(DIRETOR_ROLE, msg.sender), "Nao autorizado, apenas o Diretor pode realizar essa operacao");
        _;
    }

    modifier onlyMedico() {
        require(hasRole(MEDICO_ROLE, msg.sender), "Nao autorizado, apenas o Medico pode realizar essa operacao");
        _;
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
        pacienteWallets[idCounter].push(walletId); // Comentário: Now populating the new mapping.

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

    function existePaciente(address _wallet) public view override returns (bool) {
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
        pacienteWallets[_pacienteId].push(novaWallet); // Comentário: Now populating the new mapping.

        emit WalletAssociada(_pacienteId, novaWallet);
    }

    function removerWallet(address _wallet) public onlyDiretorMedico {
        uint256 pacienteId = walletToPacienteId[_wallet];
        require(pacienteId != 0, "Wallet nao associada a nenhum paciente");
        
        // Comentário: Lógica para remover a wallet do array `pacienteWallets`
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

        // Comentário: Remove a associação da wallet para o ID
        delete walletToPacienteId[_wallet];
    }

    function listarWallets(uint256 _pacienteId) public view onlyDiretorMedico returns (address[] memory) {
        require(_pacienteId > 0 && pacientes[_pacienteId].id != 0, "Paciente nao existe");
        return pacienteWallets[_pacienteId];
    }
}