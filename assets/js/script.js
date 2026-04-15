const PasswordToggle = {
  init: () => {
    const toggleButtons = document.querySelectorAll(".toggle-senha");
    toggleButtons.forEach(button => {
      button.addEventListener("click", (e) => {
        e.preventDefault();
        const campo = button.parentElement.querySelector('input[type="password"], input[type="text"]');
        const icon = button.querySelector('i, span');
        
        if (!campo || !icon) return;

        const isPassword = campo.type === "password";
        campo.type = isPassword ? "text" : "password";
        
        const iconClass = isPassword ? "visibility_off" : "visibility";
        if (icon.tagName === "SPAN") {
          icon.textContent = iconClass;
        } else {
          icon.className = `far fa-eye${isPassword ? "-slash" : ""}`;
        }
      });
    });
  }
};

document.addEventListener("DOMContentLoaded", PasswordToggle.init);

const DropdownPerfil = {
  init: () => {
    const dropdown = document.querySelector(".dropdown-perfil");
    if (!dropdown) return;

    const toggle = dropdown.querySelector(".dropdown-perfil-toggle");
    const menu = dropdown.querySelector(".dropdown-perfil-menu");
    const items = menu.querySelectorAll("li[role='option']");
    const selectInput = document.getElementById("perfil");
    const textDisplay = dropdown.querySelector(".dropdown-perfil-text");

    toggle.addEventListener("click", (e) => {
      e.preventDefault();
      dropdown.classList.toggle("active");
      toggle.setAttribute("aria-expanded", dropdown.classList.contains("active"));
    });

    items.forEach(item => {
      item.addEventListener("click", () => {
        const value = item.getAttribute("data-value");
        
        items.forEach(i => i.classList.remove("selected", "placeholder"));
        
        if (value === "") {
          item.classList.add("placeholder");
          textDisplay.textContent = item.textContent;
          textDisplay.classList.add("is-placeholder");
          toggle.classList.remove("has-value");
        } else {
          item.classList.add("selected");
          textDisplay.textContent = item.textContent;
          textDisplay.classList.remove("is-placeholder");
          toggle.classList.add("has-value");
        }

        selectInput.value = value;
        dropdown.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      });
    });

    document.addEventListener("click", (e) => {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", (e) => {
      if (!dropdown.classList.contains("active")) return;

      if (e.key === "Escape") {
        dropdown.classList.remove("active");
        toggle.setAttribute("aria-expanded", "false");
      }
    });
  }
};

document.addEventListener("DOMContentLoaded", DropdownPerfil.init);

const InputMasks = {
  formatCPF: (value) => {
    const cleaned = value.replace(/\D/g, '').substring(0, 11);
    if (cleaned.length === 0) return '';
    if (cleaned.length <= 3) return cleaned;
    if (cleaned.length <= 6) return cleaned.replace(/(\d{3})(\d+)/, '$1.$2');
    if (cleaned.length <= 9) return cleaned.replace(/(\d{3})(\d{3})(\d+)/, '$1.$2.$3');
    return cleaned.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  },

  formatPhone: (value) => {
    const cleaned = value.replace(/\D/g, '').substring(0, 11);
    if (cleaned.length === 0) return '';
    if (cleaned.length <= 2) return cleaned;
    if (cleaned.length <= 7) return cleaned.replace(/(\d{2})(\d+)/, '($1) $2');
    return cleaned.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
  },

  init: () => {
    const cpfInput = document.getElementById('cpf');
    const phoneInput = document.getElementById('telefone');

    if (cpfInput) {
      cpfInput.addEventListener('input', (e) => {
        e.target.value = InputMasks.formatCPF(e.target.value);
      });
    }

    if (phoneInput) {
      phoneInput.addEventListener('input', (e) => {
        e.target.value = InputMasks.formatPhone(e.target.value);
      });
    }
  }
};

document.addEventListener("DOMContentLoaded", InputMasks.init);

const FormValidator = {
  validateRegistration: (formData) => {
    const errors = {};

    if (!Validators.name(formData.nome)) {
      errors.nome = "Nome inválido (mínimo 2 caracteres, máximo 100).";
    }
    if (!Validators.name(formData.sobrenome)) {
      errors.sobrenome = "Sobrenome inválido (mínimo 2 caracteres, máximo 100).";
    }
    if (!Validators.cpf(formData.cpf)) {
      errors.cpf = Config.ERROR_MESSAGES.INVALID_CPF;
    }
    if (!Validators.email(formData.email)) {
      errors.email = Config.ERROR_MESSAGES.INVALID_EMAIL;
    }
    if (!Validators.phone(formData.telefone)) {
      errors.telefone = Config.ERROR_MESSAGES.INVALID_PHONE;
    }
    if (!Validators.city(formData.cidade)) {
      errors.cidade = "Cidade inválida.";
    }
    if (!Validators.password(formData.senha)) {
      errors.senha = "Senha deve ter mínimo 8 caracteres, incluir maiúsculas, minúsculas e números.";
    }

    return Object.keys(errors).length === 0 ? null : errors;
  },

  validateLogin: (formData) => {
    const errors = {};

    if (!Validators.email(formData.email)) {
      errors.email = Config.ERROR_MESSAGES.INVALID_EMAIL;
    }
    if (Validators.isEmpty(formData.senha)) {
      errors.senha = Config.ERROR_MESSAGES.REQUIRED_FIELD;
    }
    if (Validators.isEmpty(formData.perfil)) {
      errors.perfil = "Selecione um perfil.";
    }

    return Object.keys(errors).length === 0 ? null : errors;
  },

  validateRecuperation: (formData) => {
    const errors = {};

    if (!Validators.email(formData.email)) {
      errors.email = Config.ERROR_MESSAGES.INVALID_EMAIL;
    }

    return Object.keys(errors).length === 0 ? null : errors;
  },

  showErrors: (form, errors) => {
    UIFeedback.clearAllErrors(form);
    Object.keys(errors).forEach(fieldName => {
      const field = form.querySelector(`[name="${fieldName}"], [id="${fieldName}"]`);
      if (field) {
        UIFeedback.showError(field, errors[fieldName]);
      }
    });
  }
};

// ------------------------------------------------------------------------------------

// ==========================================================
// ROTA: CADASTRO DE ALUNO COM VALIDAÇÕES
// ==========================================================
const formCadastro = document.getElementById("form-cadastro"); 

if (formCadastro) {
    formCadastro.addEventListener("submit", async (event) => {
        event.preventDefault();
        UIFeedback.clearAllErrors(formCadastro);

        const formData = {
            nome: document.getElementById('nome')?.value.trim() || '',
            sobrenome: document.getElementById('sobrenome')?.value.trim() || '',
            cpf: document.getElementById('cpf')?.value.trim() || '',
            email: document.getElementById('email')?.value.trim() || '',
            telefone: document.getElementById('telefone')?.value.trim() || '',
            cidade: document.getElementById('cidade')?.value.trim() || '',
            senha: document.getElementById('senha')?.value || ''
        };

        const errors = FormValidator.validateRegistration(formData);
        if (errors) {
            FormValidator.showErrors(formCadastro, errors);
            UIFeedback.showWarning("Verifique os erros no formulário.");
            return;
        }

        console.log("Dados validados e prontos para o backend: ", formData);

        const submitButton = formCadastro.querySelector('button[type="submit"]');
        UIFeedback.setLoading(submitButton, true);
        submitButton.setAttribute('data-original-text', 'Cadastrar');

        try {
            const response = await fetch(`${Config.API_BASE_URL}${Config.ENDPOINTS.ALUNOS_CADASTRAR}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                UIFeedback.showSuccess(result.message);
                formCadastro.reset();
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                const errorMsg = result.message || 'Falha no cadastro.';
                UIFeedback.showError(errorMsg);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            UIFeedback.showError(Config.ERROR_MESSAGES.NETWORK_ERROR);
        } finally {
            UIFeedback.setLoading(submitButton, false);
        }
    });
}

// ==========================================================
// ROTA: CADASTRO DE MOTORISTA COM VALIDAÇÕES
// ==========================================================
const formMotorista = document.getElementById("form-cadastro-motorista"); 

if (formMotorista) {
    formMotorista.addEventListener("submit", async (event) => {
        event.preventDefault();
        UIFeedback.clearAllErrors(formMotorista);

        const formData = {
            nome: document.getElementById('nome')?.value.trim() || '',
            sobrenome: document.getElementById('sobrenome')?.value.trim() || '',
            cpf: document.getElementById('cpf')?.value.trim() || '',
            email: document.getElementById('email')?.value.trim() || '',
            telefone: document.getElementById('telefone')?.value.trim() || '',
            cidade: document.getElementById('cidade')?.value.trim() || '',
            senha: document.getElementById('senha')?.value || ''
        };

        const errors = FormValidator.validateRegistration(formData);
        if (errors) {
            FormValidator.showErrors(formMotorista, errors);
            UIFeedback.showWarning("Verifique os erros no formulário.");
            return;
        }

        console.log("Dados validados e prontos para o backend: ", formData);

        const submitButton = formMotorista.querySelector('button[type="submit"]');
        UIFeedback.setLoading(submitButton, true);
        submitButton.setAttribute('data-original-text', 'Cadastrar');

        try {
            const response = await fetch(`${Config.API_BASE_URL}${Config.ENDPOINTS.MOTORISTAS_CADASTRAR}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                UIFeedback.showSuccess(result.message);
                formMotorista.reset();
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                const errorMsg = result.message || 'Falha no cadastro.';
                UIFeedback.showError(errorMsg);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            UIFeedback.showError(Config.ERROR_MESSAGES.NETWORK_ERROR);
        } finally {
            UIFeedback.setLoading(submitButton, false);
        }
    });
}

// ==========================================================
// ROTA: LOGIN COM VALIDAÇÕES
// ==========================================================
const formLogin = document.getElementById("form-login"); 

if (formLogin) {
    formLogin.addEventListener("submit", async (event) => {
        event.preventDefault();
        UIFeedback.clearAllErrors(formLogin);

        const formData = {
            email: document.getElementById('email')?.value.trim() || '',
            senha: document.getElementById('senha')?.value || '',
            perfil: document.getElementById('perfil')?.value || ''
        };

        const errors = FormValidator.validateLogin(formData);
        if (errors) {
            FormValidator.showErrors(formLogin, errors);
            UIFeedback.showWarning("Verifique os campos obrigatórios.");
            return;
        }

        console.log("Dados validados e prontos para o backend: ", formData);

        const submitButton = formLogin.querySelector('button[type="submit"]');
        UIFeedback.setLoading(submitButton, true);
        submitButton.setAttribute('data-original-text', 'Entrar');

        try {
            const response = await fetch(`${Config.API_BASE_URL}${Config.ENDPOINTS.LOGIN}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                UIFeedback.showSuccess(`Bem-vindo(a), ${result.user.nome}!`);
                localStorage.setItem(Config.STORAGE_KEYS.USER_LOGGED_IN, JSON.stringify(result.user));

                const rememberCheckbox = document.getElementById('Check');
                if (rememberCheckbox?.checked) {
                    localStorage.setItem(Config.STORAGE_KEYS.REMEMBER_ME, formData.email);
                }

                setTimeout(() => {
                    window.location.href = 'gps.html';
                }, 1000);
            } else {
                const errorMsg = result.message || 'Falha no login.';
                UIFeedback.showError(errorMsg);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            UIFeedback.showError(Config.ERROR_MESSAGES.NETWORK_ERROR);
        } finally {
            UIFeedback.setLoading(submitButton, false);
        }
    });

    const rememberEmail = localStorage.getItem(Config.STORAGE_KEYS.REMEMBER_ME);
    if (rememberEmail) {
        const emailField = document.getElementById('email');
        const checkField = document.getElementById('Check');
        if (emailField) emailField.value = rememberEmail;
        if (checkField) checkField.checked = true;
    }
}

const formRecuperacao = document.getElementById("form-recuperar");

if (formRecuperacao) {
    formRecuperacao.addEventListener("submit", async (event) => {
        event.preventDefault();
        UIFeedback.clearAllErrors(formRecuperacao);

        const formData = {
            email: document.getElementById('email')?.value.trim() || ''
        };

        const errors = FormValidator.validateRecuperation(formData);
        if (errors) {
            FormValidator.showErrors(formRecuperacao, errors);
            UIFeedback.showWarning("Verifique o e-mail informado.");
            return;
        }

        console.log("Dados validados e prontos para o backend: ", formData);

        const submitButton = formRecuperacao.querySelector('button[type="submit"]');
        UIFeedback.setLoading(submitButton, true);
        submitButton.setAttribute('data-original-text', 'Enviar');

        try {
            const response = await fetch(`${Config.API_BASE_URL}${Config.ENDPOINTS.RECUPERAR_SENHA}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            if (response.ok) {
                UIFeedback.showSuccess(result.message);
                formRecuperacao.reset();
                setTimeout(() => {
                    window.location.href = 'index.html';
                }, 1500);
            } else {
                const errorMsg = result.message || 'Falha ao enviar e-mail.';
                UIFeedback.showError(errorMsg);
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            UIFeedback.showError(Config.ERROR_MESSAGES.NETWORK_ERROR);
        } finally {
            UIFeedback.setLoading(submitButton, false);
        }
    });
}
