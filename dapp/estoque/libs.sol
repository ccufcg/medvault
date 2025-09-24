// SPDX-License-Identifier: GPL
pragma solidity >=0.4.0 <0.9.0;


library Entidades{

    enum EnumCategoria {
        Antibiotico,
        Sutura,
        Anestesia,
        Vacina,
        Material_Cirurgico
    }


    struct ItemEstoque {
        uint idHash;             
        uint idItemHospital;     
        uint dataValidade;       
        EnumCategoria categoria; 
        string descricao;        
        bool altoCusto;          
        string lote;             
    }
}