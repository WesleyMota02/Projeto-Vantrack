from typing import Optional, List
from domain.localizacao_gps import LocalizacaoGPS
from infra.localizacao_gps_repository_interface import ILocalizacaoGPSRepository
from database import Database
from datetime import datetime, timedelta

class LocalizacaoGPSRepository(ILocalizacaoGPSRepository):

    def __init__(self, db: Database):
        self.db = db

    def criar(self, localizacao: LocalizacaoGPS) -> LocalizacaoGPS:
        query = """
            INSERT INTO localizacoes_gps (veiculo_id, latitude, longitude, timestamp)
            VALUES (%s, %s, %s, %s)
            RETURNING id, criado_em
        """
        params = (
            str(localizacao.veiculo_id),
            localizacao.latitude,
            localizacao.longitude,
            localizacao.timestamp or datetime.utcnow()
        )
        result = self.db.execute_single(query, params)
        if result:
            localizacao.id = result['id']
            localizacao.criado_em = result['criado_em']
        return localizacao

    def obter_por_id(self, localizacao_id: str) -> Optional[LocalizacaoGPS]:
        query = "SELECT * FROM localizacoes_gps WHERE id = %s"
        result = self.db.execute_single(query, (localizacao_id,))
        return LocalizacaoGPS.from_dict(result) if result else None

    def obter_ultima_por_veiculo(self, veiculo_id: str) -> Optional[LocalizacaoGPS]:
        query = """
            SELECT * FROM localizacoes_gps 
            WHERE veiculo_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 1
        """
        result = self.db.execute_single(query, (veiculo_id,))
        return LocalizacaoGPS.from_dict(result) if result else None

    def obter_historico_veiculo(self, veiculo_id: str, limite: int = 100) -> List[LocalizacaoGPS]:
        query = """
            SELECT * FROM localizacoes_gps 
            WHERE veiculo_id = %s 
            ORDER BY timestamp DESC 
            LIMIT %s
        """
        results = self.db.execute_query(query, (veiculo_id, limite))
        return [LocalizacaoGPS.from_dict(row) for row in results]

    def deletar(self, localizacao_id: str) -> bool:
        query = "DELETE FROM localizacoes_gps WHERE id = %s"
        rowcount = self.db.execute_delete(query, (localizacao_id,))
        return rowcount > 0

    def limpar_historico_veiculo(self, veiculo_id: str, dias: int = 30) -> int:
        data_limite = datetime.utcnow() - timedelta(days=dias)
        query = """
            DELETE FROM localizacoes_gps 
            WHERE veiculo_id = %s AND timestamp < %s
        """
        rowcount = self.db.execute_delete(query, (veiculo_id, data_limite))
        return rowcount
