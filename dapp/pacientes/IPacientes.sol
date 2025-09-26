// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IPacientesFull {

    struct Procedimento {
        string nome;
    }

    struct Paciente {
        uint256 id;
        address idMedico;
        string nome;
        uint256 dataNascimento;
        bool pacienteAtivo;
    }

    event PacienteRegistrado(uint256 indexed id, address indexed walletId);
    event PacienteDesativado(uint256 indexed id);
    event PacienteAtualizado(uint256 indexed id, address novoMedico);
    event WalletAssociada(uint256 indexed id, address wallet);
    event ProcedimentoRegistrado(uint256 indexed idPaciente, bytes32 procedimentoId);
    event NotificacaoMedico(uint256 indexed idPaciente, string motivo);

    function hasRole(bytes32 role, address account) external view returns (bool);
    function getRoleAdmin(bytes32 role) external view returns (bytes32);
    function grantRole(bytes32 role, address account) external;
    function revokeRole(bytes32 role, address account) external;
    function renounceRole(bytes32 role, address account) external;

    function registrarPaciente(string memory _nome, uint256 _dataNascimento) external;
    function registrarPacienteComWallet(address _wallet, string memory _nome, uint256 _dataNascimento) external;
    function desativarPaciente(uint256 _pacienteId) external;
    function atualizarPaciente(uint256 _pacienteId, address _novoMedico) external;
    function notificarMedico(uint256 _pacienteId, string memory _motivo) external;
    function existePaciente(address _wallet) external view returns (bool);
    function getPaciente(address _wallet) external view returns (Paciente memory);
    function registrarProcedimento(uint256 _pacienteId, bytes32 _procedimentoId) external;
    function adicionarWallet(uint256 _pacienteId) external returns (address novaWallet);
    function removerWallet(address _wallet) external;
    function listarWallets(uint256 _pacienteId) external view returns (address[] memory);
}
