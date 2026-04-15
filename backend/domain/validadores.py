import re
from typing import Optional

class ValidadorUsuario:

    @staticmethod
    def validar_email(email: str) -> bool:
        if not email or len(email) > 254:
            return False
        regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(regex, email) is not None

    @staticmethod
    def validar_cpf(cpf: str) -> bool:
        cleaned = ''.join(filter(str.isdigit, cpf))
        if len(cleaned) != 11:
            return False
        if len(set(cleaned)) == 1:
            return False
        
        def calcula_digito(seq: str) -> int:
            soma = sum(int(d) * (len(seq) + 1 - i) for i, d in enumerate(seq))
            resto = soma % 11
            return 0 if resto < 2 else 11 - resto
        
        if int(cleaned[9]) != calcula_digito(cleaned[:9]):
            return False
        if int(cleaned[10]) != calcula_digito(cleaned[:10]):
            return False
        
        return True

    @staticmethod
    def validar_telefone(telefone: str) -> bool:
        cleaned = ''.join(filter(str.isdigit, telefone))
        return len(cleaned) == 11 and cleaned.startswith('11')

    @staticmethod
    def validar_senha(senha: str) -> bool:
        if len(senha) < 8:
            return False
        if not re.search(r'[A-Z]', senha):
            return False
        if not re.search(r'[a-z]', senha):
            return False
        if not re.search(r'[0-9]', senha):
            return False
        return True

    @staticmethod
    def validar_nome(nome: str, min_len: int = 2, max_len: int = 100) -> bool:
        if not nome or len(nome.strip()) < min_len or len(nome.strip()) > max_len:
            return False
        return re.match(r'^[a-zA-ZáéíóúàâêôãõçÁÉÍÓÚÀÂÊÔÃÕÇ\s]+$', nome.strip()) is not None

    @staticmethod
    def validar_cidade(cidade: str, min_len: int = 2, max_len: int = 100) -> bool:
        if not cidade or len(cidade.strip()) < min_len or len(cidade.strip()) > max_len:
            return False
        return True

    @staticmethod
    def validar_tipo_perfil(tipo_perfil: str) -> bool:
        return tipo_perfil in ['aluno', 'motorista']

class RegistroCadastroRequest:

    def __init__(self, dados: dict):
        self.nome = dados.get('nome', '').strip()
        self.sobrenome = dados.get('sobrenome', '').strip()
        self.cpf = dados.get('cpf', '').strip()
        self.email = dados.get('email', '').strip()
        self.telefone = dados.get('telefone', '').strip()
        self.cidade = dados.get('cidade', '').strip()
        self.senha = dados.get('senha', '')
        self.tipo_perfil = dados.get('tipo_perfil', 'aluno')

    def validar(self) -> tuple[bool, Optional[dict]]:
        erros = {}

        if not ValidadorUsuario.validar_nome(self.nome):
            erros['nome'] = 'Nome inválido (2-100 caracteres, apenas letras)'

        if not ValidadorUsuario.validar_nome(self.sobrenome):
            erros['sobrenome'] = 'Sobrenome inválido (2-100 caracteres, apenas letras)'

        if not ValidadorUsuario.validar_cpf(self.cpf):
            erros['cpf'] = 'CPF inválido'

        if not ValidadorUsuario.validar_email(self.email):
            erros['email'] = 'E-mail inválido'

        if not ValidadorUsuario.validar_telefone(self.telefone):
            erros['telefone'] = 'Telefone inválido (11 dígitos Brasil)'

        if not ValidadorUsuario.validar_cidade(self.cidade):
            erros['cidade'] = 'Cidade inválida (2-100 caracteres)'

        if not ValidadorUsuario.validar_senha(self.senha):
            erros['senha'] = 'Senha fraca (min 8 chars, maiúsculas, minúsculas, números)'

        if not ValidadorUsuario.validar_tipo_perfil(self.tipo_perfil):
            erros['tipo_perfil'] = 'Tipo de perfil inválido'

        return (len(erros) == 0, erros if erros else None)
