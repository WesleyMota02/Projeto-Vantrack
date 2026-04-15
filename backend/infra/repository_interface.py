from abc import ABC, abstractmethod
from typing import Optional, List
from domain.usuario import Usuario

class IUsuarioRepository(ABC):

    @abstractmethod
    def criar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def obter_por_id(self, usuario_id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obter_por_email(self, email: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obter_por_cpf(self, cpf: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def listar_por_tipo(self, tipo_perfil: str) -> List[Usuario]:
        pass

    @abstractmethod
    def atualizar(self, usuario_id: str, dados: dict) -> Usuario:
        pass

    @abstractmethod
    def deletar(self, usuario_id: str) -> bool:
        pass
