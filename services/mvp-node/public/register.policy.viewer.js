(function(){
  function getPolicyText(){
    return localStorage.getItem('privacyPolicy')
      || 'Política de Privacidade — (defina um texto no ADM > Editar Política (local)).';
  }

  function openPolicyModal(){
    const overlay = document.createElement('div');
    overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
    overlay.innerHTML = `
      <div style="background:#fff;max-width:800px;width:92%;max-height:80vh;overflow:auto;border-radius:12px;box-shadow:0 10px 30px rgba(0,0,0,.2);">
        <div style="padding:18px 18px 8px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;align-items:center">
          <h3 style="margin:0;font-size:1.1rem">Política de Privacidade</h3>
          <button id="policyCloseBtn" class="btn btn-sm btn-light" style="min-width:80px">Fechar</button>
        </div>
        <div style="padding:16px;white-space:pre-wrap;line-height:1.5;font-size:0.95rem" id="policyBody"></div>
      </div>`;
    document.body.appendChild(overlay);
    overlay.querySelector('#policyBody').textContent = getPolicyText();

    const close = () => overlay.remove();
    overlay.addEventListener('click', (e)=>{ if(e.target===overlay) close(); });
    overlay.querySelector('#policyCloseBtn').addEventListener('click', close);
  }

  function bindRegisterLinks(){
    // Procura links/botões com o texto “Política de Privacidade”
    const links = Array.from(document.querySelectorAll('a,button'))
      .filter(el => /pol[íi]tica.+privacidade/i.test(el.textContent || ''));
    links.forEach(a => {
      // Evita duplo-bind
      if (a.dataset.boundPolicyViewer) return;
      a.dataset.boundPolicyViewer = '1';
      a.addEventListener('click', (ev) => {
        // Só intercepta na página de registro (se tiver um container específico, ajuste aqui)
        // Heurística: se existe um form com email+senha na página
        const onRegister = !!document.querySelector('form input[type="email"], form input[type="password"]');
        if (!onRegister) return; // deixa seguir normal em outras páginas
        ev.preventDefault();
        openPolicyModal();
      });
    });
  }

  // Executa no load e reaplica após cliques (caso seja SPA)
  const init = () => { bindRegisterLinks(); };
  document.addEventListener('DOMContentLoaded', init);
  document.addEventListener('click', () => setTimeout(bindRegisterLinks, 0));
})();
