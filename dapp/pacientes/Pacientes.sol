
struct Procedimento {
    // Importar procedimento
    string nome;
}

struct Paciente {
    address id;
    string nome;
    uint256 dataNascimento;
    bool ativo;
    // Armazenar esses dois aqui é muito problemático pra função createPaciente() !!!
    // Procedimento[] procedimentos;
    // bytes32[] wallets; // Wallets são os mútiplos ids que teremos, logo, serão bytes32
}


contract Pacientes {
    mapping(address => bytes32[]) private pacienteIdentificadores;
    mapping(address => Paciente) public pacientes;
    mapping(bytes32 => address) idToPaciente;
    uint256 private idCounter;

    function createPaciente(string memory _nome, uint256 _dataNascimento) public{
        // Necessário pra gerar o address dinamicamente
        idCounter++;
        address generatedId = address(uint160(uint256(keccak256(abi.encodePacked(msg.sender, idCounter, block.timestamp)))));

        pacientes[generatedId] = Paciente({
            id: generatedId,
            nome: _nome,
            dataNascimento: _dataNascimento,
            ativo: true
        });

    }


}

