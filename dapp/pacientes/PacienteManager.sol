contract PacienteManager {
    struct Procedimento {
        string nome;
    }

    struct PacienteStorage {
        address id;
        string nome;
        uint256 dataNascimento;
        bool ativo;
        Procedimento[] procedimentos;
    }
}