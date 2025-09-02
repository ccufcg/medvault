## Metodologia de Trabalho 

Adotaremos uma metodologia de trabalho estruturada que simula um ambiente de desenvolvimento profissional. Este guia descreve nosso fluxo de trabalho, a estratégia de branches e as responsabilidades de cada grupo ao longo do projeto.

### As Fases do Projeto

Dividiremos nosso trabalho em quatro fases distintas.

1. Desenho, Documentação e Planejamento
1. Implementação dos Contratos Inteligentes
1. Implementação das Interfaces (API e/ou DApp)
1. Integração Final e Apresentação

Cada fase e descrita abaixo

#### Fase 1: Desenho, Documentação e Planejamento

Antes de escrever qualquer código, todos os grupos se reunirão para definir a arquitetura do sistema. O resultado principal será um único documento chamado `SPECIFICATION.md` na pasta `docs` do nosso repositório. Este arquivo detalhará as assinaturas exatas de cada função, as estruturas de dados (`structs`) e os eventos de cada contrato inteligente, etc... Este é o momento de concordar sobre como os diferentes módulos do sistema conversarão entre si.

Cada grupo, pode cirar um arquivo `.md`, exemplo `modulo_paciente.md` na pasta `docs` que ao final sera referenciado pelo `SPECIFICATION.md`.


#### Fase 2: Implementação dos Contratos Inteligentes

Cada grupo criará sua própria branch a partir da `develop` e começará a implementar os contratos pelos quais é responsável. 

Quando um grupo finalizar uma parte funcional do seu contrato, ele abrirá um **Pull Request (PR)**. Este é um pedido formal para mesclar o trabalho da branch do grupo na branch `develop`. O professor, e idealmente membros de outros grupos, revisarão o código, sugerirão melhorias e, finalmente, aprovarão a integração. Nenhum código entra na `develop` sem revisão.

Se um grupo precisar de uma função que outro grupo acabou de criar, ele não deve puxar o código diretamente da branch do outro grupo. Em vez disso, o grupo que criou a função deve primeiro integrá-la à `develop` via PR. Depois, o grupo que precisa da função simplesmente atualiza sua própria branch a partir da `develop` para receber a novidade. A `develop` é nossa única fonte de verdade para o trabalho integrado.

#### Fase 3: Implementação das Interfaces (API e/ou DApp)

Depois que os contratos estiverem na blockchain, precisaremos de uma maneira para os usuários interagirem com eles. Nesta fase, os grupos construirão as interfaces, que podem ser um site (DApp) ou uma API de backend.

O processo de trabalho é exatamente o mesmo da fase anterior. O desenvolvimento acontece na branch do grupo, e as funcionalidades prontas são integradas à branch `develop` por meio de Pull Requests revisados.

#### Fase 4: Integração Final e Apresentação

Nesta última fase, garantiremos que todas as peças do quebra-cabeça se encaixam perfeitamente. Todos os grupos realizarão testes de integração no sistema completo, que estará implantado em uma rede de testes comum. O objetivo é caçar e corrigir bugs que só aparecem quando os diferentes módulos interagem.

Ao final, após a apresentação do projeto e os ajustes finais, o professor fará o último e mais importante merge: da branch `develop` para a `main`. Isso marcará a conclusão oficial do projeto, deixando a branch `main` como um registro limpo e funcional do nosso trabalho, servindo como um excelente portfólio para todos os envolvidos.


### Branches

A branch **`main`** será gerênciada pelo profgessor. Ela representa o produto final, estável e completo. Ninguém, exceto o professor, poderá enviar código diretamente para ela. Esta branch é o destino final do nosso trabalho.

A branch **`develop`** é onde a mágica acontece. Ela servirá como a branch de integração principal, refletindo o estado atual do desenvolvimento do projeto. Todas as funcionalidades finalizadas e revisadas pelos grupos serão incorporadas aqui antes de seguirem para a `main`.

Cada grupo trabalhará em sua própria **branch de longa duração**, que será criada a partir da `develop`. Por exemplo, `grupo-pacientes` ou `grupo-estoque`. Todo o desenvolvimento diário, testes e experimentos de um grupo ocorrerão isoladamente nesta branch, sem afetar o trabalho dos outros.

Nosso fluxo de trabalho pode ser resumido da seguinte forma: o código flui da `develop` para as branches dos grupos, e retorna para a `develop` através de um processo de revisão chamado Pull Request.