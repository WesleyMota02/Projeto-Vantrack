from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

@dataclass
class LocalizacaoGPS:
    id: Optional[UUID] = None
    veiculo_id: UUID = None
    latitude: float = 0.0
    longitude: float = 0.0
    timestamp: Optional[datetime] = None
    criado_em: Optional[datetime] = None

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=UUID(dados['id']) if dados.get('id') and isinstance(dados['id'], str) else dados.get('id'),
            veiculo_id=UUID(dados['veiculo_id']) if dados.get('veiculo_id') and isinstance(dados['veiculo_id'], str) else dados.get('veiculo_id'),
            latitude=float(dados.get('latitude', 0.0)),
            longitude=float(dados.get('longitude', 0.0)),
            timestamp=dados.get('timestamp'),
            criado_em=dados.get('criado_em')
        )

    def to_dict(self) -> dict:
        return {
            'id': str(self.id) if self.id else None,
            'veiculo_id': str(self.veiculo_id) if self.veiculo_id else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': str(self.timestamp) if self.timestamp else None,
            'criado_em': str(self.criado_em) if self.criado_em else None
        }
