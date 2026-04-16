class UsuarioRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, usuario):
        query = """
            INSERT INTO usuarios (email, cpf, nome, telefone, cidade, tipo_perfil, senha_hash, ativo, criado_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
            RETURNING id, email, cpf, nome, telefone, cidade, tipo_perfil, ativo, criado_em, atualizado_em
        """
        params = (usuario.email, usuario.cpf, usuario.nome, usuario.telefone, 
                  usuario.cidade, usuario.tipo_perfil, usuario.senha_hash, True)
        return self.db.execute_query_one(query, params)

    def buscar_por_id(self, usuario_id):
        query = "SELECT * FROM usuarios WHERE id = %s AND ativo = TRUE"
        return self.db.execute_query_one(query, (usuario_id,))

    def buscar_por_email(self, email):
        query = "SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE"
        return self.db.execute_query_one(query, (email,))

    def buscar_por_cpf(self, cpf):
        query = "SELECT * FROM usuarios WHERE cpf = %s AND ativo = TRUE"
        return self.db.execute_query_one(query, (cpf,))

    def listar_por_tipo(self, tipo_perfil):
        query = "SELECT * FROM usuarios WHERE tipo_perfil = %s AND ativo = TRUE"
        return self.db.execute_query(query, (tipo_perfil,), fetch=True)

    def listar_todos(self):
        query = "SELECT * FROM usuarios WHERE ativo = TRUE"
        return self.db.execute_query(query, fetch=True)

    def atualizar(self, usuario_id, dados):
        campos = []
        params = []
        for chave, valor in dados.items():
            if valor is not None:
                campos.append(f"{chave} = %s")
                params.append(valor)
        
        if not campos:
            return None
        
        params.append(usuario_id)
        query = f"UPDATE usuarios SET {', '.join(campos)}, atualizado_em = NOW() WHERE id = %s AND ativo = TRUE RETURNING *"
        return self.db.execute_query_one(query, params)

    def soft_delete(self, usuario_id):
        query = "UPDATE usuarios SET ativo = FALSE, atualizado_em = NOW() WHERE id = %s"
        self.db.execute_query(query, (usuario_id,))

    def email_existe(self, email):
        result = self.db.execute_query_one("SELECT id FROM usuarios WHERE email = %s", (email,))
        return result is not None

    def cpf_existe(self, cpf):
        result = self.db.execute_query_one("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
        return result is not None
