from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Veiculo:
    id: Optional[UUID] = None
    motorista_id: UUID = None
    placa: str = ""
    modelo: str = ""
    ano: int = 2000
    capacidade: int = 50
    ativo: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=UUID(dados['id']) if dados.get('id') and isinstance(dados['id'], str) else dados.get('id'),
            motorista_id=UUID(dados['motorista_id']) if dados.get('motorista_id') and isinstance(dados['motorista_id'], str) else dados.get('motorista_id'),
            placa=dados.get('placa', ''),
            modelo=dados.get('modelo', ''),
            ano=dados.get('ano', 2000),
            capacidade=dados.get('capacidade', 50),
            ativo=dados.get('ativo', True),
            criado_em=dados.get('criado_em'),
            atualizado_em=dados.get('atualizado_em')
        )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id) if self.id else None,
            'motorista_id': str(self.motorista_id) if self.motorista_id else None,
            'placa': self.placa,
            'modelo': self.modelo,
            'ano': self.ano,
            'capacidade': self.capacidade,
            'ativo': self.ativo,
            'criado_em': str(self.criado_em) if self.criado_em else None,
            'atualizado_em': str(self.atualizado_em) if self.atualizado_em else None
        }
