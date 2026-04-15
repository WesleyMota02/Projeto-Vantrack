from typing import Optional, List
from domain.inscricao import Inscricao
from infra.inscricao_repository_interface import IInscricaoRepository
from database import Database

class InscricaoRepository(IInscricaoRepository):

    def __init__(self, db: Database):
        self.db = db

    def criar(self, inscricao: Inscricao) -> Inscricao:
        query = """
            INSERT INTO inscricoes (aluno_id, rota_id)
            VALUES (%s, %s)
            RETURNING id, criado_em, atualizado_em
        """
        params = (str(inscricao.aluno_id), str(inscricao.rota_id))
        result = self.db.execute_single(query, params)
        if result:
            inscricao.id = result['id']
            inscricao.criado_em = result['criado_em']
            inscricao.atualizado_em = result['atualizado_em']
        return inscricao

    def obter_por_id(self, inscricao_id: str) -> Optional[Inscricao]:
        query = "SELECT * FROM inscricoes WHERE id = %s"
        result = self.db.execute_single(query, (inscricao_id,))
        return Inscricao.from_dict(result) if result else None

    def obter_por_aluno(self, aluno_id: str) -> List[Inscricao]:
        query = "SELECT * FROM inscricoes WHERE aluno_id = %s AND ativa = true ORDER BY criado_em DESC"
        results = self.db.execute_query(query, (aluno_id,))
        return [Inscricao.from_dict(row) for row in results]

    def obter_por_rota(self, rota_id: str) -> List[Inscricao]:
        query = "SELECT * FROM inscricoes WHERE rota_id = %s AND ativa = true ORDER BY criado_em DESC"
        results = self.db.execute_query(query, (rota_id,))
        return [Inscricao.from_dict(row) for row in results]

    def obter_inscricao(self, aluno_id: str, rota_id: str) -> Optional[Inscricao]:
        query = "SELECT * FROM inscricoes WHERE aluno_id = %s AND rota_id = %s AND ativa = true"
        result = self.db.execute_single(query, (aluno_id, rota_id))
        return Inscricao.from_dict(result) if result else None

    def atualizar(self, inscricao_id: str, dados: dict) -> Optional[Inscricao]:
        campos = []
        valores = []
        for chave, valor in dados.items():
            if chave not in ['id', 'aluno_id', 'rota_id', 'criado_em']:
                campos.append(f"{chave} = %s")
                valores.append(valor)

        if not campos:
            return self.obter_por_id(inscricao_id)

        valores.append(inscricao_id)
        query = f"UPDATE inscricoes SET {', '.join(campos)}, atualizado_em = CURRENT_TIMESTAMP WHERE id = %s RETURNING *"
        result = self.db.execute_single(query, tuple(valores))
        return Inscricao.from_dict(result) if result else None

    def deletar(self, inscricao_id: str) -> bool:
        query = "UPDATE inscricoes SET ativa = false WHERE id = %s"
        rowcount = self.db.execute_update(query, (inscricao_id,))
        return rowcount > 0
