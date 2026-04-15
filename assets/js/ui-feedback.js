const UIFeedback = {
  showError: (element, message) => {
    if (!element) return;
    element.classList.add('is-invalid');
    element.setAttribute('aria-invalid', 'true');
    
    let errorDiv = element.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('error-message')) {
      errorDiv = document.createElement('div');
      errorDiv.className = 'error-message';
      element.parentNode.insertBefore(errorDiv, element.nextSibling);
    }
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
  },

  clearError: (element) => {
    if (!element) return;
    element.classList.remove('is-invalid');
    element.setAttribute('aria-invalid', 'false');
    
    const errorDiv = element.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('error-message')) {
      errorDiv.style.display = 'none';
    }
  },

  clearAllErrors: (formElement) => {
    const inputs = formElement.querySelectorAll('input, select, textarea');
    inputs.forEach(input => UIFeedback.clearError(input));
  },

  showSuccess: (message) => {
    const toast = document.createElement('div');
    toast.className = 'toast toast-success';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.textContent = '✅ ' + message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), Config.UI.ANIMATION_DURATION);
    }, Config.UI.TOAST_DURATION);
  },

  showWarning: (message) => {
    const toast = document.createElement('div');
    toast.className = 'toast toast-warning';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    toast.textContent = '⚠️ ' + message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), Config.UI.ANIMATION_DURATION);
    }, Config.UI.TOAST_DURATION);
  },

  showError: (message) => {
    const toast = document.createElement('div');
    toast.className = 'toast toast-error';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.textContent = '❌ ' + message;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), Config.UI.ANIMATION_DURATION);
    }, Config.UI.TOAST_DURATION);
  },

  setLoading: (button, isLoading) => {
    if (isLoading) {
      button.disabled = true;
      button.classList.add('is-loading');
      button.innerHTML = '<span class="spinner"></span> Processando...';
    } else {
      button.disabled = false;
      button.classList.remove('is-loading');
      button.textContent = button.getAttribute('data-original-text') || 'Enviar';
    }
  },

  showPasswordStrength: (password) => {
    const strength = Validators.passwordStrength(password);
    const strengthMap = {
      0: { text: 'Muito Fraca', color: '#d32f2f' },
      1: { text: 'Fraca', color: '#f57c00' },
      2: { text: 'Regular', color: '#fbc02d' },
      3: { text: 'Boa', color: '#7cb342' },
      4: { text: 'Forte', color: '#388e3c' },
      5: { text: 'Muito Forte', color: '#1976d2' },
      6: { text: 'Excelente', color: '#0d47a1' }
    };

    let indicatorDiv = document.getElementById('password-strength');
    if (!indicatorDiv) {
      indicatorDiv = document.createElement('div');
      indicatorDiv.id = 'password-strength';
      indicatorDiv.className = 'password-strength';
      document.getElementById('senha').parentNode.appendChild(indicatorDiv);
    }

    const info = strengthMap[Math.min(strength, 6)];
    indicatorDiv.textContent = 'Força: ' + info.text;
    indicatorDiv.style.color = info.color;
  }
};
