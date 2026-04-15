from typing import Optional, List
from domain.rota import Rota
from infra.rota_repository_interface import IRotaRepository
from database import Database

class RotaRepository(IRotaRepository):

    def __init__(self, db: Database):
        self.db = db

    def criar(self, rota: Rota) -> Rota:
        query = """
            INSERT INTO rotas (motorista_id, veiculo_id, nome, origem, destino, horario_partida, capacidade_maxima)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, criado_em, atualizado_em
        """
        params = (
            str(rota.motorista_id),
            str(rota.veiculo_id) if rota.veiculo_id else None,
            rota.nome,
            rota.origem,
            rota.destino,
            rota.horario_partida,
            rota.capacidade_maxima
        )
        result = self.db.execute_single(query, params)
        if result:
            rota.id = result['id']
            rota.criado_em = result['criado_em']
            rota.atualizado_em = result['atualizado_em']
        return rota

    def obter_por_id(self, rota_id: str) -> Optional[Rota]:
        query = "SELECT * FROM rotas WHERE id = %s"
        result = self.db.execute_single(query, (rota_id,))
        return Rota.from_dict(result) if result else None

    def obter_por_motorista(self, motorista_id: str) -> List[Rota]:
        query = "SELECT * FROM rotas WHERE motorista_id = %s AND ativa = true ORDER BY horario_partida ASC"
        results = self.db.execute_query(query, (motorista_id,))
        return [Rota.from_dict(row) for row in results]

    def obter_por_veiculo(self, veiculo_id: str) -> List[Rota]:
        query = "SELECT * FROM rotas WHERE veiculo_id = %s AND ativa = true ORDER BY horario_partida ASC"
        results = self.db.execute_query(query, (veiculo_id,))
        return [Rota.from_dict(row) for row in results]

    def listar_ativas(self) -> List[Rota]:
        query = "SELECT * FROM rotas WHERE ativa = true ORDER BY horario_partida ASC"
        results = self.db.execute_query(query)
        return [Rota.from_dict(row) for row in results]

    def atualizar(self, rota_id: str, dados: dict) -> Optional[Rota]:
        campos = []
        valores = []
        for chave, valor in dados.items():
            if chave not in ['id', 'motorista_id', 'criado_em']:
                campos.append(f"{chave} = %s")
                valores.append(valor)

        if not campos:
            return self.obter_por_id(rota_id)

        valores.append(rota_id)
        query = f"UPDATE rotas SET {', '.join(campos)}, atualizado_em = CURRENT_TIMESTAMP WHERE id = %s RETURNING *"
        result = self.db.execute_single(query, tuple(valores))
        return Rota.from_dict(result) if result else None

    def deletar(self, rota_id: str) -> bool:
        query = "UPDATE rotas SET ativa = false WHERE id = %s"
        rowcount = self.db.execute_update(query, (rota_id,))
        return rowcount > 0
