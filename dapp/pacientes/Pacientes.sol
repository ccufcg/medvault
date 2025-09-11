// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IPacientes {
    function existePaciente(address wallet) external view returns (bool);
}

contract Pacientes {

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

    mapping(address => bytes32[]) private pacienteIdentificadores;
    mapping(address => Paciente) public pacientes;
    mapping(bytes32 => address) private idToPaciente;
    mapping(uint256 => address) private pacienteIdToAddress;


    uint256 private idCounter;


    event PacienteRegistrado(uint256 indexed id, address indexed wallet);
    event PacienteDesativado(uint256 indexed id, address indexed wallet);


    function createPaciente(string memory _nome, uint256 _dataNascimento) public {
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
        pacienteIdToAddress[idCounter] = generatedId;

        emit PacienteRegistrado(idCounter, generatedId);
    }


    function desativarPaciente(bytes32 _id) public {
        address pacienteAddress = idToPaciente[_id];
        require(pacienteAddress != address(0), "Nao existe paciente com ID informado");
        pacientes[pacienteAddress].pacienteAtivo = false;

        emit PacienteDesativado(pacientes[pacienteAddress].id, pacienteAddress);
    }

    function existePaciente(address wallet) public view returns (bool) {
        return pacientes[wallet].id != 0;
    }
}
