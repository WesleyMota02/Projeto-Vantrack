class LocalizacaoGPSRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, localizacao):
        query = """
            INSERT INTO localizacoes_gps (latitude, longitude, timestamp, veiculo_id)
            VALUES (%s, %s, NOW(), %s)
            RETURNING *
        """
        params = (localizacao.latitude, localizacao.longitude, localizacao.veiculo_id)
        return self.db.execute_query_one(query, params)

    def obter_ultima_localizacao(self, veiculo_id):
        query = """
            SELECT * FROM localizacoes_gps 
            WHERE veiculo_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
        """
        return self.db.execute_query_one(query, (veiculo_id,))

    def obter_historico(self, veiculo_id, limite=100):
        query = """
            SELECT * FROM localizacoes_gps 
            WHERE veiculo_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        return self.db.execute_query(query, (veiculo_id, limite), fetch=True)

    def obter_por_id(self, localizacao_id):
        query = "SELECT * FROM localizacoes_gps WHERE id = %s"
        return self.db.execute_query_one(query, (localizacao_id,))

    def listar_todas(self):
        query = "SELECT * FROM localizacoes_gps ORDER BY timestamp DESC"
        return self.db.execute_query(query, fetch=True)

    def listar_por_veiculo(self, veiculo_id):
        query = "SELECT * FROM localizacoes_gps WHERE veiculo_id = %s ORDER BY timestamp DESC"
        return self.db.execute_query(query, (veiculo_id,), fetch=True)
