from abc import ABC, abstractmethod
from typing import Optional, List
from domain.inscricao import Inscricao

class IInscricaoRepository(ABC):

    @abstractmethod
    def criar(self, inscricao: Inscricao) -> Inscricao:
        pass

    @abstractmethod
    def obter_por_id(self, inscricao_id: str) -> Optional[Inscricao]:
        pass

    @abstractmethod
    def obter_por_aluno(self, aluno_id: str) -> List[Inscricao]:
        pass

    @abstractmethod
    def obter_por_rota(self, rota_id: str) -> List[Inscricao]:
        pass

    @abstractmethod
    def obter_inscricao(self, aluno_id: str, rota_id: str) -> Optional[Inscricao]:
        pass

    @abstractmethod
    def atualizar(self, inscricao_id: str, dados: dict) -> Optional[Inscricao]:
        pass

    @abstractmethod
    def deletar(self, inscricao_id: str) -> bool:
        pass
