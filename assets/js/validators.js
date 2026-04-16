function validarEmail(e) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e); }
function validarCPF(c) { return c.replace(/\D/g,'').length === 11; }
function validarTelefone(t) { return /^[0-9]{10,11}$/.test(t.replace(/\D/g,'')); }
function validarSenha(s) {
    if (s.length < 8) return { valido: false, erro: 'Mínimo 8 caracteres' };
    if (!/[A-Z]/.test(s)) return { valido: false, erro: 'Precisa de maiúscula' };
    if (!/[a-z]/.test(s)) return { valido: false, erro: 'Precisa de minúscula' };
    if (!/[0-9]/.test(s)) return { valido: false, erro: 'Precisa de número' };
    return { valido: true };
}
function validarNome(n) { return n.trim().length >= 3 && /^[a-zA-Zá-ý\s]+$/.test(n); }
function validarCidade(c) { return c.trim().length >= 3 && /^[a-zA-Zá-ý\s]+$/.test(c); }
function validarCoordenadas(lat, lng) { const la=parseFloat(lat), lo=parseFloat(lng); return !isNaN(la)&&!isNaN(lo)&&la>=-90&&la<=90&&lo>=-180&&lo<=180; }
function validarHorario(h) { return /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/.test(h); }
function validarCapacidade(c) { const cap=parseInt(c); return !isNaN(cap)&&cap>0&&cap<=100; }
function validarAno(a) { const an=parseInt(a), anoAt=new Date().getFullYear(); return !isNaN(an)&&an>=2000&&an<=anoAt; }
function mostrarErroFormulario(i, m) { i.classList.add('input-erro'); }
function limparErroFormulario(i) { i.classList.remove('input-erro'); }
function validarFormulario(f) {
    let v=true;
    f.querySelectorAll('input[data-validar]').forEach(i=>{
        const t=i.getAttribute('data-validar'); let e='';
        if (i.hasAttribute('required')&&!i.value.trim()) e='Obrigatório';
        else if (i.value.trim()) {
            switch(t) {
                case 'email': if(!validarEmail(i.value)) e='Email inválido'; break;
                case 'cpf': if(!validarCPF(i.value)) e='CPF inválido'; break;
                case 'telefone': if(!validarTelefone(i.value)) e='Telefone inválido'; break;
                case 'senha': const rs=validarSenha(i.value); if(!rs.valido) e=rs.erro; break;
                case 'nome': if(!validarNome(i.value)) e='Nome inválido'; break;
                case 'cidade': if(!validarCidade(i.value)) e='Cidade inválida'; break;
                case 'horario': if(!validarHorario(i.value)) e='Formato HH:MM'; break;
                case 'capacidade': if(!validarCapacidade(i.value)) e='1-100'; break;
                case 'ano': if(!validarAno(i.value)) e='2000-atual'; break;
            }
        }
        if (e) { mostrarErroFormulario(i, e); v=false; } else limparErroFormulario(i);
    });
    return v;
}
