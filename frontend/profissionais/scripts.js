(() => {
  apiGet("/api/profissionais/0x5FB0a5ba9ebe2b5C1E138dC06241b09029a773ab") 
  // -----------------------
  // Helpers DOM / Estado
  // -----------------------
  const qs = (sel, root = document) => root.querySelector(sel);
  const qsa = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const state = {
    profissionais: [],
    procedimentos: [],
    tiposProcedimento: [],
    selectedProfissionalWallet: null,
  };

  const $loading = qs("#app-loading");

  function setLoading(on) {
    if (!$loading) return;
    $loading.classList.toggle("hidden", !on);
  }

  // Localiza um card pelo título <h2> e retorna refs úteis
  function getCardRefs(titleText) {
    const cards = qsa(".card");
    for (const card of cards) {
      const titleEl = qs(".card__header .card__title", card);
      if (titleEl && titleEl.textContent.trim() === titleText) {
        return {
          card,
          titleEl,
          descEl: qs(".card__header .card__description", card),
          scrollArea:
            qs(".card__content .scroll-area", card) ||
            qs(".card__content", card),
        };
      }
    }
    return null;
  }

  const cadastroCard = (() => {
    // único <form> da página
    const form = qs("form");
    const btn = form ? form.querySelector(".button--primary") : null;
    const errorsBox = qs("#form-errors");
    return { form, btn, errorsBox };
  })();

  const profissionaisCard = getCardRefs("Profissionais Cadastrados");
  const procedimentosCard = getCardRefs("Procedimentos Realizados");

  // -----------------------
  // Formatação de campos
  // -----------------------
  function formatCategoria(c) {
    if (!c) return "";
    if (c.toLowerCase() === "medico") return "Médico";
    if (c.toLowerCase() === "enfermeiro") return "Enfermeiro";
    return c;
  }

  function formatWallet(w) {
    if (!w || typeof w !== "string") return String(w ?? "");
    if (w.length <= 10) return w;
    return `${w.slice(0, 4)}...${w.slice(-4)}`;
  }

  function plural(n, s, p) {
    return n === 1 ? s : p;
  }

  // -----------------------
  // API
  // -----------------------
  async function apiGet(url) {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function apiPost(url, body) {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }

  async function loadProfissionais() {
    const result = await apiGet("/api/profissionais");
    if (!result?.success)
      throw new Error(result?.error || "Erro ao carregar profissionais");
    state.profissionais = Array.isArray(result.data) ? result.data : [];
  }

  async function loadProcedimentos() {
    const result = await apiGet("/api/procedimentos");
    if (!result?.success)
      throw new Error(result?.error || "Erro ao carregar procedimentos");
    const d = result.data || {};
    state.procedimentos = Array.isArray(d.procedimentos) ? d.procedimentos : [];
    state.tiposProcedimento = Array.isArray(d.tiposProcedimento)
      ? d.tiposProcedimento
      : [];
  }

  async function cadastrarProfissional(payload) {
    const result = await apiPost("/api/profissionais", payload);
    if (!result?.success)
      throw new Error(result?.error || "Erro ao cadastrar profissional");
    // adiciona ao estado e retorna item criado
    const novo = result.data;
    state.profissionais.push(novo);
    return novo;
  }

  // -----------------------
  // Render: Profissionais
  // -----------------------
  function renderProfissionais() {
    if (!profissionaisCard) return;

    const total = state.profissionais.length;
    if (profissionaisCard.descEl) {
      profissionaisCard.descEl.textContent = `${total} ${plural(total, "profissional", "profissionais")} ${plural(total, "cadastrado", "cadastrados")}`;
    }

    const listEl = profissionaisCard.scrollArea;
    if (!listEl) return;

    if (total === 0) {
      listEl.innerHTML = `<div class="text-center py-8 muted">Nenhum profissional cadastrado ainda</div>`;
      return;
    }

    listEl.innerHTML = state.profissionais
      .map((p) => {
        const isSelected = state.selectedProfissionalWallet === p.wallet;
        const badgeCls = p.ativo ? "badge--default" : "badge--secondary";
        return `
          <article class="card card--clickable ${isSelected ? "card--selected" : ""}" data-wallet="${p.wallet || ""}">
            <div class="card__content p-4">
              <div class="row between start gap-2">
                <div class="stack-2 flex-1">
                  <div class="row start center gap-2">
                    <h3 class="text-sm strong">${escapeHtml(p.nome || "")}</h3>
                    <span class="badge ${badgeCls} text-xxs">${p.ativo ? "Ativo" : "Inativo"}</span>
                  </div>
                  <div class="meta text-xxs muted">
                    <div class="row between"><span>ID Hospital:</span><span class="mono">${escapeHtml(String(p.idLegado ?? ""))}</span></div>
                    <div class="row between"><span>Categoria:</span><span>${escapeHtml(formatCategoria(p.categoria))}</span></div>
                    <div class="row between"><span>Registro:</span><span class="mono">${escapeHtml(p.registro || "")}</span></div>
                    <div class="row between"><span>Carteira:</span><span class="mono break">${escapeHtml(formatWallet(p.wallet || ""))}</span></div>
                  </div>
                </div>
                <button class="button button--ghost button--sm text-xxs">Ver Procedimentos</button>
              </div>
            </div>
          </article>
        `;
      })
      .join("");

    // Delegação de clique para seleção de profissional
    listEl.addEventListener("click", onProfissionaisClick, { once: true });
  }

  function onProfissionaisClick(e) {
    const card = e.target.closest(".card.card--clickable");
    if (!card) return;
    const wallet = card.getAttribute("data-wallet");
    if (!wallet) return;
    state.selectedProfissionalWallet = wallet;
    renderProfissionais(); // re-render para aplicar card--selected
    renderProcedimentos(); // mostra procedimentos do selecionado
    // reanexar o listener de delegação (foi once:true)
    profissionaisCard.scrollArea.addEventListener(
      "click",
      onProfissionaisClick,
      { once: true },
    );
  }

  function getSelectedProfissional() {
    return (
      state.profissionais.find(
        (p) => p.wallet === state.selectedProfissionalWallet,
      ) || null
    );
  }

  // -----------------------
  // Render: Procedimentos
  // -----------------------
  function getTipoProcedimentoById(id) {
    return state.tiposProcedimento.find((t) => t.id === id);
  }

  function renderProcedimentos() {
    if (!procedimentosCard) return;
    const listEl = procedimentosCard.scrollArea;
    if (!listEl) return;

    const prof = getSelectedProfissional();

    if (!prof) {
      // Se nada selecionado, limpa a área e descrição
      if (procedimentosCard.descEl) {
        procedimentosCard.descEl.textContent =
          "Selecione um profissional para visualizar os procedimentos";
      }
      listEl.innerHTML = `<div class="text-center py-8 muted">Nenhum profissional selecionado</div>`;
      return;
    }

    const doProf = state.procedimentos.filter(
      (proc) => String(proc.id_profissional) === String(prof.wallet),
    );
    const count = doProf.length;

    if (procedimentosCard.descEl) {
      procedimentosCard.descEl.textContent = `Profissional: ${prof.nome} • ${count} ${plural(count, "procedimento", "procedimentos")}`;
    }

    if (count === 0) {
      listEl.innerHTML = `<div class="text-center py-8 muted">Nenhum procedimento encontrado para este profissional</div>`;
      return;
    }

    listEl.innerHTML = doProf
      .map((procedimento) => {
        const tipo = getTipoProcedimentoById(procedimento.tipo_procedimento_id);
        const titulo =
          tipo?.tipo || `Procedimento ${procedimento.tipo_procedimento_id}`;
        const badgeStatus = procedimento.cadastrado
          ? "badge--default"
          : "badge--secondary";
        const interc = procedimento.intercorrencia
          ? `<span class="badge badge--destructive text-xxs">Intercorrência</span>`
          : "";
        const materiais = Array.isArray(procedimento.materiais)
          ? procedimento.materiais
          : [];

        return `
          <article class="card card--accent-left">
            <div class="card__content p-4">
              <div class="stack-3">
                <div class="row between start">
                  <div>
                    <h3 class="text-sm strong">${escapeHtml(titulo)}</h3>
                    <p class="text-xxs muted">ID: ${escapeHtml(String(procedimento.id))}</p>
                  </div>
                  <div class="row gap-2">
                    <span class="badge ${badgeStatus} text-xxs">${procedimento.cadastrado ? "Cadastrado" : "Pendente"}</span>
                    ${interc}
                  </div>
                </div>

                <hr class="separator" />

                <div class="grid grid--2 gap-3 text-xxs">
                  <div class="stack-2">
                    <div>
                      <span class="muted">Paciente:</span>
                      <p class="mono break">${escapeHtml(formatWallet(String(procedimento.id_paciente)))}</p>
                    </div>
                    <div>
                      <span class="muted">Profissional:</span>
                      <p class="mono break">${escapeHtml(formatWallet(String(procedimento.id_profissional)))}</p>
                    </div>
                  </div>
                  <div class="stack-2">
                    <div>
                      <span class="muted">Procedimento Anterior:</span>
                      <p class="mono">${escapeHtml(String(procedimento.id_procedimento_anterior || "Nenhum"))}</p>
                    </div>
                    <div>
                      <span class="muted">Tipo ID:</span>
                      <p class="mono">${escapeHtml(String(procedimento.tipo_procedimento_id))}</p>
                    </div>
                  </div>
                </div>

                ${
                  materiais.length > 0
                    ? `
                  <hr class="separator" />
                  <div>
                    <h4 class="text-xxs muted mb-2">Materiais Utilizados:</h4>
                    <div class="grid grid--auto-fit gap-2">
                      ${materiais
                        .map(
                          (m) => `
                        <div class="chip">
                          <div class="mono">ID: ${escapeHtml(String(m.material_id))}</div>
                          <div class="muted">Qtd: ${escapeHtml(String(m.quantidade))}</div>
                        </div>
                      `,
                        )
                        .join("")}
                    </div>
                  </div>
                `
                    : ""
                }
              </div>
            </div>
          </article>
        `;
      })
      .join("");
  }

  // -----------------------
  // Form: Cadastro
  // -----------------------
  function getFormData() {
    const nome = qs("#nome")?.value?.trim() || "";
    const idLegado = qs("#idLegado")?.value?.trim() || "";
    const categoria = qs("#categoria")?.value || "";
    const registro = qs("#registro")?.value?.trim() || "";
    const wallet = qs("#wallet")?.value?.trim() || "";
    return { nome, idLegado, categoria, registro, wallet };
  }

  function validateProfissionalForm(form) {
    const errs = [];
    if (!form.nome) errs.push("Nome é obrigatório.");
    if (!form.idLegado) errs.push("ID do Hospital é obrigatório.");
    if (!form.categoria) errs.push("Categoria é obrigatória.");
    if (!form.registro) errs.push("Registro profissional é obrigatório.");
    if (!form.wallet) errs.push("Endereço da carteira é obrigatório.");
    // simples validação de carteira
    if (form.wallet && !/^0x[a-fA-F0-9]{4,}$/.test(form.wallet)) {
      errs.push("Endereço de carteira parece inválido.");
    }
    return errs;
    // Ajuste conforme suas regras reais de validação.
  }

  function showFormErrors(list) {
    if (!cadastroCard.errorsBox) return;
    if (!Array.isArray(list) || list.length === 0) {
      cadastroCard.errorsBox.classList.add("hidden");
      cadastroCard.errorsBox.innerHTML = "";
      return;
    }
    cadastroCard.errorsBox.innerHTML = `
      <ul class="alert__list">
        ${list.map((e) => `<li>${escapeHtml(e)}</li>`).join("")}
      </ul>
    `;
    cadastroCard.errorsBox.classList.remove("hidden");
  }

  function clearForm() {
    const form = cadastroCard.form;
    if (!form) return;
    form.reset();
    showFormErrors([]);
  }

  async function onSubmitCadastro(e) {
    e.preventDefault();
    console.log("hi")
    showFormErrors([]);
    const btn = cadastroCard.btn;
    try {
      const data = getFormData();
      const errs = validateProfissionalForm(data);
      if (errs.length) {
        showFormErrors(errs);
        return;
      }

      // feedback no botão
      let originalLabel = "";
      if (btn) {
        originalLabel = btn.textContent;
        btn.textContent = "Cadastrando...";
        btn.disabled = true;
      }

      const created = await cadastrarProfissional({
        nome: data.nome,
        idLegado: data.idLegado,
        categoria: data.categoria == "Medico" ? 0 : 1,
        registro: data.registro,
        wallet: data.wallet,
      });

      // Atualiza UI
      renderProfissionais();

      // Seleciona automaticamente o recém-cadastrado
      state.selectedProfissionalWallet = created?.wallet || data.wallet;
      renderProfissionais();
      renderProcedimentos();

      clearForm();
      showToast("Sucesso", "Profissional cadastrado com sucesso.");

      if (btn) {
        btn.textContent = originalLabel || "Cadastrar Profissional";
        btn.disabled = false;
      }
    } catch (err) {
      console.error(err);
      showToast(
        "Erro",
        err instanceof Error ? err.message : "Erro ao cadastrar profissional.",
        "destructive",
      );
      if (btn) {
        btn.textContent = "Cadastrar Profissional";
        btn.disabled = false;
      }
    }
  }

  // -----------------------
  // Toast simples (injetado)
  // -----------------------
  function ensureToastRoot() {
    let root = qs("#toast-root");
    if (!root) {
      root = document.createElement("div");
      root.id = "toast-root";
      root.style.position = "fixed";
      root.style.top = "16px";
      root.style.right = "16px";
      root.style.display = "grid";
      root.style.gap = "10px";
      root.style.zIndex = "9999";
      document.body.appendChild(root);
    }
    return root;
  }

  function showToast(title, msg, variant = "default", timeout = 2800) {
    const root = ensureToastRoot();
    const el = document.createElement("div");
    el.style.minWidth = "260px";
    el.style.maxWidth = "360px";
    el.style.padding = "12px 14px";
    el.style.borderRadius = "10px";
    el.style.border = "1px solid var(--border)";
    el.style.boxShadow = "var(--shadow)";
    el.style.background =
      variant === "destructive"
        ? "color-mix(in oklab, var(--destructive), #fff 85%)"
        : "var(--card)";
    el.style.color =
      variant === "destructive"
        ? "color-mix(in oklab, var(--destructive), #000 25%)"
        : "var(--foreground)";
    el.innerHTML = `
      <div style="font-weight:700;margin-bottom:4px">${escapeHtml(title)}</div>
      <div style="font-size:.9rem;color:var(--muted-foreground)">${escapeHtml(msg)}</div>
    `;
    root.appendChild(el);
    setTimeout(() => {
      el.style.transition = "opacity .2s ease, transform .2s ease";
      el.style.opacity = "0";
      el.style.transform = "translateY(-6px)";
      setTimeout(() => el.remove(), 250);
    }, timeout);
  }

  // -----------------------
  // Segurança mínima para HTML dinâmico
  // -----------------------
  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  // -----------------------
  // Inicialização
  // -----------------------
  async function init() {
    // Garantir que o form tenha o evento de submit
    if (cadastroCard.form) {
      cadastroCard.form.addEventListener("submit", onSubmitCadastro);
    }

    setLoading(true);
    try {
      await Promise.all([loadProfissionais(), loadProcedimentos()]);
      // Seleciona automaticamente o primeiro profissional (se existir)
      if (state.profissionais.length > 0) {
        state.selectedProfissionalWallet = state.profissionais[0].wallet;
      }
      renderProfissionais();
      renderProcedimentos();
    } catch (err) {
      console.error(err);
      showToast(
        "Erro",
        err instanceof Error ? err.message : "Falha ao carregar dados.",
        "destructive",
      );
      // Render mínimos vazios
      renderProfissionais();
      renderProcedimentos();
    } finally {
      setLoading(false);
    }
  }

  document.addEventListener("DOMContentLoaded", init);
})();
