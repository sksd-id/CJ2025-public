const { createUser, findUserByEmail } = require('../utils');
const { hashPassword, verifyPassword } = require('../services/auth');
const { onlyStrings } = require('../services/validators');

const normalizeEmail = (email = '') => email.trim().toLowerCase();

async function showRegister(req, res) {
  res.render('register', { title: 'Create account', error: null });
}

async function register(req, res) {
  if (!onlyStrings(req.body)) {
    const message = 'Only string values are allowed.';
    return res.status(400).json({ ok: false, error: message });
  }
  const { email, password } = req.body;
  if (!email || !password) {
    const message = 'Email and password are required.';
    return res.status(400).json({ ok: false, error: message });
  }

  if (email.length < 8 & password < 8) {
    const message = 'Email or Password less than 8';
    return res.status(400).json({ ok: false, error: message });
  }

  const cleanEmail = normalizeEmail(email);
  const existing = await findUserByEmail(cleanEmail);
  if (existing) {
    const message = 'An account with that email already exists.';
    return res.status(400).json({ ok: false, error: message });
  }

  const passwordHash = hashPassword(password);
  const user = await createUser({ email: cleanEmail, passwordHash });

  req.session.userId = user.id;
  req.session.role = user.role;
  return res.json({ ok: true });
}

async function showLogin(req, res) {
  res.render('login', { title: 'Log in', error: null });
}

async function login(req, res) {
  if (!onlyStrings(req.body)) {
    const message = 'Only string values are allowed.';
    return res.status(400).json({ ok: false, error: message });
  }
  const { email, password } = req.body;
  if (!email || !password) {
    const message = 'Missing credentials.';
    return res.status(400).json({ ok: false, error: message });
  }

  const user = await findUserByEmail(normalizeEmail(email));
  const valid = user && verifyPassword(password, user.password);
  if (!valid) {
    const message = 'Invalid email or password.';
    return res.status(400).json({ ok: false, error: message });
  }

  req.session.userId = user.id;
  req.session.role = user.role;
  return res.json({ ok: true });
}

async function logout(req, res) {
  req.session.destroy((err) => {
    if (err) {
      // eslint-disable-next-line no-console
      console.error(err);
      return res.status(500).json({ ok: false, error: 'Unable to log out.' });
    }
    return res.json({ ok: true });
  });
}

module.exports = {
  showRegister,
  register,
  showLogin,
  login,
  logout,
};
