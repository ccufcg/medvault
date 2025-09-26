// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;

library EntidadesProfissionais {
    struct Profissional {
        address wallet;
        uint256 idLegado;
        string nome;
        Categoria categoria;
        string registro;
        bool ativo;
    }

    enum Categoria {
        Medico,
        Enfermeiro
    }
}

interface IGerenciadorProfissionais {
    function novoProfissional(
        address wallet,
        uint legacyId,
        string calldata name,
        EntidadesProfissionais.Categoria category,
        string calldata councilRegistration,
        bool ativo
    ) external returns (EntidadesProfissionais.Profissional memory);

    function getProfissional(address wallet)
        external
        view
        returns (EntidadesProfissionais.Profissional memory);

    function getAllProfissionais() external view returns (EntidadesProfissionais.Profissional[] memory)

    function ativarProfissional(address wallet) external;
    function desativarProfissional(address wallet) external;

    function isProfissionalAtivo(address wallet) external view returns (bool);
}

event ProfissionalCadastrado(address indexed wallet, uint indexed legacyId);
event ProfissionalAtivado(address indexed wallet, address indexed by);
event ProfissionalDesativado(address indexed wallet, address indexed by);

error enderecoZero();
error profissionalJaCadastrado(address wallet);
error profissionalNaoCadastrado(address wallet);
error profissionalJaAtivo(address wallet);
error profissionalJaInativo(address wallet);
error moduloNaoAutorizado(address sender);
