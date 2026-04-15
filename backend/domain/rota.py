from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class Rota:
    id: Optional[UUID] = None
    motorista_id: UUID = None
    veiculo_id: Optional[UUID] = None
    nome: str = ""
    origem: str = ""
    destino: str = ""
    horario_partida: str = ""
    capacidade_maxima: int = 50
    ativa: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=UUID(dados['id']) if dados.get('id') and isinstance(dados['id'], str) else dados.get('id'),
            motorista_id=UUID(dados['motorista_id']) if dados.get('motorista_id') and isinstance(dados['motorista_id'], str) else dados.get('motorista_id'),
            veiculo_id=UUID(dados['veiculo_id']) if dados.get('veiculo_id') and isinstance(dados['veiculo_id'], str) else dados.get('veiculo_id'),
            nome=dados.get('nome', ''),
            origem=dados.get('origem', ''),
            destino=dados.get('destino', ''),
            horario_partida=dados.get('horario_partida', ''),
            capacidade_maxima=dados.get('capacidade_maxima', 50),
            ativa=dados.get('ativa', True),
            criado_em=dados.get('criado_em'),
            atualizado_em=dados.get('atualizado_em')
        )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id) if self.id else None,
            'motorista_id': str(self.motorista_id) if self.motorista_id else None,
            'veiculo_id': str(self.veiculo_id) if self.veiculo_id else None,
            'nome': self.nome,
            'origem': self.origem,
            'destino': self.destino,
            'horario_partida': self.horario_partida,
            'capacidade_maxima': self.capacidade_maxima,
            'ativa': self.ativa,
            'criado_em': str(self.criado_em) if self.criado_em else None,
            'atualizado_em': str(self.atualizado_em) if self.atualizado_em else None
        }
