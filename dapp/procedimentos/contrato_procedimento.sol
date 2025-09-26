// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "dapp/procedimentos/libs.sol";

contract GerenciadorProcedimento is IGerenciadorProcedimento {
    mapping(uint => Entidades.Procedimento) private procedimentos;
    
    // O índice 0 será utilizado como índice coringa, para ser usado como indice de procedimento anterior, ao não existir indice anterior!
    uint private procedimento_next_id = 1;

    address private admin;
    address private verificadorPaciente;
    address private verificadorProfissional;
    address private verificadorEstoque;
    address private verificadorTipoProcedimento;

    constructor(address verificador_paciente, address verificador_profissional, address verificador_estoque, address verificador_tipo_procedimento) {
        admin = msg.sender;
        verificadorPaciente = verificador_paciente;
        verificadorProfissional = verificador_profissional;
        verificadorEstoque = verificador_estoque;
        verificadorTipoProcedimento = verificador_tipo_procedimento;
    }

    modifier isCapabaleToRegister() {
        require(msg.sender == admin || IVerificadorProfissional(verificadorProfissional).verificarProfissional(msg.sender), "Endereco sem permissao para executar funcao");
        _;
    }

    modifier procedureExists(uint id) {
        require(procedimentos[id].cadastrado || id == 0, "procedimento nao existe");
        _;
    }

    function cadastrarProcedimento(address id_paciente, uint id_procedimento_anterior, uint16 tipo_procedimento_id, bool intercorrencia) external procedureExists(id_procedimento_anterior) isCapabaleToRegister returns (Entidades.Procedimento memory) {
        require(procedimento_next_id + 1 != 0, "Limite de procedimentos atingido!");
        require(IVerificadorPaciente(verificadorPaciente).verificarPaciente(id_paciente), "Paciente nao existe");

        procedimentos[procedimento_next_id].id = procedimento_next_id;
        procedimentos[procedimento_next_id].id_paciente = id_paciente;
        procedimentos[procedimento_next_id].id_profissional = msg.sender;
        procedimentos[procedimento_next_id].id_procedimento_anterior = id_procedimento_anterior;
        procedimentos[procedimento_next_id].tipo_procedimento_id = tipo_procedimento_id;
        procedimentos[procedimento_next_id].intercorrencia = intercorrencia;
        procedimentos[procedimento_next_id].cadastrado = true;

        emit ProcedimentoCadastrado(procedimento_next_id, id_paciente, msg.sender);
        
        if (intercorrencia) {
            emit NotificacaoIntercorrencia(procedimento_next_id, msg.sender);
        }

        procedimento_next_id++;

        return procedimentos[procedimento_next_id];

    }

    function adicionaMaterial(uint id_procedimento, uint estoque_id, uint8 quantidade) procedureExists(id_procedimento) isCapabaleToRegister external {
        require(id_procedimento != 0, "procedimento nao existe");
        require(IVerificadorEstoque(verificadorEstoque).verificarEstoque(estoque_id), "estoque nao existe");

        procedimentos[id_procedimento].materiais.push(Entidades.MaterialUtilizado(estoque_id, quantidade));
        
        emit MaterialCadastrado(estoque_id, quantidade, id_procedimento, msg.sender);

        if (IVerificadorEstoque(verificadorEstoque).verificarItemAltoCusto(estoque_id)) {
            emit ItemAltoCustoUtilizado(estoque_id, quantidade, id_procedimento, msg.sender);
        }
    }

    function getProcedimento(uint id) external procedureExists(id) view returns (Entidades.Procedimento memory) {
        require(id != 0, "procedimento nao existe");
        return procedimentos[id];
    }

}