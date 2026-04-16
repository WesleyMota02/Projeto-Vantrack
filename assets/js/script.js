document.addEventListener('DOMContentLoaded',()=>{
    const fCA=document.getElementById('form-cadastro-aluno'),fCM=document.getElementById('form-cadastro-motorista');
    if(fCA) fCA.addEventListener('submit',e=>handleCadastro(e,'aluno'));
    if(fCM) fCM.addEventListener('submit',e=>handleCadastro(e,'motorista'));
    document.querySelectorAll('input[data-validar]').forEach(i=>i.addEventListener('blur',()=>validarFormulario(i.form)));
    document.getElementById('cpf')?.addEventListener('input',aplicarMascaraCPF);
    document.getElementById('telefone')?.addEventListener('input',aplicarMascaraTelefone);
});

function aplicarMascaraCPF(e){
    let v=e.target.value.replace(/\D/g,'');
    if(v.length>11)v=v.substring(0,11);
    if(v.length>9)v=v.substring(0,3)+'.'+v.substring(3,6)+'.'+v.substring(6,9)+'-'+v.substring(9);
    else if(v.length>6)v=v.substring(0,3)+'.'+v.substring(3,6)+'.'+v.substring(6);
    else if(v.length>3)v=v.substring(0,3)+'.'+v.substring(3);
    e.target.value=v;
}

function aplicarMascaraTelefone(e){
    let v=e.target.value.replace(/\D/g,'');
    if(v.length>11)v=v.substring(0,11);
    if(v.length>6)v='('+v.substring(0,2)+') '+v.substring(2,7)+'-'+v.substring(7);
    else if(v.length>2)v='('+v.substring(0,2)+') '+v.substring(2);
    e.target.value=v;
}

async function handleCadastro(e,tp){
    e.preventDefault();
    const f=e.target;
    if(!validarFormulario(f)){mostrarNotificacao('Corrija os erros','erro');return;}
    const s=document.getElementById('senha').value,cs=document.getElementById('confirmar-senha').value;
    if(s!==cs){mostrarNotificacao('Senhas não conferem','erro');return;}
    const b=f.querySelector('button[type="submit"]');b.disabled=true;b.textContent='Cadastrando...';
    try{
        const r=await fetchAPI('POST','/cadastro',{
            email:document.getElementById('email').value.trim(),
            cpf:document.getElementById('cpf').value,
            nome:document.getElementById('nome').value.trim(),
            telefone:document.getElementById('telefone').value,
            cidade:document.getElementById('cidade').value.trim(),
            tipo_perfil:tp,
            senha:s
        });
        if(r&&r.id){mostrarNotificacao('Cadastro OK! Redirecionando...','sucesso',1500);setTimeout(()=>window.location.href='/pages/index.html',1000);}
    }catch(e){mostrarNotificacao(e.message||'Erro cadastro','erro');}finally{b.disabled=false;b.textContent=tp==='aluno'?'Cadastrar como Aluno':'Cadastrar como Motorista';}
}
