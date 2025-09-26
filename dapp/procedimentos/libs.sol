// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

library Entidades {

    struct TipoProcedimento {
        uint16 id;
        string tipo;
        uint16 categoria_profissional_id;
        bool cadastrado;
    }

    struct MaterialUtilizado {
        uint material_id;
        uint8 quantidade;
    }

    struct Procedimento {
        uint id;
        address id_paciente;
        address id_profissional;
        uint id_procedimento_anterior;
        MaterialUtilizado[] materiais;
        uint16 tipo_procedimento_id;
        bool intercorrencia;
        bool cadastrado;
    }

}

interface IGerenciadorTiposProcedimento {
    function cadastraTipo(string memory tipo, uint16 categoria_profissional_id) external returns (Entidades.TipoProcedimento memory);
    function getTipo(uint16 id) external view returns(Entidades.TipoProcedimento memory);
    function deleteTipo(uint16 id) external;

    event TipoCadastrado(uint16 id, string tipo, uint16 categoria_profissional_id);
    event TipoDeletado(uint16 id, string tipo, uint16 categoria_profissional_id);

    error categoriaSaudeNaoExiste(uint16 categoria_profissional_id);
    error tipoProcedimentoLimiteAtingido();
}

interface IGerenciadorProcedimento {
    function cadastrarProcedimento(address id_paciente, uint id_procedimento_anterior, uint16 tipo_procedimento_id, bool intercorrencia) external returns (Entidades.Procedimento memory);
    function getProcedimento(uint id) external view returns (Entidades.Procedimento memory);
    function adicionaMaterial(uint id_procedimento, uint estoque_id, uint8 quantidade) external;

    event ProcedimentoCadastrado(uint indexed id, address indexed id_paciente, address indexed id_profissional);
    event NotificacaoIntercorrencia(uint indexed id, address indexed id_profissional);
    event MaterialCadastrado(uint indexed estoque_id, uint8 quantidade, uint indexed id, address indexed id_profissional);
    event ItemAltoCustoUtilizado(uint indexed estoque_id, uint8 quantidade, uint indexed id, address indexed id_profissional);

    error isNotCapableRegisterProcedure(address sender);
    error procedimentoLimiteAtingido();
    error tipoProcedimentoNaoExiste(uint16 tipo_procedimento_id);
    error pacienteNaoExiste(address id_paciente);
    error profisionalNaoExiste(address id_profissional);
    error procedimentoNaoExiste(uint id_procedimento);
    error estoqueNaoExiste(uint estoque_id);
}

interface IVerificadorCategoriaSaude {
    function VerificarExistenciaCategoria(uint16 categoria_profissional_id) external view returns (bool); 
}

interface IVerificadorPaciente {
    function verificarPaciente(address paciente_id) external view returns (bool);
}

interface IVerificadorProfissional {
    function verificarProfissional(address profissional_id) external view returns (bool);
}

interface IVerificadorEstoque {
    function verificarEstoque(uint estoque_id) external view returns (bool);
    function verificarItemAltoCusto(uint estoque_id) external view returns (bool);
}

interface IProcedimentoStorage {
    function insertProcedimento(uint procedimento_id, address wallet) external;
}

interface IVerificadorTipoProcedimento {
    function verificarTipoProcedimento(uint16 procedimento_id) external view returns (bool);
}

error isNotAdmin(address admin, address sender);
