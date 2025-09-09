Claro! Abaixo estão as funcionalidades esperadas para cada um dos módulos do sistema **MedVault**, com base na documentação fornecida. Incluem tanto funcionalidades de escrita (mutação do estado), quanto funcionalidades de leitura (consultas).

---

## ✅ **1. Módulo de Pacientes**

### 📌 Funcionalidades Principais

#### 🔧 Escrita
- `cadastrarPaciente(address walletPaciente)`: Cadastra um novo paciente vinculado a uma wallet. Só é permitido por profissionais cadastrados.
- `atualizarStatusPaciente(address walletPaciente, bool ativo)`: Altera status ativo/inativo do paciente.
- `vincularResponsavel(address walletPaciente, address walletMedico)`: Registra médico responsável.

#### 🔍 Consulta
- `consultarPaciente(address walletPaciente)`: Retorna os dados do paciente (sem dados pessoais).
- `listarProcedimentosPorPaciente(address walletPaciente)`: Retorna o histórico de procedimentos associados ao paciente.
- `isPacienteAtivo(address walletPaciente)`: Verifica se o paciente está ativo.

---

## ✅ **2. Módulo de Profissionais de Saúde**

### 📌 Funcionalidades Principais

#### 🔧 Escrita
- `registrarProfissional(address wallet, string nome, uint idHospital, Categoria categoria, string registroConselho)`: Registra novo profissional.
- `alterarStatusProfissional(address wallet, bool ativo)`: Ativa ou desativa um profissional.

#### 🔍 Consulta
- `consultarProfissional(address wallet)`: Retorna os dados do profissional vinculado ao wallet.
- `isProfissionalAtivo(address wallet)`: Verifica se o profissional está ativo.
- `listarProfissionaisPorCategoria(Categoria categoria)`: Lista todos os profissionais por categoria (médico, enfermeiro, etc).

---

## ✅ **3. Módulo de Controle de Estoque**

### 📌 Funcionalidades Principais

#### 🔧 Escrita
- `catalogarItem(uint idItemHospital, string lote, uint dataValidade, Categoria categoria, bool altoCusto)`: Cadastra/atualiza item no estoque (apenas por profissional válido).
- `registrarUsoItem(uint idItemHospital)`: Marca o item como utilizado (chamada via Procedimentos).

#### 🔍 Consulta
- `consultarItem(uint idItemHospital)`: Retorna os dados do item.
- `itemExiste(uint idItemHospital)`: Verifica se o item está catalogado.
- `listarItensPorCategoria(Categoria categoria)`: Retorna todos os itens de determinada categoria.
- `estaValido(uint idItemHospital)`: Verifica, via timestamp, se o item ainda está dentro do prazo de validade.

---

## ✅ **4. Módulo de Procedimentos**

### 📌 Funcionalidades Principais

#### 🔧 Escrita
- `cadastrarProcedimento(address paciente, address responsavel, string tipo, uint data, MaterialUtilizado[] materiais, bool intercorrencia)`: Registra novo procedimento.
- `adicionarTipoProcedimento(string tipo)`: Adiciona um novo tipo permitido de procedimento (exclusivo do Diretor Médico).

#### 🔍 Consulta
- `consultarProcedimento(uint idProcedimento)`: Retorna os dados completos do procedimento.
- `listarProcedimentosPorResponsavel(address profissional)`: Lista procedimentos realizados por um profissional.
- `listarIntercorrencias()`: Retorna todos os procedimentos marcados com intercorrência.
- `isTipoPermitido(string tipo)`: Verifica se um tipo de procedimento é aceito.

---

## ⚠️ **5. Módulo de Controle de Acesso e Relatórios** (não implementado)

✅ Como compensação:
- Todos os módulos devem manter **verificação de permissões** manualmente com base no endereço da carteira.
- **Auditoria mínima** é feita por meio de **eventos emitidos**, que podem ser lidos por um sistema externo (off-chain).

---

### ⚙️ Eventos recomendados (em todos os contratos):

- `PacienteCadastrado(address wallet)`
- `ProfissionalRegistrado(address wallet, uint idHospital)`
- `ItemCatalogado(uint idItemHospital)`
- `ProcedimentoRegistrado(uint idProcedimento, address paciente, address responsavel)`
- `NotificacaoIntercorrencia(uint idProcedimento)`

---

Se quiser, posso agora gerar os protótipos (assinaturas das funções em Solidity) ou os contratos esboçados para cada módulo. Deseja isso?