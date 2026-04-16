from datetime import datetime
from pydantic import BaseModel, validator

class Inscricao(BaseModel):
    id: int = None
    aluno_id: int
    rota_id: int
    status: str = 'ativa'
    criado_em: datetime = None
    atualizado_em: datetime = None

    @validator('status')
    def validar_status(cls, v):
        if v not in ['ativa', 'cancelada', 'concluida']:
            raise ValueError('Status deve ser: ativa, cancelada ou concluida')
        return v

    class Config:
        from_attributes = True

class InscricaoCreate(BaseModel):
    aluno_id: int
    rota_id: int
