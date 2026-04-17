document.addEventListener('DOMContentLoaded',()=>{
    const fCA=document.getElementById('form-cadastro-aluno'),fCM=document.getElementById('form-cadastro-motorista');
    if(fCA) fCA.addEventListener('submit',e=>handleCadastro(e,'aluno'));
    if(fCM) fCM.addEventListener('submit',e=>handleCadastro(e,'motorista'));
    document.querySelectorAll('input[data-validar]').forEach(i=>i.addEventListener('blur',()=>validarFormulario(i.form)));
    document.getElementById('cpf')?.addEventListener('input',aplicarMascaraCPF);
    document.getElementById('telefone')?.addEventListener('input',aplicarMascaraTelefone);
    
    // Toggle de senha - cadastro
    document.querySelectorAll('.toggle-senha').forEach(btn=>{
        btn.addEventListener('click',e=>{
            e.preventDefault();
            const input=btn.parentElement.querySelector('input[type="password"], input[type="text"]');
            const icon=btn.querySelector('i');
            if(input){
                const isPassword=input.type==='password';
                input.type=isPassword?'text':'password';
                icon?.classList.toggle('fa-eye');
                icon?.classList.toggle('fa-eye-slash');
                console.log(`[TOGGLE] Senha ${isPassword?'visível':'ocultada'}`);
            }
        });
    });
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
    
    // Validar formulário
    if(!validarFormulario(f)){
        console.log('[CADASTRO] Validação falhou');
        mostrarNotificacao('Corrija os erros','erro');
        return;
    }
    
    // Validar senhas
    const s=document.getElementById('senha').value,cs=document.getElementById('confirmar-senha').value;
    if(s!==cs){
        console.log('[CADASTRO] Senhas não conferem');
        mostrarNotificacao('Senhas não conferem','erro');
        return;
    }
    
    // Preparar dados - REMOVER MÁSCARAS
    const cpfSemMascara=document.getElementById('cpf').value.replace(/\D/g,'');
    const telefoneSemMascara=document.getElementById('telefone').value.replace(/\D/g,'');
    
    console.log('[CADASTRO] Iniciando...');
    console.log(`  CPF: ${cpfSemMascara} (${cpfSemMascara.length} dígitos)`);
    console.log(`  Telefone: ${telefoneSemMascara} (${telefoneSemMascara.length} dígitos)`);
    
    const b=f.querySelector('button[type="submit"]');
    b.disabled=true;
    b.textContent='Cadastrando...';
    
    try{
        const payload={
            email:document.getElementById('email').value.trim(),
            cpf:cpfSemMascara,
            nome:document.getElementById('nome').value.trim(),
            telefone:telefoneSemMascara,
            cidade:document.getElementById('cidade').value.trim(),
            tipo_perfil:tp,
            senha:s
        };
        
        console.log('[CADASTRO] Payload:', payload);
        
        const r=await fetchAPI('POST','/cadastro',payload);
        
        if(r&&r.id){
            console.log('[CADASTRO] Sucesso:', r);
            mostrarNotificacao('Cadastro OK! Redirecionando...','sucesso',1500);
            setTimeout(()=>window.location.href='/pages/index.html',1500);
        }else{
            console.log('[CADASTRO] Resposta inválida:', r);
            mostrarNotificacao('Erro ao cadastrar','erro');
        }
    }catch(e){
        console.error('[CADASTRO] Erro:', e);
        mostrarNotificacao(e.message||'Erro ao cadastrar','erro');
    }finally{
        b.disabled=false;
        b.textContent=tp==='aluno'?'Cadastrar como Aluno':'Cadastrar como Motorista';
    }
}
