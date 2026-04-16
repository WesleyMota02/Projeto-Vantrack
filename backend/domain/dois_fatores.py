from datetime import datetime, timedelta
from uuid import uuid4
import random
import string

class CodigoVerificacao2FA:
    def __init__(self, id, usuario_id, dispositivo_hash, codigo_2fa, metodo, 
                 telefone_sms=None, email_envio=None, verificado=False, 
                 tentativas_restantes=3, criado_em=None, expira_em=None, verificado_em=None):
        self.id = id
        self.usuario_id = usuario_id
        self.dispositivo_hash = dispositivo_hash
        self.codigo_2fa = codigo_2fa
        self.metodo = metodo  # 'SMS' ou 'EMAIL'
        self.telefone_sms = telefone_sms
        self.email_envio = email_envio
        self.verificado = verificado
        self.tentativas_restantes = tentativas_restantes
        self.criado_em = criado_em or datetime.utcnow()
        self.expira_em = expira_em
        self.verificado_em = verificado_em

    @classmethod
    def criar(cls, usuario_id, dispositivo_hash, metodo, telefone_sms=None, email_envio=None):
        """Factory method para criar novo código 2FA"""
        codigo_2fa = ''.join(random.choices(string.digits, k=6))
        criado_em = datetime.utcnow()
        expira_em = criado_em + timedelta(minutes=5)  # Válido por 5 minutos
        
        return cls(
            id=str(uuid4()),
            usuario_id=usuario_id,
            dispositivo_hash=dispositivo_hash,
            codigo_2fa=codigo_2fa,
            metodo=metodo,
            telefone_sms=telefone_sms,
            email_envio=email_envio,
            verificado=False,
            tentativas_restantes=3,
            criado_em=criado_em,
            expira_em=expira_em,
            verificado_em=None
        )

    def validar_codigo(self, codigo_fornecido):
        """Valida o código fornecido pelo usuário"""
        if self.verificado:
            return False, "Código já foi verificado"
        
        if datetime.utcnow() > self.expira_em:
            return False, "Código expirado"
        
        if self.tentativas_restantes <= 0:
            return False, "Número máximo de tentativas atingido"
        
        self.tentativas_restantes -= 1
        
        if codigo_fornecido != self.codigo_2fa:
            return False, f"Código inválido. Tentativas restantes: {self.tentativas_restantes}"
        
        self.verificado = True
        self.verificado_em = datetime.utcnow()
        return True, "Código verificado com sucesso"

    def to_dict(self):
        """Serializa para dicionário"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'dispositivo_hash': self.dispositivo_hash,
            'metodo': self.metodo,
            'verificado': self.verificado,
            'tentativas_restantes': self.tentativas_restantes,
            'criado_em': self.criado_em.isoformat(),
            'expira_em': self.expira_em.isoformat(),
            'verificado_em': self.verificado_em.isoformat() if self.verificado_em else None
        }
