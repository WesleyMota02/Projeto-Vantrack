import pytest
from datetime import datetime
from uuid import uuid4
from domain.usuario import Usuario
from domain.veiculo import Veiculo
from domain.rota import Rota
from domain.inscricao import Inscricao
from domain.localizacao_gps import LocalizacaoGPS

class UsuarioFactory:
    
    @staticmethod
    def criar_aluno(cpf="11144477735", email="aluno@test.com", nome="João Silva"):
        return Usuario(
            id=uuid4(),
            tipo_perfil="aluno",
            nome=nome,
            sobrenome="Silva",
            cpf=cpf,
            email=email,
            telefone="11987654321",
            cidade="São Paulo",
            senha_hash="hashed_password",
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )
    
    @staticmethod
    def criar_motorista(cpf="12345678901", email="motorista@test.com", nome="Maria Santos"):
        return Usuario(
            id=uuid4(),
            tipo_perfil="motorista",
            nome=nome,
            sobrenome="Santos",
            cpf=cpf,
            email=email,
            telefone="11987654322",
            cidade="São Paulo",
            senha_hash="hashed_password",
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )

class VeiculoFactory:
    
    @staticmethod
    def criar_veiculo(motorista_id=None, placa="ABC1234"):
        if motorista_id is None:
            motorista_id = uuid4()
        
        return Veiculo(
            id=uuid4(),
            motorista_id=motorista_id,
            placa=placa,
            modelo="Mercedes Sprinter",
            ano=2022,
            capacidade=50,
            ativo=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )

class RotaFactory:
    
    @staticmethod
    def criar_rota(motorista_id=None, veiculo_id=None):
        if motorista_id is None:
            motorista_id = uuid4()
        
        return Rota(
            id=uuid4(),
            motorista_id=motorista_id,
            veiculo_id=veiculo_id,
            nome="Rota Centro-Norte",
            origem="Escola Centro",
            destino="Bairro Norte",
            horario_partida="07:30",
            capacidade_maxima=50,
            ativa=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )

class InscricaoFactory:
    
    @staticmethod
    def criar_inscricao(aluno_id=None, rota_id=None):
        if aluno_id is None:
            aluno_id = uuid4()
        if rota_id is None:
            rota_id = uuid4()
        
        return Inscricao(
            id=uuid4(),
            aluno_id=aluno_id,
            rota_id=rota_id,
            ativa=True,
            criado_em=datetime.utcnow(),
            atualizado_em=datetime.utcnow()
        )

class LocalizacaoGPSFactory:
    
    @staticmethod
    def criar_localizacao(veiculo_id=None, latitude=-23.5505, longitude=-46.6333):
        if veiculo_id is None:
            veiculo_id = uuid4()
        
        return LocalizacaoGPS(
            id=uuid4(),
            veiculo_id=veiculo_id,
            latitude=latitude,
            longitude=longitude,
            timestamp=datetime.utcnow(),
            criado_em=datetime.utcnow()
        )
