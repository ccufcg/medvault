procedimento_address = "0x97821722D49Cd975d2208dd40d7f5015Ab4Bb936"
procedimento_abi = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "estoque_id",
				"type": "uint256"
			}
		],
		"name": "estoqueNaoExiste",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "isNotCapableRegisterProcedure",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "id_procedimento",
				"type": "uint256"
			}
		],
		"name": "procedimentoNaoExiste",
		"type": "error"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "estoque_id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "quantidade",
				"type": "uint8"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "id_profissional",
				"type": "address"
			}
		],
		"name": "ItemAltoCustoUtilizado",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "estoque_id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint8",
				"name": "quantidade",
				"type": "uint8"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "id_profissional",
				"type": "address"
			}
		],
		"name": "MaterialCadastrado",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "id_procedimento",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "estoque_id",
				"type": "uint256"
			},
			{
				"internalType": "uint8",
				"name": "quantidade",
				"type": "uint8"
			}
		],
		"name": "adicionaMaterial",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "id_paciente",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "id_procedimento_anterior",
				"type": "uint256"
			},
			{
				"internalType": "uint16",
				"name": "tipo_procedimento_id",
				"type": "uint16"
			},
			{
				"internalType": "bool",
				"name": "intercorrencia",
				"type": "bool"
			}
		],
		"name": "cadastrarProcedimento",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "address",
						"name": "id_paciente",
						"type": "address"
					},
					{
						"internalType": "address",
						"name": "id_profissional",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "id_procedimento_anterior",
						"type": "uint256"
					},
					{
						"components": [
							{
								"internalType": "uint256",
								"name": "material_id",
								"type": "uint256"
							},
							{
								"internalType": "uint8",
								"name": "quantidade",
								"type": "uint8"
							}
						],
						"internalType": "struct Entidades.MaterialUtilizado[]",
						"name": "materiais",
						"type": "tuple[]"
					},
					{
						"internalType": "uint16",
						"name": "tipo_procedimento_id",
						"type": "uint16"
					},
					{
						"internalType": "bool",
						"name": "intercorrencia",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "cadastrado",
						"type": "bool"
					}
				],
				"internalType": "struct Entidades.Procedimento",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "verificador_paciente",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "verificador_profissional",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "verificador_estoque",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "verificador_tipo_procedimento",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "procedimentoStorage",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "getProcedimento",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "id",
						"type": "uint256"
					},
					{
						"internalType": "address",
						"name": "id_paciente",
						"type": "address"
					},
					{
						"internalType": "address",
						"name": "id_profissional",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "id_procedimento_anterior",
						"type": "uint256"
					},
					{
						"components": [
							{
								"internalType": "uint256",
								"name": "material_id",
								"type": "uint256"
							},
							{
								"internalType": "uint8",
								"name": "quantidade",
								"type": "uint8"
							}
						],
						"internalType": "struct Entidades.MaterialUtilizado[]",
						"name": "materiais",
						"type": "tuple[]"
					},
					{
						"internalType": "uint16",
						"name": "tipo_procedimento_id",
						"type": "uint16"
					},
					{
						"internalType": "bool",
						"name": "intercorrencia",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "cadastrado",
						"type": "bool"
					}
				],
				"internalType": "struct Entidades.Procedimento",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
profissionais_address = "0x718E58098C2F0350f29555cC8280795494a402b2"
profissionais_abi = [
	{
		"inputs": [],
		"name": "enderecoZero",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "admin",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "isNotAdmin",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "profissionalJaAtivo",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "profissionalJaCadastrado",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "profissionalJaInativo",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "profissionalNaoCadastrado",
		"type": "error"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "by",
				"type": "address"
			}
		],
		"name": "ProfissionalAtivado",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "legacyId",
				"type": "uint256"
			}
		],
		"name": "ProfissionalCadastrado",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "by",
				"type": "address"
			}
		],
		"name": "ProfissionalDesativado",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "ativarProfissional",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "desativarProfissional",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "procedimento_id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "insertProcedimento",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "idLegado",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "nome",
				"type": "string"
			},
			{
				"internalType": "enum EntidadesProfissionais.Categoria",
				"name": "categoria",
				"type": "uint8"
			},
			{
				"internalType": "string",
				"name": "registro",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "ativo",
				"type": "bool"
			}
		],
		"name": "novoProfissional",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "wallet",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "idLegado",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "nome",
						"type": "string"
					},
					{
						"internalType": "enum EntidadesProfissionais.Categoria",
						"name": "categoria",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "registro",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "ativo",
						"type": "bool"
					}
				],
				"internalType": "struct EntidadesProfissionais.Profissional",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [],
		"name": "getAllProfissionais",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "wallet",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "idLegado",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "nome",
						"type": "string"
					},
					{
						"internalType": "enum EntidadesProfissionais.Categoria",
						"name": "categoria",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "registro",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "ativo",
						"type": "bool"
					}
				],
				"internalType": "struct EntidadesProfissionais.Profissional[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "getProcedimentosDoProfissional",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "enum EntidadesProfissionais.Categoria",
				"name": "categoria",
				"type": "uint8"
			},
			{
				"internalType": "bool",
				"name": "onlyActive",
				"type": "bool"
			}
		],
		"name": "getProfissionaisPorCategoria",
		"outputs": [
			{
				"internalType": "address[]",
				"name": "",
				"type": "address[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "getProfissional",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "wallet",
						"type": "address"
					},
					{
						"internalType": "uint256",
						"name": "idLegado",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "nome",
						"type": "string"
					},
					{
						"internalType": "enum EntidadesProfissionais.Categoria",
						"name": "categoria",
						"type": "uint8"
					},
					{
						"internalType": "string",
						"name": "registro",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "ativo",
						"type": "bool"
					}
				],
				"internalType": "struct EntidadesProfissionais.Profissional",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "wallet",
				"type": "address"
			}
		],
		"name": "isProfissionalAtivo",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "profissional_id",
				"type": "address"
			}
		],
		"name": "verificarProfissional",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
