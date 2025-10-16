import express from "express";
import cors from "cors";
import pkg from "pg";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const { Pool } = pkg;
const app = express();
app.use(express.json());
app.use(cors());

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 1) servir estáticos de /public
app.use(express.static(join(__dirname, "public")));

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

// healthcheck
app.get("/healthz", (_req, res) => res.json({ ok: true, ts: new Date().toISOString() }));

// AUTH
app.post("/api/auth/register", async (req, res) => {
  try {
    const { name, email, password } = req.body;
    if (!name || !email || !password) return res.status(400).json({ error: "dados obrigatórios" });
    const hash = await bcrypt.hash(password, 10);
    const result = await pool.query(
      "INSERT INTO users (name,email,password_hash) VALUES ($1,$2,$3) RETURNING id,name,email",
      [name, email, hash]
    );
    const token = jwt.sign({ id: result.rows[0].id, email }, process.env.JWT_SECRET || "secret", { expiresIn: "7d" });
    res.json({ user: result.rows[0], token });
  } catch (e) {
    if (String(e).includes("unique")) return res.status(409).json({ error: "email já cadastrado" });
    res.status(500).json({ error: e.message });
  }
});

app.post("/api/auth/login", async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ error: "dados obrigatórios" });
    const { rows } = await pool.query("SELECT * FROM users WHERE email=$1", [email]);
    if (!rows.length) return res.status(401).json({ error: "Usuário não encontrado" });
    const ok = await bcrypt.compare(password, rows[0].password_hash);
    if (!ok) return res.status(401).json({ error: "Senha incorreta" });
    const token = jwt.sign({ id: rows[0].id, email }, process.env.JWT_SECRET || "secret", { expiresIn: "7d" });
    res.json({ token });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// OPORTUNIDADES
app.get("/api/opportunities", async (req, res) => {
  try {
    const { type, category } = req.query;
    let sql = "SELECT * FROM businesses WHERE 1=1";
    const params = [];
    if (type) { sql += " AND type=$1"; params.push(type); }
    if (category) { sql += params.length ? " AND category=$2" : " AND category=$1"; params.push(category); }
    const { rows } = await pool.query(sql, params);
    res.json(rows);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

app.post("/api/opportunities", async (req, res) => {
  try {
    const auth = req.headers.authorization;
    if (!auth) return res.status(401).json({ error: "sem token" });
    const token = auth.split(" ")[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET || "secret");

    const { type, category, title, description, image_url, tags, location } = req.body;
    const result = await pool.query(
      `INSERT INTO businesses (user_id,type,category,title,description,image_url,tags,location)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *`,
      [decoded.id, type, category, title, description, image_url || null, tags || null, location || null]
    );
    res.json(result.rows[0]);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// 2) rota raiz envia o seu index.html
app.get("/", (_req, res) => {
  res.sendFile(join(__dirname, "public", "index.html"));
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on ${port}`));
