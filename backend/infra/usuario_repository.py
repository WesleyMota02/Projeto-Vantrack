class UsuarioRepository:
    def __init__(self, db):
        self.db = db

    def criar(self, usuario):
        from uuid import uuid4
        usuario_id = str(uuid4())
        
        query = """
            INSERT INTO usuarios (id, email, cpf, nome, telefone, cidade, tipo_perfil, senha_hash, ativo, criado_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        params = (usuario_id, usuario.email, usuario.cpf, usuario.nome, usuario.telefone, 
                  usuario.cidade, usuario.tipo_perfil, usuario.senha_hash, True)
        
        try:
            self.db.execute_query(query, params)
        except Exception as e:
            print(f"Erro ao inserir usuário: {e}")
            raise
        
        # Buscar o usuário criado
        usuario_criado = self.buscar_por_id(usuario_id)
        
        if usuario_criado is None:
            raise Exception(f"Falha ao criar usuário. ID: {usuario_id}")
            
        return usuario_criado

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
        query = f"UPDATE usuarios SET {', '.join(campos)}, atualizado_em = NOW() WHERE id = %s AND ativo = TRUE"
        self.db.execute_query(query, params)
        
        # Buscar o usuário atualizado
        usuario_atualizado = self.buscar_por_id(usuario_id)
        return usuario_atualizado

    def soft_delete(self, usuario_id):
        query = "UPDATE usuarios SET ativo = FALSE, atualizado_em = NOW() WHERE id = %s"
        self.db.execute_query(query, (usuario_id,))

    def email_existe(self, email):
        result = self.db.execute_query_one("SELECT id FROM usuarios WHERE email = %s", (email,))
        return result is not None

    def cpf_existe(self, cpf):
        result = self.db.execute_query_one("SELECT id FROM usuarios WHERE cpf = %s", (cpf,))
        return result is not None
