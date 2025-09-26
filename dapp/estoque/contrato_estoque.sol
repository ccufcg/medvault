// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "dapp/estoque/libs.sol";

interface IVerificadorEstoque {
    function verificarEstoque(uint uuid) external view returns (bool);
    function verificarItemAltoCusto(uint uuid) external view returns (bool);
}

contract Estoque is IVerificadorEstoque {

    mapping(uint => Entidades.ItemEstoque) private catalogoItens;
    uint private contadorIds;
    address public admin;

    event ItemCatalogado(uint indexed idItemHospital, uint idHash);
    event ItemUtilizado(uint indexed idItemHospital, uint idHash);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Apenas admin");
        _;
    }

    constructor() {
        admin = msg.sender;
    }

    // Funções Admin - necessário modulo de controle de admin 
    function addItem(
        uint idItemHospital,
        string memory lote,
        Entidades.EnumCategoria categoria,
        uint dataValidade,
        bool altoCusto,
        string memory descricao
    ) external onlyAdmin returns (uint) {
        contadorIds++;
        catalogoItens[contadorIds] = Entidades.ItemEstoque({
            idHash: contadorIds,
            idItemHospital: idItemHospital,
            dataValidade: dataValidade,
            categoria: categoria,
            descricao: descricao,
            altoCusto: altoCusto,
            lote: lote
        });

        emit ItemCatalogado(idItemHospital, contadorIds);
        return contadorIds;
    }

    function getItem(uint uuid) external view returns (Entidades.ItemEstoque memory) {
        require(catalogoItens[uuid].idHash != 0, "Item inexistente");
        return catalogoItens[uuid];
    }

    // Funções Externas 
    // Verifica se o item existe e não está vencido.
    function verificarEstoque(uint uuid) external view override returns (bool) {
        Entidades.ItemEstoque storage item = catalogoItens[uuid];
        return (item.idHash != 0 && item.dataValidade > block.timestamp);
    }

    // Retorna True se o item é marcado como alto custo.
    function verificarItemAltoCusto(uint uuid) external view override returns (bool) {
        Entidades.ItemEstoque storage item = catalogoItens[uuid];
        return (item.idHash != 0 && item.altoCusto);
    }

    // Evento de Uso de item de alto custo deveria ser auqi
    function registrarUso(uint uuid) external {
        Entidades.ItemEstoque storage item = catalogoItens[uuid];
        require(item.idHash != 0, "Item inexistente");
        require(item.dataValidade > block.timestamp, "Item vencido");
        emit ItemUtilizado(item.idItemHospital, item.idHash);
    }
}