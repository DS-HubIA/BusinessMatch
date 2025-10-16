import express from "express";
import cors from "cors";
import pkg from "pg";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";

const { Pool } = pkg;
const app = express();
app.use(express.json());
app.use(cors());

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

app.get("/healthz", (req, res) => res.json({ ok: true, ts: new Date().toISOString() }));

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

app.get("/", (req, res) => res.send("MVP rodando ✅"));

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on ${port}`));
