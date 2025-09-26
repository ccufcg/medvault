// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

import "dapp/procedimentos/libs.sol";
import "dapp/profissionais/libs.sol";

contract ProfissionalManager is IGerenciadorProfissionais, IVerificadorProfissional, IProcedimentoStorage {
    address private owner;

    mapping(address => EntidadesProfissionais.Profissional) private _profissionais;
    address[] private _profissionaisList;
    mapping(EntidadesProfissionais.Categoria => address[]) private _indicePorCategoria;
    mapping(address => uint[]) private _procedimentosDoProfissional;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyAdmin() {
        if (msg.sender != owner) revert isNotAdmin(owner, msg.sender);
        _;
    }

    function novoProfissional(
        address wallet,
        uint256 idLegado,
        string calldata nome,
        EntidadesProfissionais.Categoria categoria,
        string calldata registro,
        bool ativo
    ) external onlyAdmin
      returns (EntidadesProfissionais.Profissional memory) {
        if (wallet == address(0)) revert enderecoZero();
        if (_profissionais[wallet].wallet != address(0)) revert profissionalJaCadastrado(wallet);

        EntidadesProfissionais.Profissional memory p = EntidadesProfissionais.Profissional({
            wallet: wallet,
            idLegado: idLegado,
            nome: nome,
            categoria: categoria,
            registro: registro,
            ativo: ativo
        });

        _profissionais[wallet] = p;
        _indicePorCategoria[categoria].push(wallet);
        _profissionaisList.push(wallet);

        emit ProfissionalCadastrado(wallet, idLegado);

        if (ativo) emit ProfissionalAtivado(wallet, msg.sender);
        else emit ProfissionalDesativado(wallet, msg.sender);

        return p;
    }

    function isProfissionalAtivo(address wallet) external view returns (bool) {
        EntidadesProfissionais.Profissional storage p = _profissionais[wallet];
        if (p.wallet == address(0)) revert profissionalNaoCadastrado(wallet);
        return p.ativo;
    }

    function desativarProfissional(address wallet) external onlyAdmin {
        EntidadesProfissionais.Profissional storage p = _profissionais[wallet];
        if (p.wallet == address(0)) revert profissionalNaoCadastrado(wallet);
        if (!p.ativo) revert profissionalJaInativo(wallet);
        p.ativo = false;
        emit ProfissionalDesativado(wallet, msg.sender);
    }

    function ativarProfissional(address wallet) external onlyAdmin {
        EntidadesProfissionais.Profissional storage p = _profissionais[wallet];
        if (p.wallet == address(0)) revert profissionalNaoCadastrado(wallet);
        if (p.ativo) revert profissionalJaAtivo(wallet);
        p.ativo = true;
        emit ProfissionalAtivado(wallet, msg.sender);
    }

    function getProfissional(address wallet)
        external
        view
        returns (EntidadesProfissionais.Profissional memory)
    {
        EntidadesProfissionais.Profissional memory p = _profissionais[wallet];
        if (p.wallet == address(0)) revert profissionalNaoCadastrado(wallet);
        return p;
    }

    function getAllProfissionais()
        external
        view
        returns (EntidadesProfissionais.Profissional[] memory) 
    {
        uint256 n = _profissionaisList.length;
        EntidadesProfissionais.Profissional[] memory arr = new EntidadesProfissionais.Profissional[](n);
        
        for (uint256 i = 0; i < n; i++) {
            arr[i] = _profissionais[_profissionaisList[i]];
        }

        return arr;
    }

    function verificarProfissional(address profissional_id)
        external
        view
        override
        returns (bool)
    {
        EntidadesProfissionais.Profissional memory p = _profissionais[profissional_id];
        return p.ativo;
    }

    function getProcedimentosDoProfissional(address wallet)
        external
        view
        returns (uint[] memory)
    {
        if (_profissionais[wallet].wallet == address(0)) revert profissionalNaoCadastrado(wallet);
        return _procedimentosDoProfissional[wallet];
    }

    function getProfissionaisPorCategoria(
        EntidadesProfissionais.Categoria categoria,
        bool onlyActive
    ) external view returns (address[] memory) {
        address[] memory allInCat = _indicePorCategoria[categoria];
        if (!onlyActive) return allInCat;

        uint len = allInCat.length;
        uint total;
        for (uint i = 0; i < len; i++) {
            if (this.verificarProfissional(allInCat[i])) total++;
        }

        address[] memory filtered = new address[](total);
        uint idx;
        for (uint i = 0; i < len; i++) {
            if (this.verificarProfissional(allInCat[i])) {
                filtered[idx++] = allInCat[i];
            }
        }
        return filtered;
    }

    function insertProcedimento(uint procedimento_id, address wallet) external {
        _procedimentosDoProfissional[wallet].push(procedimento_id);
    }
}
