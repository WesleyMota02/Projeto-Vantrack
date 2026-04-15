from abc import ABC, abstractmethod
from typing import Optional, List
from domain.localizacao_gps import LocalizacaoGPS

class ILocalizacaoGPSRepository(ABC):

    @abstractmethod
    def criar(self, localizacao: LocalizacaoGPS) -> LocalizacaoGPS:
        pass

    @abstractmethod
    def obter_por_id(self, localizacao_id: str) -> Optional[LocalizacaoGPS]:
        pass

    @abstractmethod
    def obter_ultima_por_veiculo(self, veiculo_id: str) -> Optional[LocalizacaoGPS]:
        pass

    @abstractmethod
    def obter_historico_veiculo(self, veiculo_id: str, limite: int = 100) -> List[LocalizacaoGPS]:
        pass

    @abstractmethod
    def deletar(self, localizacao_id: str) -> bool:
        pass

    @abstractmethod
    def limpar_historico_veiculo(self, veiculo_id: str, dias: int = 30) -> int:
        pass
