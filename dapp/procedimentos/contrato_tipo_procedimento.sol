// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "dapp/procedimentos/libs.sol";
import "dapp/profissionais/libs.sol";

contract GerenciadorTipoProcedimento is IGerenciadorTiposProcedimento, IVerificadorTipoProcedimento {
    uint16 private quantos_tipos;
    mapping(uint16 => Entidades.TipoProcedimento) private tipos_procedimento;
    
    address private admin;

    constructor() {
        admin = msg.sender;
    }

    modifier isAdmin() {
        require(msg.sender == admin, "is not admin");
        _;
    }

    modifier typeExists(uint16 id) {
        require(tipos_procedimento[id].cadastrado, "type not exist");
        _;
    }

    function cadastraTipo(string memory tipo, EntidadesProfissionais.Categoria categoria) external isAdmin returns (Entidades.TipoProcedimento memory) {
        require(!tipos_procedimento[quantos_tipos].cadastrado, "type ammount exceed the limit!");
        tipos_procedimento[quantos_tipos] = Entidades.TipoProcedimento(quantos_tipos, tipo, categoria, true);
        emit TipoCadastrado(quantos_tipos, tipo, categoria);
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
        emit TipoDeletado(id, tipo.tipo, tipo.categoria);
    }

    function verificarTipoProcedimento(uint16 procedimento_id) external view returns (bool) {
        return tipos_procedimento[procedimento_id].cadastrado;
    }
}