class UsuarioJaExisteException(Exception):
    def __init__(self, campo: str, valor: str):
        self.campo = campo
        self.valor = valor
        super().__init__(f"Usuário com {campo} '{valor}' já existe")

class UsuarioNaoEncontradoException(Exception):
    def __init__(self, usuario_id: str):
        super().__init__(f"Usuário com ID '{usuario_id}' não encontrado")

class EmailNaoEncontradoException(Exception):
    def __init__(self, email: str):
        super().__init__(f"Usuário com e-mail '{email}' não encontrado")

class SenhaInvalidaException(Exception):
    def __init__(self):
        super().__init__("Senha incorreta")

class DadosInvalidosException(Exception):
    def __init__(self, mensagem: str, detalhes: dict = None):
        self.detalhes = detalhes or {}
        super().__init__(mensagem)

class ErroAutenticacaoException(Exception):
    def __init__(self, mensagem: str = "Falha na autenticação"):
        super().__init__(mensagem)

class ErroGeracaoTokenException(Exception):
    def __init__(self):
        super().__init__("Erro ao gerar token de autenticação")

class ErroConexaoBancoDadosException(Exception):
    def __init__(self):
        super().__init__("Erro ao conectar ao banco de dados")
