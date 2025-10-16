(() => {
  const API = "";
  let AUTH = localStorage.getItem("bm_token") || null;

  function setAuth(t){ AUTH=t; localStorage.setItem("bm_token",t); }
  function hdr(){ return AUTH ? { Authorization: "Bearer " + AUTH } : {}; }

  async function req(path, opts = {}) {
    const r = await fetch(API + path, {
      method: opts.method || "GET",
      headers: { "Content-Type": "application/json", ...hdr(), ...(opts.headers || {}) },
      body: opts.body ? JSON.stringify(opts.body) : undefined
    });
    if (!r.ok) throw new Error(await r.text());
    return r.json();
  }

  // Auth
  window.apiRegister = async ({ name, email, password }) => {
    const { token } = await req("/api/auth/register", { method: "POST", body: { name, email, password } });
    setAuth(token);
    return true;
  };
  window.apiLogin = async ({ email, password }) => {
    const { token } = await req("/api/auth/login", { method: "POST", body: { email, password } });
    setAuth(token);
    return true;
  };

  // Oportunidades
  window.apiCreateBusiness = async (payload) => {
    return req("/api/opportunities", { method: "POST", body: payload });
  };
  window.apiListBusinesses = async (query = {}) => {
    const qs = new URLSearchParams(query).toString();
    return req("/api/opportunities" + (qs ? `?${qs}` : ""));
  };

  // Adapter para seu HTML atual
  async function hydrateFront() {
    try {
      const items = await window.apiListBusinesses();
      // Normaliza para um formato comum que costuma existir no seu front
      const normalized = items.map(x => ({
        id: x.id,
        type: x.type,
        category: x.category,
        title: x.title,
        description: x.description,
        image: x.image_url || "",
        tags: Array.isArray(x.tags) ? x.tags : [],
        contact: x.contact || "", // pode vir vazio (sem join)
        phone: x.phone || "",
        userAvatar: x.user_avatar || "",
        location: x.location || ""
      }));
      if (typeof window.businessOpportunities !== "undefined") {
        window.businessOpportunities = normalized;
      }
      if (typeof window.renderCards === "function") window.renderCards();
      if (typeof window.updateStats === "function") window.updateStats();
      // fallback simples se seu HTML não tem funções globais
      if (typeof window.renderCards !== "function") {
        const el = document.getElementById("app");
        if (el) el.innerHTML = `<h2>Oportunidades</h2>` + normalized.map(c => `
          <div style="border:1px solid #ddd;padding:8px;margin:8px 0">
            <b>${c.type}</b> • ${c.category}<br>${c.title}<br>${c.description}<br>
            <small>${c.location || ""}</small>
          </div>`).join("");
      }
    } catch (e) {
      console.warn("Falha ao carregar oportunidades:", e);
    }
  }

  window.addEventListener("DOMContentLoaded", hydrateFront);
})();
