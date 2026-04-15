from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Inscricao:
    id: Optional[UUID] = None
    aluno_id: UUID = None
    rota_id: UUID = None
    data_inscricao: Optional[datetime] = None
    ativa: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=UUID(dados['id']) if dados.get('id') and isinstance(dados['id'], str) else dados.get('id'),
            aluno_id=UUID(dados['aluno_id']) if dados.get('aluno_id') and isinstance(dados['aluno_id'], str) else dados.get('aluno_id'),
            rota_id=UUID(dados['rota_id']) if dados.get('rota_id') and isinstance(dados['rota_id'], str) else dados.get('rota_id'),
            data_inscricao=dados.get('data_inscricao'),
            ativa=dados.get('ativa', True),
            criado_em=dados.get('criado_em'),
            atualizado_em=dados.get('atualizado_em')
        )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id) if self.id else None,
            'aluno_id': str(self.aluno_id) if self.aluno_id else None,
            'rota_id': str(self.rota_id) if self.rota_id else None,
            'data_inscricao': str(self.data_inscricao) if self.data_inscricao else None,
            'ativa': self.ativa,
            'criado_em': str(self.criado_em) if self.criado_em else None,
            'atualizado_em': str(self.atualizado_em) if self.atualizado_em else None
        }
