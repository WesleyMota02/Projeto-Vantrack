require('dotenv').config();
const express = require('express');
const mysql = require('mysql2/promise');
const cors = require('cors');
// 🚨 MÓDULO DE SEGURANÇA: Importa o bcryptjs para criptografar/comparar senhas
const bcrypt = require('bcryptjs'); 

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_DATABASE,
    connectionLimit: 10
});

// ---------------------------------------------------------------------
// 🚀 ROTAS DE CADASTRO CORRIGIDAS (AGORA USAM HASH)
// ---------------------------------------------------------------------

// ROTA: CADASTRO DE ALUNO 
app.post('/api/alunos/cadastrar', async (req, res) => {
    const { nome, sobrenome, cpf, email, telefone, cidade, senha } = req.body;
    if (!nome || !sobrenome || !cpf || !email || !cidade || !senha) {
        return res.status(400).json({ message: "Dados obrigatórios faltando." });
    }
    try {
        // 🔐 GERA HASH DA SENHA
        const salt = await bcrypt.genSalt(10);
        const senha_hash = await bcrypt.hash(senha, salt);
        
        const sql = `
            INSERT INTO Alunos (nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        `;
        const [result] = await pool.execute(sql, [nome, sobrenome, cpf, email, telefone, cidade, senha_hash]);
        
        return res.status(201).json({ 
            message: "Aluno cadastrado com sucesso!",
            aluno_id: result.insertId
        });

    } catch (error) {
        if (error.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ message: "CPF ou E-mail já cadastrado." });
        }
        console.error("Erro no cadastro de Aluno:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ROTA: CADASTRO DE MOTORISTA
app.post('/api/motoristas/cadastrar', async (req, res) => {
    const { nome, sobrenome, cpf, email, telefone, cidade, senha } = req.body;
    if (!nome || !sobrenome || !cpf || !email || !cidade || !senha) {
        return res.status(400).json({ message: "Dados obrigatórios faltando." });
    }
    try {
        // 🔐 GERA HASH DA SENHA
        const salt = await bcrypt.genSalt(10);
        const senha_hash = await bcrypt.hash(senha, salt);

        const sql = `
            INSERT INTO Motoristas (nome, sobrenome, cpf, email, telefone, cidade, senha_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        `;
        const [result] = await pool.execute(sql, [nome, sobrenome, cpf, email, telefone, cidade, senha_hash]);
        
        return res.status(201).json({ 
            message: "Motorista cadastrado com sucesso!",
            motorista_id: result.insertId
        });

    } catch (error) {
        if (error.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ message: "CPF ou E-mail já cadastrado." });
        }
        console.error("Erro no cadastro de Motorista:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ---------------------------------------------------------------------
// 🔐 ROTA DE LOGIN CORRIGIDA (COMPARA HASH)
// ---------------------------------------------------------------------

app.post('/api/login', async (req, res) => {
    const { email, senha, perfil } = req.body;

    if (!email || !senha || !perfil) {
        return res.status(400).json({ message: "E-mail, senha e perfil são obrigatórios." });
    }
    if (perfil !== 'aluno' && perfil !== 'motorista') {
        return res.status(400).json({ message: "Perfil inválido. Deve ser 'aluno' ou 'motorista'." });
    }

    const tabela = perfil === 'aluno' ? 'Alunos' : 'Motoristas';

    try {
        const sql = `SELECT * FROM ${tabela} WHERE email = ?`;
        const [rows] = await pool.execute(sql, [email]);

        if (rows.length === 0) {
            return res.status(401).json({ message: "Credenciais inválidas." });
        }

        const usuario = rows[0];

        // 🔐 COMPARA HASH
        const senhaCorreta = await bcrypt.compare(senha, usuario.senha_hash);
        
        if (!senhaCorreta) {
            return res.status(401).json({ message: "Credenciais inválidas." });
        }

        const dadosUsuario = { 
            id: usuario.aluno_id || usuario.motorista_id,
            nome: usuario.nome,
            sobrenome: usuario.sobrenome,
            email: usuario.email,
            perfil: perfil
        };

        return res.status(200).json({ 
            message: "Login realizado com sucesso!",
            user: dadosUsuario
        });

    } catch (error) {
        console.error("Erro no processo de Login:", error.message);
        return res.status(500).json({
            message: "Erro interno do servidor ao tentar fazer login."
        });
    }
});

// ---------------------------------------------------------------------
// ⚙️ ROTAS DE GESTÃO E RASTREAMENTO
// ---------------------------------------------------------------------

// ROTA: CADASTRO DE VEÍCULO (VAN)
app.post('/api/veiculos/cadastrar', async (req, res) => {
    const { placa, modelo, capacidade_alunos, motorista_responsavel_id } = req.body;

    if (!placa || !modelo || !capacidade_alunos) {
        return res.status(400).json({ message: "Placa, modelo e capacidade são obrigatórios." });
    }
    
    try {
        let sql;
        let params;
        
        if (motorista_responsavel_id) {
            const [motoristaRows] = await pool.execute('SELECT motorista_id FROM Motoristas WHERE motorista_id = ?', [motorista_responsavel_id]);
            if (motoristaRows.length === 0) {
                return res.status(404).json({ message: "Motorista responsável não encontrado." });
            }
            sql = `INSERT INTO Veiculos (placa, modelo, capacidade_alunos, motorista_responsavel_id) VALUES (?, ?, ?, ?)`;
            params = [placa, modelo, capacidade_alunos, motorista_responsavel_id];
        } else {
            sql = `INSERT INTO Veiculos (placa, modelo, capacidade_alunos) VALUES (?, ?, ?)`;
            params = [placa, modelo, capacidade_alunos];
        }

        const [result] = await pool.execute(sql, params);
        
        return res.status(201).json({ 
            message: "Veículo cadastrado com sucesso!",
            veiculo_id: result.insertId
        });

    } catch (error) {
        if (error.code === 'ER_DUP_ENTRY' && error.sqlMessage.includes('placa')) {
            return res.status(409).json({ message: "Placa já cadastrada." });
        }
        console.error("Erro no cadastro de Veículo:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ROTA: CRIAÇÃO DE ROTA
app.post('/api/rotas/criar', async (req, res) => {
    const { nome_rota, descricao, veiculo_id } = req.body;

    if (!nome_rota || !veiculo_id) {
        return res.status(400).json({ message: "Nome da rota e ID do veículo são obrigatórios." });
    }

    try {
        const [veiculoRows] = await pool.execute('SELECT veiculo_id FROM Veiculos WHERE veiculo_id = ?', [veiculo_id]);
        if (veiculoRows.length === 0) {
            return res.status(404).json({ message: "Veículo não encontrado." });
        }

        const sql = `INSERT INTO Rotas (nome_rota, descricao, veiculo_id) VALUES (?, ?, ?)`;
        const [result] = await pool.execute(sql, [nome_rota, descricao, veiculo_id]);
        
        return res.status(201).json({ 
            message: "Rota criada com sucesso!",
            rota_id: result.insertId
        });

    } catch (error) {
        console.error("Erro na criação de Rota:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ROTA: ASSOCIAR ALUNO À ROTA
app.post('/api/rotas/associar-aluno', async (req, res) => {
    const { aluno_id, rota_id, ponto_embarque } = req.body;

    if (!aluno_id || !rota_id) {
        return res.status(400).json({ message: "ID do aluno e ID da rota são obrigatórios." });
    }

    try {
        const [alunoRows] = await pool.execute('SELECT aluno_id FROM Alunos WHERE aluno_id = ?', [aluno_id]);
        if (alunoRows.length === 0) {
            return res.status(404).json({ message: "Aluno não encontrado." });
        }
        const [rotaRows] = await pool.execute('SELECT rota_id FROM Rotas WHERE rota_id = ?', [rota_id]);
        if (rotaRows.length === 0) {
            return res.status(404).json({ message: "Rota não encontrada." });
        }

        const sql = `
            INSERT INTO Alunos_Rotas (aluno_id, rota_id, ponto_embarque) 
            VALUES (?, ?, ?);
        `;
        const [result] = await pool.execute(sql, [aluno_id, rota_id, ponto_embarque]);
        
        return res.status(201).json({ 
            message: "Aluno associado à rota com sucesso!",
            aluno_rota_id: result.insertId
        });

    } catch (error) {
        if (error.code === 'ER_DUP_ENTRY') {
            return res.status(409).json({ message: "Este aluno já está associado a esta rota." });
        }
        console.error("Erro na associação Aluno-Rota:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ROTA: RASTREAMENTO (GPS)
app.get('/api/rastreamento/:veiculo_id', async (req, res) => {
    const { veiculo_id } = req.params;
    const { limite = 1 } = req.query; 

    try {
        const sql = `
            SELECT 
                latitude, 
                longitude, 
                timestamp_gps 
            FROM Rastreamento_GPS 
            WHERE veiculo_id = ?
            ORDER BY timestamp_gps DESC
            LIMIT ?;
        `;
        const [rows] = await pool.execute(sql, [veiculo_id, parseInt(limite)]);
        
        if (rows.length === 0) {
            return res.status(404).json({ message: "Nenhum dado de rastreamento encontrado para este veículo." });
        }
        
        return res.status(200).json(rows);

    } catch (error) {
        console.error("Erro na obtenção de Rastreamento GPS:", error.message);
        return res.status(500).json({ message: "Erro interno do servidor." });
    }
});

// ROTA: RECUPERAÇÃO DE SENHA
app.post('/api/recuperar-senha', async (req, res) => {
    const { email, perfil } = req.body;
    
    if (!email || !perfil) {
        return res.status(400).json({ message: "E-mail e perfil são obrigatórios." });
    }

    if (perfil !== 'aluno' && perfil !== 'motorista') {
        return res.status(400).json({ message: "Perfil inválido. Deve ser 'aluno' ou 'motorista'." });
    }

    const tabela = perfil === 'aluno' ? 'Alunos' : 'Motoristas';
    
    try {
        const sql = `SELECT * FROM ${tabela} WHERE email = ?`;
        const [rows] = await pool.execute(sql, [email]);
        
        if (rows.length === 0) {
            return res.status(200).json({ message: "Se o e-mail estiver cadastrado, as instruções serão enviadas." });
        }

        const usuario = rows[0];
        const recoveryToken = usuario.aluno_id || usuario.motorista_id; 

        console.log(`[RECOVERY MOCK] Token gerado para ${email} (${perfil}): ${recoveryToken}`);

        return res.status(200).json({ 
            message: "Se o e-mail estiver cadastrado, as instruções foram simuladas (e-mail desativado).",
        });

    } catch (error) {
        console.error("Erro no processo de recuperação de senha:", error.message);
        return res.status(200).json({ message: "Se o e-mail estiver cadastrado, as instruções serão enviadas." });
    }
});

// Rota de teste simples para verificar se o servidor está ativo
app.get('/api/status', (req, res) => {
    res.status(200).json({
        status: "OK",
        message: "Backend Vantrack está ativo e rodando!",
        db_connection: pool.config.database ? "Configurado" : "Não configurado"
    });
});


// INICIO DO SERVIDOR
app.listen(PORT, () => {
    console.log(`🚀 Servidor Node.js rodando em http://localhost:${PORT}`);
});