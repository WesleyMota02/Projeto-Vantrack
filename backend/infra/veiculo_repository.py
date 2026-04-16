class VeiculoRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, veiculo):
        query = """
            INSERT INTO veiculos (placa, modelo, ano, capacidade, motorista_id, criado_em)
            VALUES (%s, %s, %s, %s, %s, NOW())
            RETURNING *
        """
        params = (veiculo.placa, veiculo.modelo, veiculo.ano, veiculo.capacidade, veiculo.motorista_id)
        return self.db.execute_query_one(query, params)

    def buscar_por_id(self, veiculo_id):
        query = "SELECT * FROM veiculos WHERE id = %s"
        return self.db.execute_query_one(query, (veiculo_id,))

    def buscar_por_placa(self, placa):
        query = "SELECT * FROM veiculos WHERE placa = %s"
        return self.db.execute_query_one(query, (placa,))

    def listar_por_motorista(self, motorista_id):
        query = "SELECT * FROM veiculos WHERE motorista_id = %s"
        return self.db.execute_query(query, (motorista_id,), fetch=True)

    def listar_todos(self):
        query = "SELECT * FROM veiculos"
        return self.db.execute_query(query, fetch=True)

    def atualizar(self, veiculo_id, dados):
        campos = []
        params = []
        for chave, valor in dados.items():
            if valor is not None:
                campos.append(f"{chave} = %s")
                params.append(valor)
        
        if not campos:
            return None
        
        params.append(veiculo_id)
        query = f"UPDATE veiculos SET {', '.join(campos)}, atualizado_em = NOW() WHERE id = %s RETURNING *"
        return self.db.execute_query_one(query, params)

    def deletar(self, veiculo_id):
        query = "DELETE FROM veiculos WHERE id = %s"
        self.db.execute_query(query, (veiculo_id,))

    def placa_existe(self, placa):
        result = self.db.execute_query_one("SELECT id FROM veiculos WHERE placa = %s", (placa,))
        return result is not None
