from domain.dois_fatores import CodigoVerificacao2FA
from datetime import datetime
from uuid import uuid4

class Dois_FatoresRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, usuario_id, dispositivo_hash, metodo, telefone_sms=None, email_envio=None):
        """Cria novo código de verificação 2FA"""
        codigo = CodigoVerificacao2FA.criar(
            usuario_id=usuario_id,
            dispositivo_hash=dispositivo_hash,
            metodo=metodo,
            telefone_sms=telefone_sms,
            email_envio=email_envio
        )

        query = """
            INSERT INTO dois_fatores 
            (id, usuario_id, dispositivo_hash, codigo_2fa, metodo, telefone_sms, email_envio, 
             verificado, tentativas_restantes, criado_em, expira_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        self.db.execute_query(
            query,
            (codigo.id, usuario_id, dispositivo_hash, codigo.codigo_2fa, metodo,
             telefone_sms, email_envio, False, 3, codigo.criado_em, codigo.expira_em)
        )

        return codigo

    def buscar_por_id(self, dois_fatores_id):
        """Busca código 2FA por ID"""
        query = "SELECT * FROM dois_fatores WHERE id = %s"
        resultado = self.db.execute_query_one(query, (dois_fatores_id,))
        
        if not resultado:
            return None
        
        return self._mapear_para_modelo(resultado)

    def buscar_ativo_por_usuario_e_dispositivo(self, usuario_id, dispositivo_hash):
        """Busca código 2FA ativo (não expirado, não verificado) para usuário e dispositivo"""
        query = """
            SELECT * FROM dois_fatores 
            WHERE usuario_id = %s 
            AND dispositivo_hash = %s 
            AND verificado = FALSE
            AND expira_em > NOW()
            ORDER BY criado_em DESC
            LIMIT 1
        """
        
        resultado = self.db.execute_query_one(
            query,
            (usuario_id, dispositivo_hash)
        )
        
        if not resultado:
            return None
        
        return self._mapear_para_modelo(resultado)

    def atualizar_verificacao(self, dois_fatores_id, verificado, tentativas_restantes):
        """Atualiza status de verificação e tentativas restantes"""
        query = """
            UPDATE dois_fatores 
            SET verificado = %s, 
                tentativas_restantes = %s,
                verificado_em = CASE WHEN %s THEN NOW() ELSE verificado_em END
            WHERE id = %s
        """
        
        self.db.execute_query(
            query,
            (verificado, tentativas_restantes, verificado, dois_fatores_id)
        )
        
        # Buscar o registro atualizado
        resultado = self.db.execute_query_one(
            "SELECT * FROM dois_fatores WHERE id = %s",
            (dois_fatores_id,)
        )
        return self._mapear_para_modelo(resultado)

    def limpar_expirados(self, usuario_id):
        """Remove códigos expirados do usuário"""
        query = """
            DELETE FROM dois_fatores 
            WHERE usuario_id = %s 
            AND expira_em <= NOW()
        """
        
        self.db.execute_query(query, (usuario_id,))

    def deletar(self, dois_fatores_id):
        """Deleta código 2FA"""
        query = "DELETE FROM dois_fatores WHERE id = %s"
        self.db.execute_query(query, (dois_fatores_id,))

    def _mapear_para_modelo(self, row):
        """Converte resultado do banco em modelo CodigoVerificacao2FA"""
        return CodigoVerificacao2FA(
            id=row['id'],
            usuario_id=row['usuario_id'],
            dispositivo_hash=row['dispositivo_hash'],
            codigo_2fa=row['codigo_2fa'],
            metodo=row['metodo'],
            telefone_sms=row['telefone_sms'],
            email_envio=row['email_envio'],
            verificado=row['verificado'],
            tentativas_restantes=row['tentativas_restantes'],
            criado_em=row['criado_em'],
            expira_em=row['expira_em'],
            verificado_em=row['verificado_em']
        )
