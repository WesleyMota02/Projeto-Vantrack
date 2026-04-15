from typing import Optional, List
from domain.usuario import Usuario
from infra.repository_interface import IUsuarioRepository
from database import Database

class UsuarioRepository(IUsuarioRepository):

    def __init__(self, db: Database):
        self.db = db

    def criar(self, usuario: Usuario) -> Usuario:
        query = """
            INSERT INTO usuarios (tipo_perfil, nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id, criado_em, atualizado_em
        """
        params = (
            usuario.tipo_perfil, usuario.nome, usuario.sobrenome,
            usuario.cpf, usuario.email, usuario.telefone, usuario.cidade,
            usuario.senha_hash
        )
        result = self.db.execute_single(query, params)
        if result:
            usuario.id = result['id']
            usuario.criado_em = result['criado_em']
            usuario.atualizado_em = result['atualizado_em']
        return usuario

    def obter_por_id(self, usuario_id: str) -> Optional[Usuario]:
        query = "SELECT * FROM usuarios WHERE id = %s"
        result = self.db.execute_single(query, (usuario_id,))
        return Usuario.from_dict(result) if result else None

    def obter_por_email(self, email: str) -> Optional[Usuario]:
        query = "SELECT * FROM usuarios WHERE email = %s"
        result = self.db.execute_single(query, (email,))
        return Usuario.from_dict(result) if result else None

    def obter_por_cpf(self, cpf: str) -> Optional[Usuario]:
        query = "SELECT * FROM usuarios WHERE cpf = %s"
        result = self.db.execute_single(query, (cpf,))
        return Usuario.from_dict(result) if result else None

    def listar_por_tipo(self, tipo_perfil: str) -> List[Usuario]:
        query = "SELECT * FROM usuarios WHERE tipo_perfil = %s ORDER BY criado_em DESC"
        results = self.db.execute_query(query, (tipo_perfil,))
        return [Usuario.from_dict(row) for row in results]

    def atualizar(self, usuario_id: str, dados: dict) -> Usuario:
        campos = []
        valores = []
        for chave, valor in dados.items():
            if chave not in ['id', 'criado_em']:
                campos.append(f"{chave} = %s")
                valores.append(valor)
        
        if not campos:
            return self.obter_por_id(usuario_id)
        
        valores.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)}, atualizado_em = CURRENT_TIMESTAMP WHERE id = %s RETURNING *"
        result = self.db.execute_single(query, tuple(valores))
        return Usuario.from_dict(result) if result else None

    def deletar(self, usuario_id: str) -> bool:
        query = "DELETE FROM usuarios WHERE id = %s"
        rowcount = self.db.execute_delete(query, (usuario_id,))
        return rowcount > 0
