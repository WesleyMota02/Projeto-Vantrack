// Mostrar / esconder senha
const campoSenha = document.getElementById("senha");
const botaoToggle = document.querySelector(".toggle-senha");
const iconeSenha = document.getElementById("icone-senha");

if (botaoToggle && campoSenha && iconeSenha) {
    botaoToggle.addEventListener("click", () => {
        const tipoAtual = campoSenha.getAttribute("type");

        if (tipoAtual === "password") {
            campoSenha.setAttribute("type", "text");
            iconeSenha.textContent = "visibility_off";
        } else {
            campoSenha.setAttribute("type", "password");
            iconeSenha.textContent = "visibility";
        }
    });
}

// Apenas para exemplo: evita que a página recarregue ao enviar
const formCadastro = document.getElementById("form-cadastro");

if (formCadastro) {
    formCadastro.addEventListener("submit", (event) => {
        event.preventDefault();

        // Aqui você pode depois integrar com seu back-end / API
        alert("Cadastro enviado (exemplo). Aqui você conecta com o back-end.");
    });
}
