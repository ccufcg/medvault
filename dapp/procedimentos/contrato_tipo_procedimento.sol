// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "dapp/procedimentos/libs.sol";

contract GerenciadorTipoProcedimento is IGerenciadorTiposProcedimento, IVerificadorTipoProcedimento {
    uint16 private quantos_tipos;
    mapping(uint16 => Entidades.TipoProcedimento) private tipos_procedimento;
    
    address private admin;
    address private verificador_categoria_saude;

    constructor(address verificador_categoria_saude_address) {
        admin = msg.sender;
        verificador_categoria_saude = verificador_categoria_saude_address;
    }

    modifier isAdmin() {
        require(msg.sender == admin, isNotAdmin(admin, msg.sender));
        _;
    }

    modifier typeExists(uint16 id) {
        require(tipos_procedimento[id].cadastrado, tipoProcedimentoNaoExiste(id));
        _;
    }

    function cadastraTipo(string memory tipo, uint16 categoria_profissional_id) external isAdmin returns (Entidades.TipoProcedimento memory) {
        require(IVerificadorCategoriaSaude(verificador_categoria_saude).VerificarExistenciaCategoria(categoria_profissional_id), categoriaSaudeNaoExiste(categoria_profissional_id));
        require(!tipos_procedimento[quantos_tipos].cadastrado, tipoProcedimentoLimiteAtingido());
        tipos_procedimento[quantos_tipos] = Entidades.TipoProcedimento(quantos_tipos, tipo, categoria_profissional_id, true);
        emit TipoCadastrado(quantos_tipos, tipo, categoria_profissional_id);
        quantos_tipos++;
        return tipos_procedimento[quantos_tipos-1];
    }
    
    function getTipo(uint16 id) external typeExists(id) view returns(Entidades.TipoProcedimento memory) {
        return tipos_procedimento[id];
    }
    
    function deleteTipo(uint16 id) typeExists(id) isAdmin external {
        uint16 temp = id;
        Entidades.TipoProcedimento memory tipo = tipos_procedimento[id];
        while (tipos_procedimento[temp].cadastrado && temp + 1 != id) {
            tipos_procedimento[temp] = tipos_procedimento[temp + 1];
        }
        tipos_procedimento[temp].cadastrado = false;
        quantos_tipos--;
        emit TipoDeletado(id, tipo.tipo, tipo.categoria_profissional_id);
    }

    function verificarTipoProcedimento(uint16 procedimento_id) external view returns (bool) {
        return tipos_procedimento[procedimento_id].cadastrado;
    }

}