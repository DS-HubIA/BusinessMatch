(() => {
  const API = "";
  let AUTH = localStorage.getItem("bm_token") || null;
  function setAuth(t){ AUTH=t; localStorage.setItem("bm_token",t); }
  function hdr(){ return AUTH ? { Authorization: "Bearer " + AUTH } : {}; }
  async function req(p,o){ const r=await fetch(API+p,{headers:{"Content-Type":"application/json",...hdr(),...(o&&o.headers||{})},...(o||{})}); if(!r.ok) throw new Error(await r.text()); return r.json(); }
  window.apiRegister = async (payload)=>{ const { token } = await req("/api/auth/register",{method:"POST",body:JSON.stringify(payload)}); setAuth(token); return true; }
  window.apiLogin = async (payload)=>{ const { token } = await req("/api/auth/login",{method:"POST",body:JSON.stringify(payload)}); setAuth(token); return true; }
  window.apiCreateBusiness = async (payload)=> req("/api/opportunities",{method:"POST",body:JSON.stringify(payload)});
  window.apiListBusinesses = async (q)=> req("/api/opportunities" + (q||""));
})();
