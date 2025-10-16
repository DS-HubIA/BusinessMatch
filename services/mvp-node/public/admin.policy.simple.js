(function(){
  // Lê a política salva no localStorage
  window.getPrivacyPolicy = function(){
    return localStorage.getItem('privacyPolicy') || 'Escreva aqui a Política de Privacidade do Clube de Negócios Sebrae…';
  };

  // Injeta um botão "Editar Política (local)" no ADM (engrenagem)
  function mountAdminButton(){
    if (document.getElementById('btnEditPrivacyLocal')) return;
    // tente achar a área do ADM; ajuste o seletor se necessário
    const gearArea = document.querySelector('#adminMenu, .admin-menu, .settings-menu, [data-admin], [data-settings]')
      || document.querySelector('header, nav');

    if (!gearArea) return;

    const btn = document.createElement('button');
    btn.id = 'btnEditPrivacyLocal';
    btn.className = 'btn btn-sm btn-outline';
    btn.style.marginLeft = '8px';
    btn.textContent = 'Editar Política (local)';
    btn.addEventListener('click', openEditor);
    gearArea.appendChild(btn);
  }

  // Modal simples p/ editar e salvar no localStorage
  function openEditor(){
    const modal = document.createElement('div');
    modal.id = 'policyModalLocal';
    modal.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
    modal.innerHTML = `
      <div style="background:#fff;max-width:720px;width:92%;border-radius:12px;padding:16px;box-shadow:0 10px 30px rgba(0,0,0,.2)">
        <h3 style="margin:0 0 8px">Política de Privacidade</h3>
        <textarea id="policyTextareaLocal" style="width:100%;min-height:260px;border:1px solid #ddd;border-radius:8px;padding:10px;"></textarea>
        <div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">
          <button id="policyRestore" class="btn btn-light">Restaurar padrão</button>
          <button id="policyCancel" class="btn btn-light">Cancelar</button>
          <button id="policySave" class="btn btn-primary">Salvar (local)</button>
        </div>
      </div>`;
    document.body.appendChild(modal);

    const ta = modal.querySelector('#policyTextareaLocal');
    const defaultText = 'Escreva aqui a Política de Privacidade do Clube de Negócios Sebrae…';
    ta.value = window.getPrivacyPolicy();

    const close = () => modal.remove();
    modal.addEventListener('click', (e)=>{ if(e.target===modal) close(); });
    modal.querySelector('#policyCancel').addEventListener('click', close);
    modal.querySelector('#policyRestore').addEventListener('click', ()=>{
      ta.value = defaultText;
    });
    modal.querySelector('#policySave').addEventListener('click', ()=>{
      const v = (ta.value || '').trim();
      if (v.length < 10){ alert('Texto muito curto.'); return; }
      localStorage.setItem('privacyPolicy', v);
      alert('Política salva neste navegador (MVP local).');
      close();
    });
  }

  // Expor helper para páginas que exibem a política (ex.: register)
  window.renderPrivacyPolicyInto = function(selector){
    const el = document.querySelector(selector);
    if (el) el.textContent = window.getPrivacyPolicy();
  };

  function init(){
    mountAdminButton();
    // tenta montar de novo após cliques de navegação interna (se SPA)
    document.addEventListener('click', (e)=>{
      if (e.target.closest && e.target.closest('.settings, .admin, [data-admin], [data-settings]')) {
        setTimeout(mountAdminButton, 0);
      }
    });
  }
  (document.readyState === 'loading') ? document.addEventListener('DOMContentLoaded', init) : init();
})();
