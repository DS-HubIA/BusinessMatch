import express from "express";
import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import pkg from "pg";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const { Pool } = pkg;

const app = express();

// ----- Segurança base
app.disable("x-powered-by");
app.set("trust proxy", 1); // Render/Cloudflare

app.use(helmet({
  crossOriginResourcePolicy: { policy: "cross-origin" },
  contentSecurityPolicy: false, // (pode ligar depois e whitelistar seus domínios/recursos)
  referrerPolicy: { policy: "no-referrer" }
}));
app.use(helmet.hsts({ maxAge: 15552000 })); // 180 dias

// JSON com limite (evita payloads grandes)
app.use(express.json({ limit: "200kb" }));

// CORS restrito (ajuste a lista conforme necessário)
const ALLOWED = [
  "https://businessmatch-v2.onrender.com",
  "http://localhost:3000",
  "http://localhost:5173"
];
app.use(cors({
  origin: (origin, cb) => {
    if (!origin || ALLOWED.includes(origin)) return cb(null, true);
    return cb(new Error("Not allowed by CORS"));
  }
}));

// Rate limit (geral + login)
const apiLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 1000, standardHeaders: true, legacyHeaders: false });
const authLimiter = rateLimit({ windowMs: 10 * 60 * 1000, max: 30, standardHeaders: true, legacyHeaders: false }); // freia brute-force

app.use("/api/", apiLimiter);
app.use("/api/auth/", authLimiter);

// ----- Static /public
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
app.use(express.static(join(__dirname, "public")));

// ----- DB
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

const onlyDigits = s => (s || "").replace(/\D+/g, "");

// ----- Health
app.get("/healthz", (_req, res) => res.json({ ok: true, ts: new Date().toISOString() }));

// ----- AUTH
app.post("/api/auth/register", async (req, res) => {
  try {
    let { name, email, password, phone, company, cnpj } = req.body || {};
    if (!name || !email || !password || !phone || !cnpj) return res.status(400).json({ error: "Campos obrigatórios: nome, email, senha, celular, CNPJ" });
    if (!email.includes("@")) return res.status(400).json({ error: "email inválido" });
    if (String(password).length < 6) return res.status(400).json({ error: "senha muito curta (mín. 6)" });

    const phoneDigits = onlyDigits(phone);
    if (phoneDigits.length < 10 || phoneDigits.length > 11) return res.status(400).json({ error: "celular inválido" });

    const cnpjDigits = onlyDigits(cnpj);
    if (cnpjDigits.length !== 14) return res.status(400).json({ error: "CNPJ inválido" });

    const hash = await bcrypt.hash(password, 12); // custo um pouco maior
    const result = await pool.query(
      `INSERT INTO users (name,email,phone,company,password_hash,cnpj)
       VALUES ($1,$2,$3,$4,$5,$6)
       RETURNING id,name,email,phone,company,cnpj`,
      [name, email, phoneDigits, company || null, hash, cnpjDigits]
    );

    const token = jwt.sign({ id: result.rows[0].id, email }, process.env.JWT_SECRET || "secret", { expiresIn: "7d" });
    res.json({ user: result.rows[0], token });
  } catch (e) {
    if (String(e).includes("unique")) return res.status(409).json({ error: "email já cadastrado" });
    res.status(500).json({ error: "erro interno" });
  }
});

app.post("/api/auth/login", async (req, res) => {
  try {
    const { email, password } = req.body || {};
    if (!email || !password) return res.status(400).json({ error: "dados obrigatórios" });
    const { rows } = await pool.query("SELECT id, email, password_hash FROM users WHERE email=$1", [email]);
    if (!rows.length) return res.status(401).json({ error: "credenciais inválidas" });
    const ok = await bcrypt.compare(password, rows[0].password_hash);
    if (!ok) return res.status(401).json({ error: "credenciais inválidas" });
    const token = jwt.sign({ id: rows[0].id, email: rows[0].email }, process.env.JWT_SECRET || "secret", { expiresIn: "7d" });
    res.json({ token });
  } catch {
    res.status(500).json({ error: "erro interno" });
  }
});

// ----- OPORTUNIDADES
app.get("/api/opportunities", async (req, res) => {
  try {
    const { type, category } = req.query;
    let sql = "SELECT * FROM businesses WHERE 1=1";
    const params = [];
    if (type) { params.push(type); sql += ` AND type=$${params.length}`; }
    if (category) { params.push(category); sql += ` AND category=$${params.length}`; }
    const { rows } = await pool.query(sql, params);
    res.json(rows);
  } catch {
    res.status(500).json({ error: "erro interno" });
  }
});

app.post("/api/opportunities", async (req, res) => {
  try {
    const auth = req.headers.authorization || "";
    const token = auth.split(" ")[1];
    if (!token) return res.status(401).json({ error: "sem token" });
    const decoded = jwt.verify(token, process.env.JWT_SECRET || "secret");

    const { type, category, title, description, image_url, tags, location } = req.body || {};
    if (!type || !category || !title || !description) return res.status(400).json({ error: "dados obrigatórios" });

    const result = await pool.query(
      `INSERT INTO businesses (user_id,type,category,title,description,image_url,tags,location)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING *`,
      [decoded.id, type, category, title, description, image_url || null, Array.isArray(tags)?tags:null, location || null]
    );
    res.json(result.rows[0]);
  } catch {
    res.status(500).json({ error: "erro interno" });
  }
});

// ----- Front
app.get("/", (_req, res) => {
  res.sendFile(join(__dirname, "public", "index.html"));
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server running on ${port}`));
