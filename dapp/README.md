## Funcionalidades da Minimas da Etapa 2

Nesta etapa, cada grupo deve implementar seu respectivo contrato inteligente com base nas definições funcionais previamente descritas. Como há **interdependência entre os módulos**, algumas funcionalidades exigem chamadas e validações de contratos de outros grupos. Dessa forma, **a comunicação entre os grupos será essencial**. Recomenda-se o uso de *issues*, canais de mensagens ou qualquer outro meios alinhar as interfaces e garantir a integração fluida entre os contratos.

A avaliação final será por grupo, utilizando o **Remix IDE**, onde será verificado se o modulo implementa as funcionalidades descritas e se está **funcional**.

1.  [**Funcionalidade minimas do sistema**](#funcionalidade-minimas-do-sistema)
    1.  [Módulo Pacientes](#módulo-pacientes)
    2.  [Módulo Profissionais de Saúde](#módulo-profissionais-de-saúde)
    3.  [Módulo Controle de Estoque](#módulo-controle-de-estoque)
    4.  [Módulo de Procedimentos](#módulo-de-procedimentos)
    5.  [Módulo de Controle de Acesso e Relatórios](#módulo-de-controle-de-acesso-e-relatórios)
1.  [**Sugestão de Implementação**](#sugestão-de-implementação)
1.  [**Onde os módulos serão testados?**](#onde-os-módulos-serão-testados)

## Funcionalidade minimas do sistema

Esta seção descreve, por módulo, as funcionalidades minimas esperadas.

### Módulo Pacientes

#### Cadastro

O cadastro de um novo paciente pode ser feito por profissionais de saúde devidamente registrado no sistema. Esse processo associa o endereço da carteira com o médico responsável e define seu status como ativo ou não, podendo ser atualizado caso necessário. E importante que cada inserção ou alteração deve ser armazenado indexado na blockchain.

#### Consultas

Este módulo também permite a consulta do status de um paciente, bem como o histórico de procedimentos associados a cada carteira de paciente. Nenhum dado sensível ou pessoal é armazenado diretamente, reforçando a privacidade. Ao mesmo tempo, o Diretor Médico mantém um mapeamento off-chain entre carteiras e identidades internas, acessível sob registro e com fins de auditoria.


### Módulo Profissionais de Saúde

#### Cadastro

A cada profissional é atribuída os dados como nome, categoria profissional (médico, enfermeiro, dentista, fisioterapeuta), identificação interna do hospital, registro no conselho de classe (numero do CRM/COREN...) e seu endereço de carteira. A funcionalidade principal é garantir que apenas usuários devidamente registrados e ativos possam interagir com os contratos dos demais módulos, seja para cadastrar pacientes, registrar procedimentos ou gerenciar estoque. A alteração do status de um profissional — ativando ou desativando seu acesso — também é controlada dentro deste módulo. A cada aleração ou cadastro o modulo deve gerar registro indexados.

#### Consultas

Este módulo deve disponibilizar consultas públicas para verificar se um profissional está ativo, além de permitir filtrar profissionais por categoria e a listagem dos procedimentos realizadas pelo profissional. 

### Módulo Controle de Estoque

#### Cadastro

Esse módulo funciona como um catálogo de materiais e medicamentos utilizados nos procedimentos clínicos. Ele não registra a quantidade de cada item no estoque, aspecto que permanece sob a responsabilidade do sistema offchain, mas assegura que todos os insumos utilizados estejam devidamente cadastrados, com informações como o lote, a validade, a categoria do item (como antibiótico, material cirúrgico etc.) e se trata-se de um item de alto custo.

Apenas profissionais cadastrados podem catalogar novos itens. E para todo cadastro de item de alto custo, este deve ser indexado pelo lote e proficional. 

#### Consultas

É possível consultar detalhes de qualquer item por meio de seu identificador, verificar se está com data de validade vigente e até listar itens com base em sua categoria. Se um item de alto custo for utilizado, essa informação pode ser usada para gerar notificações ao Diretor Médico.

### Módulo de Procedimentos

#### Cadastro

Este modulo permite o registro de um procedimento clínico, validando se o profissional responsável está ativo e devidamente registrado, se a carteira utilizada pelo paciente é conhecida e também se os materiais incluídos estão corretamente catalogados. O procedimento só é registrado se todas essas validações forem bem-sucedidas — caso contrário, a transação é revertida. Além disso, toda vez que um material de alto custo é utilizado em um procedimento, o contrato emite um evento correspondente.

O contrato permite que o Diretor Médico adicione novos tipos de procedimento sem a necessidade de alterar toda a lógica do sistema. Em caso de intercorrência médica durante um procedimento, o evento correspondente é emitido, permitindo que sistemas off-chain reagam a estas situações imediatamente, por exemplo, disparando um e-mail ou SMS ao responsável hospitalar.

#### Consultas

É possível consultar os dados de qualquer procedimento, listar os procedimentos realizados por um determinado profissional, listar os procedimentos por tipo e ainda extrair um histórico de intercorrências registradas.

### Módulo de Controle de Acesso e Relatórios (não implementado)

Embora este módulo constasse na proposta original do sistema como responsável pela governança de acesso e geração de relatórios consolidados, a divisão de equipes impediu sua implementação prática. Como alternativa, suas funcionalidades críticas foram parcialmente absorvidas pelos demais módulos. 

Dessa forma, cada contrato é responsável por validar diretamente se a carteira que tenta executar determinada ação é de um profissional habilitado. Além disso, os eventos emitidos por todos os contratos permitem que ferramentas externas ou scripts off-chain gerem relatórios e acompanhem o histórico de eventos da rede com finalidades administrativas e de auditoria.

## Sugestão de Implementação

Para garantir uma implementação o mais fluida possivel, recomenda-se seguir a seguinte ordem:

1. **Definição das `structs` e tipos auxiliares** O primeiro passo é definir todas as estruturas de dados (`structs`) que serão utilizadas nos contratos. Isso inclui estruturas como `Profissional`, `ItemEstoque`, `MaterialUtilizado`, `Procedimento`, entre outras. Também é importante definir `enums`, `mappings` e eventos que permitam futura integração entre os módulos. Essa etapa pode ser modularizada por contrato, mas mantendo coerência nas definições compartilhadas.
1. **Dialogo entre os grupos para definição das assinaturas** : Os grupos devem ser comunicar para solicitar as assinaturas dos metodos que utilizaram de outros contratos.
1. **Implementação dos Módulos**
    <!-- - Profissionais de Saúde & Pacientes
    - Estoque & Procedimentos -->
6. **Validação e testes integrados**  
   Após a conclusão dos contratos principais, cada equipe pode realizar testes integrados com os outros módulos. 

## Onde os módulos serão testados?

É esperado que os módulos sejam executados em uma rede **Hyperledger Besu**, utilizando o [ambiente de testes disponível neste repositório](https://github.com/ccufcg/bc101-dev-env).

> Embora não seja necessário, caso haja interesse/necessidade, podem considerar o endereço da conta do **diretor médico** como `0xfe3b557e8fb62b89f4916b721be55ceb828dbd73`

