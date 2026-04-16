import re
from datetime import datetime

def validar_email(email):
    """Valida formato de email"""
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(padrao, email):
        raise ValueError("Email inválido")
    return True

def validar_cpf(cpf):
    """Valida CPF (formato básico)"""
    cpf_limpo = cpf.replace('.', '').replace('-', '')
    if not re.match(r'^\d{11}$', cpf_limpo):
        raise ValueError("CPF deve conter 11 dígitos")
    return True

def validar_telefone(telefone):
    """Valida número de telefone"""
    telefone_limpo = telefone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    if not re.match(r'^[0-9]{10,11}$', telefone_limpo):
        raise ValueError("Telefone inválido")
    return True

def validar_senha(senha):
    """Valida força da senha"""
    if len(senha) < 8:
        raise ValueError("Senha deve ter no mínimo 8 caracteres")
    if not re.search(r'[A-Z]', senha):
        raise ValueError("Senha deve conter letras maiúsculas")
    if not re.search(r'[a-z]', senha):
        raise ValueError("Senha deve conter letras minúsculas")
    if not re.search(r'[0-9]', senha):
        raise ValueError("Senha deve conter números")
    return True

def validar_nome(nome):
    """Valida nome do usuário"""
    if len(nome) < 3:
        raise ValueError("Nome deve ter no mínimo 3 caracteres")
    if not nome.replace(' ', '').isalpha():
        raise ValueError("Nome deve conter apenas letras")
    return True

def validar_cidade(cidade):
    """Valida nome da cidade"""
    if len(cidade) < 3:
        raise ValueError("Cidade deve ter no mínimo 3 caracteres")
    if not cidade.replace(' ', '').isalpha():
        raise ValueError("Cidade deve conter apenas letras")
    return True

def validar_tipo_perfil(tipo_perfil):
    """Valida tipo de perfil"""
    if tipo_perfil not in ['aluno', 'motorista']:
        raise ValueError("Tipo de perfil inválido")
    return True

def validar_horario(horario):
    """Valida formato de hora HH:MM"""
    try:
        datetime.strptime(horario, '%H:%M')
        return True
    except ValueError:
        raise ValueError("Horário deve estar no formato HH:MM")

def validar_coordenadas(latitude, longitude):
    """Valida coordenadas GPS"""
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude deve estar entre -90 e 90")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude deve estar entre -180 e 180")
    return True
