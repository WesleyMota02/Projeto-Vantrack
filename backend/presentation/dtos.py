from dataclasses import dataclass
from typing import Optional
from domain.usuario import Usuario

@dataclass
class CadastroDTO:
    nome: str
    sobrenome: str
    cpf: str
    email: str
    telefone: str
    cidade: str
    senha: str
    tipo_perfil: str

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            nome=dados.get('nome', '').strip(),
            sobrenome=dados.get('sobrenome', '').strip(),
            cpf=dados.get('cpf', '').strip(),
            email=dados.get('email', '').strip(),
            telefone=dados.get('telefone', '').strip(),
            cidade=dados.get('cidade', '').strip(),
            senha=dados.get('senha', ''),
            tipo_perfil=dados.get('tipo_perfil', 'aluno')
        )

@dataclass
class LoginDTO:
    email: str
    senha: str
    perfil: str

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            email=dados.get('email', '').strip(),
            senha=dados.get('senha', ''),
            perfil=dados.get('perfil', 'aluno')
        )

@dataclass
class UsuarioResponseDTO:
    id: str
    tipo_perfil: str
    nome: str
    sobrenome: str
    cpf: str
    email: str
    telefone: str
    cidade: str
    ativo: bool
    criado_em: str
    atualizado_em: str

    @classmethod
    def from_usuario(cls, usuario: Usuario):
        return cls(
            id=str(usuario.id) if usuario.id else None,
            tipo_perfil=usuario.tipo_perfil,
            nome=usuario.nome,
            sobrenome=usuario.sobrenome,
            cpf=usuario.cpf,
            email=usuario.email,
            telefone=usuario.telefone,
            cidade=usuario.cidade,
            ativo=usuario.ativo,
            criado_em=str(usuario.criado_em),
            atualizado_em=str(usuario.atualizado_em)
        )

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'tipo_perfil': self.tipo_perfil,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'cidade': self.cidade,
            'ativo': self.ativo,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }

@dataclass
class LoginResponseDTO:
    usuario: UsuarioResponseDTO
    token: str
    tipo_token: str = 'Bearer'

    def to_dict(self) -> dict:
        return {
            'usuario': self.usuario.to_dict(),
            'token': self.token,
            'tipo_token': self.tipo_token
        }
