class InscricaoRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, inscricao):
        query = """
            INSERT INTO inscricoes (aluno_id, rota_id, status, criado_em)
            VALUES (%s, %s, %s, NOW())
            RETURNING *
        """
        params = (inscricao.aluno_id, inscricao.rota_id, 'ativa')
        return self.db.execute_query_one(query, params)

    def buscar_por_id(self, inscricao_id):
        query = "SELECT * FROM inscricoes WHERE id = %s"
        return self.db.execute_query_one(query, (inscricao_id,))

    def listar_por_aluno(self, aluno_id):
        query = "SELECT * FROM inscricoes WHERE aluno_id = %s"
        return self.db.execute_query(query, (aluno_id,), fetch=True)

    def listar_por_rota(self, rota_id):
        query = "SELECT * FROM inscricoes WHERE rota_id = %s"
        return self.db.execute_query(query, (rota_id,), fetch=True)

    def contar_por_rota(self, rota_id):
        query = "SELECT COUNT(*) as total FROM inscricoes WHERE rota_id = %s AND status = 'ativa'"
        result = self.db.execute_query_one(query, (rota_id,))
        return result['total'] if result else 0

    def inscricao_existe(self, aluno_id, rota_id):
        query = "SELECT id FROM inscricoes WHERE aluno_id = %s AND rota_id = %s"
        result = self.db.execute_query_one(query, (aluno_id, rota_id))
        return result is not None

    def atualizar_status(self, inscricao_id, novo_status):
        query = "UPDATE inscricoes SET status = %s, atualizado_em = NOW() WHERE id = %s RETURNING *"
        return self.db.execute_query_one(query, (novo_status, inscricao_id))

    def cancelar(self, inscricao_id):
        query = "UPDATE inscricoes SET status = 'cancelada', atualizado_em = NOW() WHERE id = %s RETURNING *"
        return self.db.execute_query_one(query, (inscricao_id,))

    def listar_todas(self):
        query = "SELECT * FROM inscricoes"
        return self.db.execute_query(query, fetch=True)
