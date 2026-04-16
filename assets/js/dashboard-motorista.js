let usuarioAtual = {
  id: null,
  tipo_perfil: null,
  nome: null,
  email: null
};

const menuItems = document.querySelectorAll('.menu-item');
const sections = document.querySelectorAll('.dashboard-section');
const logoutBtn = document.getElementById('logout-btn');

function carregarDadosUsuario() {
  const token = localStorage.getItem('auth_token');
  if (!token) {
    window.location.href = '/index.html';
    return;
  }

  const usuarioJSON = localStorage.getItem('usuario_dados');
  if (usuarioJSON) {
    usuarioAtual = JSON.parse(usuarioJSON);
    document.getElementById('motorista-nome').textContent = usuarioAtual.nome;
    document.getElementById('profile-name').textContent = usuarioAtual.nome;
  }
}

function trocarSecao(nomeSecao) {
  sections.forEach(section => section.classList.remove('active'));
  menuItems.forEach(item => item.classList.remove('active'));

  const secao = document.getElementById(nomeSecao + '-section');
  if (secao) {
    secao.classList.add('active');
  }

  const menu = document.querySelector(`[data-menu="${nomeSecao}"]`);
  if (menu) {
    menu.classList.add('active');
  }

  const titles = {
    'inicio': 'Início',
    'alunos': 'Lista de Alunos',
    'rotas': 'Minhas Rotas',
    'chat': 'Chat'
  };

  document.getElementById('page-title').textContent = titles[nomeSecao] || nomeSecao;
}

menuItems.forEach(item => {
  item.addEventListener('click', (e) => {
    e.preventDefault();
    const nomeSecao = item.getAttribute('data-menu');
    trocarSecao(nomeSecao);
  });
});

logoutBtn.addEventListener('click', () => {
  localStorage.removeItem('auth_token');
  localStorage.removeItem('usuario_dados');
  window.location.href = '/index.html';
});

document.addEventListener('DOMContentLoaded', () => {
  carregarDadosUsuario();
  trocarSecao('inicio');
});
