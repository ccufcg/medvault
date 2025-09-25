// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "./libs.sol";

interface IVerificadorEstoque {
    function verificarEstoque(uint uuid) external view returns (bool);
    function verificarItemAltoCusto(uint uuid) external view returns (bool);
}

contract Estoque is IVerificadorEstoque {

    mapping(uint => Entidades.ItemEstoque) private catalogoItens;
    uint private contadorIds;
    address public admin;

    // Controle das categorias dinâmicas
    string[] private categorias; // lista de categorias validas
    mapping(string => bool) private categoriaValida; // mapping para verificação

    event CategoriaAdicionada(string nomeCategoria);
    event ItemCatalogado(uint indexed idItemHospital, uint idHash);
    event ItemUtilizado(uint indexed idItemHospital, uint idHash);

    modifier onlyAdmin() {
        require(msg.sender == admin, "Apenas admin");
        _;
    }

    constructor() {
        admin = msg.sender;
    }
    // Funções Externas 
    // Funções de categoria
    function addCategoria(string memory nomeCategoria) external onlyAdmin {
        require(bytes(nomeCategoria).length > 0, "Nome invalido");
        require(!categoriaValida[nomeCategoria], "Categoria ja existente");
        categorias.push(nomeCategoria);
        categoriaValida[nomeCategoria] = true;
        emit CategoriaAdicionada(nomeCategoria);
    }

    function listarCategorias() external view returns (string[] memory) {
        return categorias;
    }
    function categoriaExiste(string memory nomeCategoria) public view returns (bool) {
        return categoriaValida[nomeCategoria];
    }
    
    // Funções add Item
    function addItem(
        uint idItemHospital,
        string memory lote,
        string memory categoria,
        uint dataValidade,
        bool altoCusto,
        string memory descricao
    ) external onlyAdmin returns (uint) {
        require(categoriaValida[categoria], "Categoria nao existe");

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

    // Lista todos os itens cadastrados
    function listarItens() external view returns (Entidades.ItemEstoque[] memory) {
        Entidades.ItemEstoque[] memory itens = new Entidades.ItemEstoque[](contadorIds);
        uint j = 0;
        for (uint i = 1; i <= contadorIds; i++) {
            if (catalogoItens[i].idHash != 0) {
                itens[j] = catalogoItens[i];
                j++;
            }
        }
        return itens;
    }

    // Lista apenas os itens de alto custo
    function listarItensAltoCusto() external view returns (Entidades.ItemEstoque[] memory) {
        // Primeiro conta quantos itens alto custo existem
        uint count = 0;
        for (uint i = 1; i <= contadorIds; i++) {
            if (catalogoItens[i].altoCusto) {
                count++;
            }
        }

        // Cria array no tamanho exato
        Entidades.ItemEstoque[] memory itensAltoCusto = new Entidades.ItemEstoque[](count);
        uint j = 0;
        for (uint i = 1; i <= contadorIds; i++) {
            if (catalogoItens[i].altoCusto) {
                itensAltoCusto[j] = catalogoItens[i];
                j++;
            }
        }
        return itensAltoCusto;
    }
}