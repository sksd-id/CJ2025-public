
const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const dbPath = path.join(__dirname, '..', 'data.db');
const db = new sqlite3.Database(dbPath);

// Promise wrappers around sqlite3
const run = (sql, params = []) =>
  new Promise((resolve, reject) => {
    db.run(sql, params, function onRun(err) {
      if (err) return reject(err);
      resolve(this);
    });
  });

const get = (sql, params = []) =>
  new Promise((resolve, reject) => {
    db.get(sql, params, (err, row) => {
      if (err) return reject(err);
      resolve(row);
    });
  });

const all = (sql, params = []) =>
  new Promise((resolve, reject) => {
    db.all(sql, params, (err, rows) => {
      if (err) return reject(err);
      resolve(rows);
    });
  });

// Database setup helpers
async function initDb() {
  await run(
    `CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )`
  );

  await run(
    `CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        stored_name TEXT NOT NULL,
        original_name TEXT NOT NULL,
        mime_type TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )`
  );
}

async function ensureAdmin({ email, passwordHash }) {
  const existing = await findUserByEmail(email);
  if (existing) return existing;
  const user = await createUser({ email, passwordHash, role: 'admin' });
  return user;
}

async function createUser({ email, passwordHash, role = 'user' }) {
  const result = await run(
    `INSERT INTO users (email, password, role) VALUES (?, ?, ?)`,
    [email, passwordHash, role]
  );
  return { id: result.lastID, email, role };
}

async function findUserByEmail(email) {
  return get(`SELECT * FROM users WHERE email = ?`, [email]);
}

async function findUserById(id) {
  return get(`SELECT * FROM users WHERE id = ?`, [id]);
}

async function listUsers() {
  return all(
    `SELECT id, email, role, created_at FROM users ORDER BY created_at DESC LIMIT 10`
  );
}

// Upload queries
async function recordUpload({ userId, storedName, originalName, mimeType }) {
  await run(
    `INSERT INTO uploads (user_id, stored_name, original_name, mime_type) VALUES (?, ?, ?, ?)`,
    [userId, storedName, originalName, mimeType]
  );
}

async function listUploads({ userId } = {}) {
  if (userId) {
    return all(
      `SELECT id, stored_name, original_name, mime_type, created_at 
       FROM uploads WHERE user_id = ? ORDER BY created_at DESC`,
      [userId]
    );
  }
  return all(
    `SELECT uploads.id, uploads.stored_name, uploads.original_name, uploads.mime_type, uploads.created_at,
            users.email AS owner_email
     FROM uploads 
     JOIN users ON users.id = uploads.user_id
     ORDER BY uploads.created_at DESC LIMIT 10`
  );
}

async function getExpiredUploads(minutes = 60) {
  const windowExpr = `-${minutes} minutes`;
  return all(
    `SELECT id, stored_name FROM uploads WHERE created_at <= datetime('now', ?)`,
    [windowExpr]
  );
}

async function deleteUploadsByIds(ids = []) {
  if (!ids.length) return 0;
  const placeholders = ids.map(() => '?').join(',');
  const result = await run(`DELETE FROM uploads WHERE id IN (${placeholders})`, ids);
  return result.changes ?? ids.length;
}

async function purgeExpiredUploads(minutes = 60) {
  const expired = await getExpiredUploads(minutes);
  if (!expired.length) return { removed: 0, files: [] };
  await deleteUploadsByIds(expired.map((u) => u.id));
  return { removed: expired.length, files: expired.map((u) => u.stored_name) };
}

const encode = (s) => encodeURIComponent(s);
const decode = (s) => unescape(s);

function sanitize(name) {
  let f = decode(encode(name));
  f = f.replace(/\.\./g, '');
  f = f.replace(/[\\/]/g, '');
  return f;
}

function peelToAllowedExt(name, allowedExts) {
  let cur = name;
  while (true) {
    const dot = cur.lastIndexOf('.');
    if (dot <= 0) return `${cur}.txt`;
    cur = sanitize(cur)
    const ext = cur.slice(dot + 1).toLowerCase();
    if (new RegExp(allowedExts.join('|')).test(ext)) return cur;
    cur = cur.slice(0, dot);
  }
}

module.exports = {
  initDb,
  ensureAdmin,
  createUser,
  findUserByEmail,
  findUserById,
  listUsers,
  recordUpload,
  listUploads,
  purgeExpiredUploads,
  encode,
  decode,
  peelToAllowedExt
};
