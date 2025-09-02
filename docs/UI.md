## **Interfaces (API vs. JS/DApp)**

Considerando o volume e a complexidade, a sugestão para os grupos de alunos seria:


*   **Módulo de Procedimentos:** Uma **API** ou **JS** seria a interface prioritária para interagir com este módulo, pois pode gerenciar a complexidade das chamadas e se integrar aos sistemas existentes do hospital.
*   **Módulo de Controle de Estoque:** A lógica do contrato é de um catálogo, mas ele será intensamente consultado. Uma **API** ou **JS** para o sistema de almoxarifado do hospital popular e gerenciar este catálogo seria o mais eficiente.
*   **Módulo de Pacientes e Módulo de Profissionais:** Ambos são essencialmente contratos de registro. A lógica on-chain simples (adicionar, desativar, verificar existência). São excelentes candidatos para que os alunos implementem **ambas as interfaces** a exemplo:
    1.  Uma **API** para o sistema de RH/Cadastro do hospital gerenciar os registros.
    2.  Uma **Interface JS (DApp com Metamask)** para que um administrador ou o próprio profissional possa visualizar seus dados.
*   **Módulo de Relatórios e Controle de Acesso:** A função de relatório no contrato é apenas de leitura. Em razão disso gostaria de um front-end **Interface JS (DApp)**, onde o grupo criará uma tela de filtros que consome os dados do contrato via Metamask e os exibe em tabelas:
    1. Listagem dos procedimento realizados com alguns filtros
    2. Busca dos procedimentos que utilizaram um insumo (do estoque) por `tipo` ou com o `lote` especifico!

agora o relatorio só será exibido se a carteira for de um profissional de saúde ou do diretor médico. 


Sumário:

| Módulo | Grupo | Interface Sugerida | 
| :--- | :--- | :--- |
| **Gestão de Pacientes** | Grupo X | API **e** JS |
| **Cadastro de Profissionais** | Grupo X | API **e** JS | 
| **Controle de Estoque** | Grupo X | API **ou** JS | 
| **Registro de Procedimentos** | Grupo X | API **ou** JS | 
| **Acesso e Relatórios**| Grupo X | Interface JS | 


