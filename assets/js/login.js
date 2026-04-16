document.addEventListener('DOMContentLoaded',()=>{
    const fL=document.getElementById('form-login'), fRS=document.getElementById('form-recuperar-senha'), bTS=document.querySelector('.toggle-senha');
    const dH=document.querySelector('.dropdown-header'), dL=document.getElementById('dropdown-perfil-list'), dI=document.querySelectorAll('.dropdown-item');
    if(fL) fL.addEventListener('submit',handleLogin);
    if(fRS) fRS.addEventListener('submit',handleRecuperarSenha);
    if(bTS) bTS.addEventListener('click',e=>{e.preventDefault();const i=document.getElementById('senha'),ic=e.target.closest('.toggle-senha').querySelector('i');i.type=i.type==='password'?'text':'password';ic.classList.toggle('fa-eye');ic.classList.toggle('fa-eye-slash');});
    if(dH){
        dH.addEventListener('click',e=>{e.stopPropagation();dL.style.display=dL.style.display==='none'?'block':'none';dH.classList.toggle('open');});
        dI.forEach(item=>item.addEventListener('click',e=>{e.stopPropagation();const v=item.getAttribute('data-value');document.getElementById('perfil').value=v;document.getElementById('perfil-display').textContent=item.textContent;dL.style.display='none';dH.classList.remove('open');dH.classList.remove('is-placeholder');dI.forEach(it=>it.classList.remove('selected'));item.classList.add('selected');}));
        document.addEventListener('click',()=>{dL.style.display='none';dH.classList.remove('open');});
    }
    document.querySelectorAll('input[data-validar]').forEach(i=>i.addEventListener('blur',()=>validarFormulario(i.form)));
});

async function handleLogin(e){
    e.preventDefault();
    if(!validarFormulario(this)){mostrarNotificacao('Corrija os erros','erro');return;}
    if(!document.getElementById('perfil').value){mostrarNotificacao('Selecione um perfil','erro');return;}
    const b=this.querySelector('button[type="submit"]');b.disabled=true;b.textContent='Entrando...';
    try{
        const r=await fetchAPI('POST','/login',{email:document.getElementById('email').value.trim(),senha:document.getElementById('senha').value});
        if(r&&r.token){setToken(r.token);setUser(r.usuario);mostrarNotificacao('Login OK!','sucesso',1500);setTimeout(()=>window.location.href='/pages/perfil.html',1000);}
    }catch(e){mostrarNotificacao(e.message||'Erro login','erro');}finally{b.disabled=false;b.textContent='Entrar';}
}

async function handleRecuperarSenha(e){
    e.preventDefault();
    if(!validarFormulario(this)){mostrarNotificacao('Corrija os erros','erro');return;}
    const b=this.querySelector('button[type="submit"]');b.disabled=true;b.textContent='Enviando...';
    try{
        const r=await fetchAPI('POST','/recuperar-senha',{email:document.getElementById('email-recuperar').value.trim(),nova_senha:document.getElementById('nova-senha').value});
        if(r){mostrarNotificacao('Senha atualizada!','sucesso',1500);setTimeout(()=>window.location.href='/pages/index.html',1000);}
    }catch(e){mostrarNotificacao(e.message||'Erro','erro');}finally{b.disabled=false;b.textContent='Recuperar';}
}
