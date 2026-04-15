const Config = {
  API_BASE_URL: 'http://localhost:3000/api',

  ENDPOINTS: {
    ALUNOS_CADASTRAR: '/alunos/cadastrar',
    MOTORISTAS_CADASTRAR: '/motoristas/cadastrar',
    LOGIN: '/login',
    RECUPERAR_SENHA: '/recuperar-senha',
    VEICULOS_CADASTRAR: '/veiculos/cadastrar'
  },

  VALIDATION_RULES: {
    NAME_MIN: 2,
    NAME_MAX: 100,
    PASSWORD_MIN: 8,
    CPF_LENGTH: 11,
    PHONE_LENGTH: 11,
    EMAIL_MAX: 254,
    CITY_MIN: 2,
    CITY_MAX: 100
  },

  UI: {
    TOAST_DURATION: 5000,
    ANIMATION_DURATION: 300,
    DEBOUNCE_DELAY: 500
  },

  STORAGE_KEYS: {
    USER_LOGGED_IN: 'usuarioLogado',
    REMEMBER_ME: 'lembrarMe',
    SESSION_TOKEN: 'sessionToken'
  },

  ERROR_MESSAGES: {
    NETWORK_ERROR: 'Erro de conexão com o servidor. Verifique sua internet.',
    INVALID_EMAIL: 'E-mail inválido.',
    INVALID_CPF: 'CPF inválido.',
    INVALID_PHONE: 'Telefone inválido. Use formato brasileiro (11 dígitos).',
    WEAK_PASSWORD: 'Senha fraca. Use maiúsculas, minúsculas, números e símbolos.',
    REQUIRED_FIELD: 'Campo obrigatório.',
    PASSWORD_MISMATCH: 'As senhas não coincidem.',
    DUPLICATE_EMAIL: 'E-mail já cadastrado.',
    DUPLICATE_CPF: 'CPF já cadastrado.'
  }
};
