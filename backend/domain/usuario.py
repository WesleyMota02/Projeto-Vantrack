from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from datetime import datetime

@dataclass
class Usuario:
    id: Optional[UUID] = None
    tipo_perfil: str = None
    nome: str = None
    sobrenome: str = None
    cpf: str = None
    email: str = None
    telefone: str = None
    cidade: str = None
    senha_hash: Optional[str] = None
    ativo: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            tipo_perfil=data.get('tipo_perfil'),
            nome=data.get('nome'),
            sobrenome=data.get('sobrenome'),
            cpf=data.get('cpf'),
            email=data.get('email'),
            telefone=data.get('telefone'),
            cidade=data.get('cidade'),
            senha_hash=data.get('senha_hash'),
            ativo=data.get('ativo', True),
            criado_em=data.get('criado_em'),
            atualizado_em=data.get('atualizado_em')
        )

    def to_dict(self, include_senha_hash=False):
        data = {
            'id': str(self.id) if self.id else None,
            'tipo_perfil': self.tipo_perfil,
            'nome': self.nome,
            'sobrenome': self.sobrenome,
            'cpf': self.cpf,
            'email': self.email,
            'telefone': self.telefone,
            'cidade': self.cidade,
            'ativo': self.ativo,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'atualizado_em': self.atualizado_em.isoformat() if self.atualizado_em else None
        }
        if include_senha_hash:
            data['senha_hash'] = self.senha_hash
        return data
