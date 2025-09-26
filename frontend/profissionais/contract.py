address = "0xB40f83837274EfF33631637CBD8aC61579f362b5"
abi = [
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
