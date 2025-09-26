### Proposta de Interfaces


1. [Descrição dos Módulos](#descrição-dos-módulos)
    1.  [Módulo Pacientes](#módulo-de-pacientes)
    2.  [Módulo Profissionais de Saúde](#módulo-de-profissionais-de-saúde)
    3.  [Módulo Controle de Estoque](#módulo-de-controle-de-estoque)
    4.  [Módulo de Procedimentos](#módulo-de-procedimentos)
1. [O que devo entregar?](#o-que-devo-entregar)

## Descrição dos Módulos

Nas seções aseguir são apresentados os requisitos das interfaces:

### Módulo de Pacientes 

O grupo de Pacientes deverá criar uma sistema/página web que simula o **"Portal do Diretor Médico"** para o gerenciamento de pacientes. Sendo dividdia em dois segmentos, cadastro e consultas.

O processo de cadastro seguira o seguinte fluxo: o atendente do hospital entrará com o **nome** e **CPF** do paciente. O sistema "off-chain" (que da as garantias de privacidade ao paciente):
1. irá gerar uma nova carteira e salvar a associação entre CPF, nome e o endereço da carteira. 
2. Em seguida, o sistema chamará o contrato para registrar a nova carteira na blockchain.

Ao final do processo, a página deve exibir o endereço da carteira gerada e, como sugestão (se possivel), um **QRCode** correspondente a esse endereço. Isso simula de forma excelente a entrega da "identidade digital" ao paciente para que ele possa realizar seus atendimentos. Caso não seja possivel, inserir um QRCode qualquer apenas para simular.

A seção de consulta para o "Diretor Médico", permitindo duas ações:

1.  Dado o endereço de uma carteira, recuperar o **nome e CPF** do paciente associado (buscando nos dados "off-chain").
2.  Dado um CPF, listar **todos os endereços de carteiras** já registrados para aquele paciente.

### Módulo de Profissionais de Saúde

Para este modulo o grupo deve implementar uma sistema web de cadastro e uma API de consulta.

Primeiro, devem criar uma **página de cadastro** para os profissionais, com campos para nome, ID do hospital, categoria, registro profissional e endereço da carteira.

Adicionalmente, o grupo deve desenvolver uma **API RESTful** que servirá como ponto de consulta para os outros módulos. Ela deve ter duas funcionalidades principais:

1.  **Listar todos os profissionais cadastrados.** A consulta deve retornar os dados em formato JSON, por exemplo:
    ```json
    [
      {
        "nome": "Dr. Gabriel",
        "categoria": "Medico",
        "registroConselho": "CRM/PB 12345",
        "wallet": "0xABC...123",
        "ativo": true
      }
    ]
    ```

2.  **Listar todos os procedimentos realizados por um profissional específico** (a busca será feita pelo endereço da carteira). Isso exigirá uma consulta ao contrato do Módulo de Procedimentos. O retorno pode seguir este modelo:
    ```json
    {
      "profissional": {
        "nome": "Dr. Matheus",
        "registroConselho": "CRM/PB 12345",
        "ativo": true,
        "wallet": "0xABC...123"
      },
      "procedimentos": [
        { "idProcedimento": 1, "pacienteWallet": "0xPac...iEnte1", "tipoProcedimento": "Cirurgia" },
        { "idProcedimento": 5, "pacienteWallet": "0xPac...iEnte2", "tipoProcedimento": "Curativo" }
      ]
    }
    ```

### Módulo de Controle de Estoque

O grupo de Controle de Estoque criará uma **API** para gerenciar o catálogo de itens e expor informações sobre o uso de materiais.

A API deve permitir o **cadastro de novos produtos/itens e suas categorias** através de uma chamada (ex: `POST /api/itens`), que só pode ser realizada por um profissional de saúde cadastrado. O grupo deve criar um script para popular a base com alguns itens basicos. E disponibilizar uma tabela em markdown com os itens e categorias.


A API deve implementar uma consulta que lista todos os **procedimentos que utilizaram itens de alto custo**. Para isso, o sistema de vocês deverá interagir com os contratos de Estoque (para saber quais itens são de alto custo) e de Procedimentos (para obter os detalhes). A listagem em JSON pode ser mais clara e informativa se seguir esta estrutura aprimorada:

```json
[
  {
    "procedimento": {
      "idProcedimento": 1,
      "pacienteWallet": "0xPac...iEnte1",
      "profissionalWallet": "0xABC...123"
    },
    "materiaisDeAltoCustoUtilizados": [
      {
        "idItemHospital": 5501,
        "lote": "LOTE-XYZ-2025",
        "quantidade": 1
      }
    ]
  }
]
```

### Módulo de Procedimentos

> ⚠️ Este módulo deve garantir que as consutlas dos demais modulos sejam executadas.
> - Certifiquem-se que os grupos podem iterar sobre coleção dos procedimentos
> - Que existam metodos para recupear os dados dos tipos de procedimentos


Este grupo deve prover uma **API** (ou uma pagina web) para o "Diretor Médico" poder **cadastrar novos tipos de procedimento** (ex: "Sessão de Quimioterapia", "Sutura Simples"), que serão salvos no contrato.

A segunda e principal tarefa é desenvolver uma página que funcionará como um **"Dashboard de Monitoramento em Tempo Real"**. Esta página deve "escutar" os eventos da blockchain. Toda vez que um procedimento for registrado utilizando um **material de alto custo**, um **pop-up de alerta** deve aparecer na tela **automaticamente** (sem precisar recarregar a página).

Para exibir as informações completas no pop-up, o sistema de vocês precisará:
1.  Capturar o evento da blockchain.
2.  Usar o endereço do profissional (disponível no evento) para consultar a **API do Módulo de Profissionais** e obter o nome e o número de registro dele.

O pop-up deve informar claramente os dados, como: **Nome do profissional (com registro)**, o **endereço da carteira do paciente** e o **tipo de procedimento** que está sendo realizado.

## O que devo entregar?

O código-fonte de cada grupo deve ser depositado em suas respectivas pastas dentro do diretório `frontend/`.

Além disso, cada grupo deve entregar um vídeo com a demonstração completa das funcionalidades desenvolvidas. O vídeo deve ser narrado, explicando o passo a passo da utilização do sistema e o cumprimento dos requisitos. Segue um breve checklist de cada modulo:

### Vídeos

É importante que o video deve ser narrado!

**Para o Módulo de Pacientes**: Video 1, demosntras o cadastro onde um atendente insere o nome e o CPF do paciente, fazendo com que o sistema gere uma nova carteira digital, associe os dados a ela e a registre na blockchain. Video 2, visão do diretor médico buscar o nome e CPF de um paciente usando o endereço da carteira, ou listar todas as carteiras de um paciente a partir do seu CPF.

**O Módulo de Profissionais de Saúde**: (video unico) Demonstrar o cadastro para profissionais, solicitando dados como nome, ID do hospital, categoria, registro profissional e endereço da carteira. Listar todos os profissionais cadastrados e, a partir do endereço da carteira de um profissional, listar todos os procedimentos que ele realizou, o que exigirá uma consulta ao contrato do Módulo de Procedimentos.

**Ao Módulo de Controle de Estoque**  Demonstrar o cadastro de produtos. Consultar os procedimentos que utilizaram itens de alto custo, interagindo com os contratos de Estoque e de Procedimentos para obter e exibir os dados detalhados.

**Finalmente, o Módulo de Procedimentos**: Cadastrar um procedimento simples e um de alto custo exibindo que apenas para o de alto custo resulta em um aviso ao diretor médico.

