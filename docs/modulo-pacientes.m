```mermaid
classDiagram
    class Pacientes {
        <<Contract>>
        - pacienteIdentifiers: mapping(address → bytes32[])
        - idToPaciente: mapping(bytes32 → address)
        +registrarPaciente(wallet: address)
        +desativarPaciente(id: bytes32)
        +atualizarPaciente(id: bytes32)
        +existePaciente(id: bytes32): bool
        +obterPaciente(id: bytes32): Paciente onlyDiretorMedico
        +listarWallets(id: bytes32): address[]
        +removerWallet(id: bytes32)
        +adicionarWallet(id: bytes32)
        +getHistoricoProcedimentos(id: bytes32): Procedimento[]
    }

    class IPacientes {
        <<Interface>>
        +existePaciente(id: bytes32): bool
        +listarWallets(id: bytes32): address[]
    }

    class Paciente {
        <<Struct>>
        +id: bytes32
        +nome: string
        +dataNascimento: uint
        +pacienteAtivo: bool
        +wallets: address[]
        +historicoProcedimentos: bytes32[]
    }

    class Procedimento {
        <<Struct>>
        +id: bytes32
        ...
    }

    class Eventos {
        <<Events>>
        +PacienteRegistrado(id: bytes32, wallet: address)
        +PacienteAtualizado(id: bytes32)
        +PacienteDesativado(id: bytes32, wallet: address)
        +WalletAssociada(id: bytes32, wallet: address)
        +WalletRemovida(id: bytes32, wallet: address)
        +ProcedimentoRegistrado(idPaciente: bytes32, idProcedimento: bytes32)
        +Reidentificacao(diretor: address, wallet: address, idPaciente: bytes32)
    }

    class Roles {
        <<AccessControl>>
        +DEFAULT_ADMIN_ROLE
        +DIRETOR_ROLE
    }

    Pacientes ..|> IPacientes
    Pacientes --> Paciente : armazena
    Paciente --> Procedimento : historico
    Pacientes --> Eventos : dispara
    Pacientes --> Roles : restrições de acesso

```