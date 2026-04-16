from dataclasses import dataclass
from typing import Optional
from datetime import datetime, date
import uuid


@dataclass
class EnderecoAluno:
    id: str = None
    aluno_id: str = None
    rota_id: str = None
    endereco_coleta: str = None
    endereco_entrega: str = None
    latitude_coleta: Optional[float] = None
    longitude_coleta: Optional[float] = None
    latitude_entrega: Optional[float] = None
    longitude_entrega: Optional[float] = None
    principal: bool = True
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @staticmethod
    def criar(aluno_id: str, rota_id: str, endereco_coleta: str, endereco_entrega: str) -> "EnderecoAluno":
        return EnderecoAluno(
            id=str(uuid.uuid4()),
            aluno_id=aluno_id,
            rota_id=rota_id,
            endereco_coleta=endereco_coleta,
            endereco_entrega=endereco_entrega,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )


@dataclass
class PresencaDiaria:
    id: str = None
    aluno_id: str = None
    rota_id: str = None
    data: date = None
    vai_embarcar: bool = True
    confirmado_em: Optional[datetime] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None

    @staticmethod
    def criar(aluno_id: str, rota_id: str, data: date, vai_embarcar: bool = True) -> "PresencaDiaria":
        return PresencaDiaria(
            id=str(uuid.uuid4()),
            aluno_id=aluno_id,
            rota_id=rota_id,
            data=data,
            vai_embarcar=vai_embarcar,
            confirmado_em=datetime.utcnow() if vai_embarcar is not None else None,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )


@dataclass
class MensagemChat:
    id: str = None
    remetente_id: str = None
    destinatario_id: str = None
    texto: str = None
    lido: bool = False
    lido_em: Optional[datetime] = None
    criado_em: Optional[datetime] = None

    @staticmethod
    def criar(remetente_id: str, destinatario_id: str, texto: str) -> "MensagemChat":
        return MensagemChat(
            id=str(uuid.uuid4()),
            remetente_id=remetente_id,
            destinatario_id=destinatario_id,
            texto=texto,
            lido=False,
            criado_em=datetime.utcnow()
        )

    def marcar_como_lido(self) -> None:
        self.lido = True
        self.lido_em = datetime.utcnow()
