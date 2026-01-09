const { listUsers, listUploads } = require('../utils');

async function showAdmin(req, res) {
  const [users, uploads] = await Promise.all([listUsers(), listUploads()]);
  res.render('admin', {
    title: 'Admin dashboard',
    users,
    uploads,
    js: req.query.js ?? ''
  });
}

module.exports = { showAdmin };
