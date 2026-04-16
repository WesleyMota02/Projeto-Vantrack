class PresencaDiariaRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, presenca):
        query = """
            INSERT INTO presenca_diaria 
            (aluno_id, rota_id, data, vai_embarcar, confirmado_em, criado_em)
            VALUES (%s, %s, %s, %s, NOW(), NOW())
            RETURNING *
        """
        params = (presenca.aluno_id, presenca.rota_id, presenca.data, presenca.vai_embarcar)
        return self.db.execute_query_one(query, params)

    def buscar_por_id(self, presenca_id):
        query = "SELECT * FROM presenca_diaria WHERE id = %s"
        return self.db.execute_query_one(query, (presenca_id,))

    def buscar_por_aluno_e_data(self, aluno_id, data):
        query = "SELECT * FROM presenca_diaria WHERE aluno_id = %s AND data = %s"
        return self.db.execute_query_one(query, (aluno_id, data))

    def buscar_por_aluno_rota_e_data(self, aluno_id, rota_id, data):
        query = "SELECT * FROM presenca_diaria WHERE aluno_id = %s AND rota_id = %s AND data = %s"
        return self.db.execute_query_one(query, (aluno_id, rota_id, data))

    def listar_por_aluno(self, aluno_id, limit=30):
        query = """
            SELECT * FROM presenca_diaria 
            WHERE aluno_id = %s 
            ORDER BY data DESC 
            LIMIT %s
        """
        return self.db.execute_query(query, (aluno_id, limit), fetch=True)

    def listar_por_rota(self, rota_id, data=None):
        if data:
            query = """
                SELECT * FROM presenca_diaria 
                WHERE rota_id = %s AND data = %s 
                ORDER BY criado_em DESC
            """
            return self.db.execute_query(query, (rota_id, data), fetch=True)
        else:
            query = "SELECT * FROM presenca_diaria WHERE rota_id = %s ORDER BY data DESC"
            return self.db.execute_query(query, (rota_id,), fetch=True)

    def listar_confirmados_por_rota_e_data(self, rota_id, data):
        query = """
            SELECT * FROM presenca_diaria 
            WHERE rota_id = %s AND data = %s AND vai_embarcar = TRUE
            ORDER BY criado_em DESC
        """
        return self.db.execute_query(query, (rota_id, data), fetch=True)

    def contar_confirmados_por_rota_e_data(self, rota_id, data):
        query = """
            SELECT COUNT(*) as total FROM presenca_diaria 
            WHERE rota_id = %s AND data = %s AND vai_embarcar = TRUE
        """
        result = self.db.execute_query_one(query, (rota_id, data))
        return result['total'] if result else 0

    def atualizar(self, presenca_id, dados):
        campos = []
        params = []
        for chave, valor in dados.items():
            if valor is not None:
                campos.append(f"{chave} = %s")
                params.append(valor)
        
        if not campos:
            return None
        
        params.append(presenca_id)
        query = f"UPDATE presenca_diaria SET {', '.join(campos)}, atualizado_em = NOW() WHERE id = %s RETURNING *"
        return self.db.execute_query_one(query, params)

    def deletar(self, presenca_id):
        query = "DELETE FROM presenca_diaria WHERE id = %s"
        self.db.execute_query(query, (presenca_id,))
