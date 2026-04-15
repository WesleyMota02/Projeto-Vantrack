from abc import ABC, abstractmethod
from typing import Optional, List
from domain.veiculo import Veiculo

class IVeiculoRepository(ABC):

    @abstractmethod
    def criar(self, veiculo: Veiculo) -> Veiculo:
        pass

    @abstractmethod
    def obter_por_id(self, veiculo_id: str) -> Optional[Veiculo]:
        pass

    @abstractmethod
    def obter_por_motorista(self, motorista_id: str) -> List[Veiculo]:
        pass

    @abstractmethod
    def obter_por_placa(self, placa: str) -> Optional[Veiculo]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Veiculo]:
        pass

    @abstractmethod
    def atualizar(self, veiculo_id: str, dados: dict) -> Optional[Veiculo]:
        pass

    @abstractmethod
    def deletar(self, veiculo_id: str) -> bool:
        pass
