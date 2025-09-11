
struct Procedimento {
    // Importar procedimento
    string nome;
}


contract Pacientes {
    mapping(address => bytes32[]) private pacienteIdentificadores;
    mapping(bytes32 => address) idToPaciente;

    struct Paciente {
        address id;
        string nome;
        uint256 dataNascimento;
        bool ativo;
        Procedimento[] procedimentos;
        bytes32[] wallets;
    }
}

