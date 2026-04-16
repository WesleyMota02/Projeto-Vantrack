class MensagemChatRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, mensagem):
        query = """
            INSERT INTO mensagens_chat 
            (remetente_id, destinatario_id, texto, lido, criado_em)
            VALUES (%s, %s, %s, FALSE, NOW())
            RETURNING *
        """
        params = (mensagem.remetente_id, mensagem.destinatario_id, mensagem.texto)
        return self.db.execute_query_one(query, params)

    def buscar_por_id(self, mensagem_id):
        query = "SELECT * FROM mensagens_chat WHERE id = %s"
        return self.db.execute_query_one(query, (mensagem_id,))

    def listar_conversa(self, usuario1_id, usuario2_id, limit=50):
        query = """
            SELECT * FROM mensagens_chat 
            WHERE (remetente_id = %s AND destinatario_id = %s) 
               OR (remetente_id = %s AND destinatario_id = %s)
            ORDER BY criado_em DESC
            LIMIT %s
        """
        params = (usuario1_id, usuario2_id, usuario2_id, usuario1_id, limit)
        return self.db.execute_query(query, params, fetch=True)

    def listar_nao_lidas_por_usuario(self, usuario_id, limit=100):
        query = """
            SELECT * FROM mensagens_chat 
            WHERE destinatario_id = %s AND lido = FALSE
            ORDER BY criado_em DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (usuario_id, limit), fetch=True)

    def contar_nao_lidas_por_usuario(self, usuario_id):
        query = "SELECT COUNT(*) as total FROM mensagens_chat WHERE destinatario_id = %s AND lido = FALSE"
        result = self.db.execute_query_one(query, (usuario_id,))
        return result['total'] if result else 0

    def listar_conversas_usuario(self, usuario_id, limit=20):
        query = """
            SELECT DISTINCT 
                CASE 
                    WHEN remetente_id = %s THEN destinatario_id 
                    ELSE remetente_id 
                END as outro_usuario_id,
                MAX(criado_em) as ultima_mensagem
            FROM mensagens_chat 
            WHERE remetente_id = %s OR destinatario_id = %s
            GROUP BY outro_usuario_id
            ORDER BY ultima_mensagem DESC
            LIMIT %s
        """
        return self.db.execute_query(query, (usuario_id, usuario_id, usuario_id, limit), fetch=True)

    def marcar_como_lida(self, mensagem_id):
        query = """
            UPDATE mensagens_chat 
            SET lido = TRUE, lido_em = NOW() 
            WHERE id = %s 
            RETURNING *
        """
        return self.db.execute_query_one(query, (mensagem_id,))

    def marcar_conversa_como_lida(self, usuario_id, outro_usuario_id):
        query = """
            UPDATE mensagens_chat 
            SET lido = TRUE, lido_em = NOW() 
            WHERE destinatario_id = %s AND remetente_id = %s AND lido = FALSE
        """
        self.db.execute_query(query, (usuario_id, outro_usuario_id))

    def deletar(self, mensagem_id):
        query = "DELETE FROM mensagens_chat WHERE id = %s"
        self.db.execute_query(query, (mensagem_id,))

    def listar_por_remetente(self, remetente_id, limit=100):
        query = """
            SELECT * FROM mensagens_chat 
            WHERE remetente_id = %s 
            ORDER BY criado_em DESC 
            LIMIT %s
        """
        return self.db.execute_query(query, (remetente_id, limit), fetch=True)
