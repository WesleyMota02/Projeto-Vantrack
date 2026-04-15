from typing import Optional, List
from domain.veiculo import Veiculo
from infra.veiculo_repository_interface import IVeiculoRepository
from database import Database

class VeiculoRepository(IVeiculoRepository):

    def __init__(self, db: Database):
        self.db = db

    def criar(self, veiculo: Veiculo) -> Veiculo:
        query = """
            INSERT INTO veiculos (motorista_id, placa, modelo, ano, capacidade)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, criado_em, atualizado_em
        """
        params = (str(veiculo.motorista_id), veiculo.placa, veiculo.modelo, veiculo.ano, veiculo.capacidade)
        result = self.db.execute_single(query, params)
        if result:
            veiculo.id = result['id']
            veiculo.criado_em = result['criado_em']
            veiculo.atualizado_em = result['atualizado_em']
        return veiculo

    def obter_por_id(self, veiculo_id: str) -> Optional[Veiculo]:
        query = "SELECT * FROM veiculos WHERE id = %s"
        result = self.db.execute_single(query, (veiculo_id,))
        return Veiculo.from_dict(result) if result else None

    def obter_por_motorista(self, motorista_id: str) -> List[Veiculo]:
        query = "SELECT * FROM veiculos WHERE motorista_id = %s AND ativo = true ORDER BY criado_em DESC"
        results = self.db.execute_query(query, (motorista_id,))
        return [Veiculo.from_dict(row) for row in results]

    def obter_por_placa(self, placa: str) -> Optional[Veiculo]:
        query = "SELECT * FROM veiculos WHERE UPPER(placa) = UPPER(%s)"
        result = self.db.execute_single(query, (placa,))
        return Veiculo.from_dict(result) if result else None

    def listar_todos(self) -> List[Veiculo]:
        query = "SELECT * FROM veiculos WHERE ativo = true ORDER BY criado_em DESC"
        results = self.db.execute_query(query)
        return [Veiculo.from_dict(row) for row in results]

    def atualizar(self, veiculo_id: str, dados: dict) -> Optional[Veiculo]:
        campos = []
        valores = []
        for chave, valor in dados.items():
            if chave not in ['id', 'motorista_id', 'criado_em']:
                campos.append(f"{chave} = %s")
                valores.append(valor)

        if not campos:
            return self.obter_por_id(veiculo_id)

        valores.append(veiculo_id)
        query = f"UPDATE veiculos SET {', '.join(campos)}, atualizado_em = CURRENT_TIMESTAMP WHERE id = %s RETURNING *"
        result = self.db.execute_single(query, tuple(valores))
        return Veiculo.from_dict(result) if result else None

    def deletar(self, veiculo_id: str) -> bool:
        query = "UPDATE veiculos SET ativo = false WHERE id = %s"
        rowcount = self.db.execute_update(query, (veiculo_id,))
        return rowcount > 0
