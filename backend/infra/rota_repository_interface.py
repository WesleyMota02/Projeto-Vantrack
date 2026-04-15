from abc import ABC, abstractmethod
from typing import Optional, List
from domain.rota import Rota

class IRotaRepository(ABC):

    @abstractmethod
    def criar(self, rota: Rota) -> Rota:
        pass

    @abstractmethod
    def obter_por_id(self, rota_id: str) -> Optional[Rota]:
        pass

    @abstractmethod
    def obter_por_motorista(self, motorista_id: str) -> List[Rota]:
        pass

    @abstractmethod
    def obter_por_veiculo(self, veiculo_id: str) -> List[Rota]:
        pass

    @abstractmethod
    def listar_ativas(self) -> List[Rota]:
        pass

    @abstractmethod
    def atualizar(self, rota_id: str, dados: dict) -> Optional[Rota]:
        pass

    @abstractmethod
    def deletar(self, rota_id: str) -> bool:
        pass
