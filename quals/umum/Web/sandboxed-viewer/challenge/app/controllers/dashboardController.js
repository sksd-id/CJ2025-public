const { listUploads, recordUpload } = require('../utils');
const { onlyStrings } = require('../services/validators');

async function showHome(req, res) {
  if (req.user) {
    return res.redirect('/dashboard');
  }
  res.render('home', { title: 'Sandboxed Viewer', user: null });
}

async function showDashboard(req, res) {
  const uploads = await listUploads({ userId: req.user.id });
  res.render('dashboard', {
    title: 'Dashboard',
    uploads,
  });
}

async function handleUpload(req, res) {
  const respondError = (message, status = 400) =>
    res.status(status).json({ ok: false, error: message });

  if (!onlyStrings(req.body)) return respondError('Only string form fields are allowed.');
  const file = req.file;
  if (!file) return respondError('Please choose a file to upload.');

  try {
    await recordUpload({
      userId: req.user.id,
      storedName: file.filename,
      originalName: file.originalname,
      mimeType: file.mimetype,
    });
  } catch (err) {
    // eslint-disable-next-line no-console
    console.error(err);
    return respondError('Upload failed. Please try again later.', 500);
  }

  return res.json({
    ok: true,
    message: 'File uploaded successfully.',
    path: `/files/${file.filename}`,
  });
}

module.exports = { showHome, showDashboard, handleUpload };
