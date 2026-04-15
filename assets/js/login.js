const LoginModule = {
  init: () => {
    const form = document.getElementById("form-login");
    const emailInput = document.getElementById("email");
    const senhaInput = document.getElementById("senha");

    if (!form || !emailInput || !senhaInput) return;

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const email = Validators.sanitizeInput(emailInput.value);
      const senha = senhaInput.value;

      if (!Validators.required(email) || !Validators.required(senha)) {
        UIFeedback.showWarning("Por favor, preencha todos os campos!");
        return;
      }

      if (!Validators.email(email)) {
        UIFeedback.showError("E-mail inválido.");
        return;
      }

      window.location.href = "gps.html";
    });
  }
};

document.addEventListener("DOMContentLoaded", LoginModule.init);
