(function(){
  function openEditor(initText){
    const modal = document.createElement('div');
    modal.id = 'policyModal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
    modal.innerHTML = `
      <div style="background:#fff;max-width:720px;width:92%;border-radius:12px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.2)">
        <h3 style="margin:0 0 8px">Política de Privacidade</h3>
        <textarea id="policyTextarea" style="width:100%;min-height:260px;border:1px solid #ddd;border-radius:8px;padding:10px;"></textarea>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
          <button id="policyCancel" class="btn btn-light">Cancelar</button>
          <button id="policySave" class="btn btn-primary">Salvar</button>
        </div>
      </div>`;
    document.body.appendChild(modal);
    const ta = modal.querySelector("#policyTextarea");
    ta.value = initText || "";

    const close = () => { modal.remove(); };
    modal.addEventListener("click", (e)=>{ if(e.target===modal) close(); });
    modal.querySelector("#policyCancel").addEventListener("click", close);
    modal.querySelector("#policySave").addEventListener("click", async ()=>{
      const policy = ta.value.trim();
      if (policy.length < 10) { alert("Texto muito curto."); return; }
      const secret = prompt("Digite o ADMIN_SECRET para confirmar a atualização:");
      if (!secret) return;

      try {
        const r = await fetch("/api/admin/policy", {
          method: "PUT",
          headers: { "Content-Type": "application/json", "X-Admin-Secret": secret },
          body: JSON.stringify({ policy })
        });
        if(!r.ok){
          const t = await r.text();
          throw new Error(t);
        }
        alert("Política atualizada!");
        close();
      } catch(err){
        alert("Erro ao salvar: " + err.message);
      }
    });
  }

  async function loadAndOpen(){
    try{
      const r = await fetch("/api/policy");
      const j = await r.json();
      openEditor(j.policy || "");
    }catch(e){
      openEditor("Escreva aqui a política…");
    }
  }

  function init(){
    // procura o link / botão já existente de "Política de Privacidade" e intercepta
    const candidates = Array.from(document.querySelectorAll("a,button"))
      .filter(el => /pol[íi]tica.+privacidade/i.test(el.textContent || ""));
    if (candidates.length){
      const link = candidates[0];
      link.addEventListener("click", (ev)=>{
        // se o link original abrir outra página, bloqueamos e abrimos o editor
        ev.preventDefault();
        loadAndOpen();
      }, { capture:true });
    } else {
      // fallback: cria um botão no topo
      const header = document.querySelector("header, nav, .admin, .settings") || document.body;
      const btn = document.createElement("button");
      btn.textContent = "Política de Privacidade";
      btn.className = "btn btn-sm btn-outline";
      btn.style.marginLeft = "8px";
      btn.addEventListener("click", loadAndOpen);
      header.appendChild(btn);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
