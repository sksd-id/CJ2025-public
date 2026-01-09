const express = require('express');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const EXECUTION_TIMEOUT = 5000;
const MAX_CODE_LENGTH = 10000;
const ADMIN_TOKEN = process.env.ADMIN_TOKEN;
const TEMP_DIR = '/tmp';

async function executeCode(code) {
    return new Promise((resolve) => {
        const filename = `sandbox_${crypto.randomBytes(16).toString('hex')}.js`;
        const filepath = path.join(TEMP_DIR, filename);

        try {
            fs.writeFileSync(filepath, code);
        } catch (err) {
            return resolve({ success: false, error: 'Failed to create temp file' });
        }

        const child = spawn('node', [path.join(__dirname, 'runner.js'), filepath], {
            timeout: EXECUTION_TIMEOUT,
            stdio: ['ignore', 'pipe', 'pipe'],
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        const timeout = setTimeout(() => {
            child.kill('SIGKILL');
        }, EXECUTION_TIMEOUT);

        child.on('close', (code) => {
            clearTimeout(timeout);

            try {
                fs.unlinkSync(filepath);
            } catch (e) {}

            if (stdout) {
                try {
                    const result = JSON.parse(stdout.trim());
                    return resolve(result);
                } catch (e) {
                    console.error(e)
                    return resolve({ success: false, error: 'Invalid response from runner' });
                }
            }

            if (stderr) {
                return resolve({ success: false, error: stderr.trim() });
            }

            return resolve({ success: false, error: 'Execution timeout or no output' });
        });

        child.on('error', (err) => {
            clearTimeout(timeout);
            try {
                fs.unlinkSync(filepath);
            } catch (e) {}
            resolve({ success: false, error: err.message });
        });
    });
}

app.get('/', (req, res) => {
    res.send(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JS Sandbox</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Courier New', monospace;
            background: #1a1a2e;
            color: #eee;
            padding: 2rem;
            margin: 0;
            min-height: 100vh;
        }
        .container { max-width: 900px; margin: 0 auto; }
        h1 { color: #00d4ff; margin-bottom: 2rem; }
        textarea {
            width: 100%;
            height: 300px;
            background: #16213e;
            color: #00ff88;
            border: 1px solid #0f3460;
            padding: 1rem;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            resize: vertical;
            border-radius: 8px;
        }
        textarea:focus { outline: none; border-color: #00d4ff; }
        button {
            background: #00d4ff;
            color: #1a1a2e;
            border: none;
            padding: 0.8rem 2rem;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin-top: 1rem;
            border-radius: 5px;
            transition: all 0.3s;
        }
        button:hover { background: #00ff88; }
        button:disabled { background: #555; cursor: not-allowed; }
        #output {
            margin-top: 2rem;
            background: #16213e;
            padding: 1rem;
            border-radius: 8px;
            min-height: 100px;
            white-space: pre-wrap;
            font-size: 14px;
        }
        .success { border-left: 4px solid #00ff88; }
        .error { border-left: 4px solid #ff4444; }
        .result { color: #00ff88; }
        .error-msg { color: #ff4444; }
    </style>
</head>
<body>
    <div class="container">
        <h1>JavaScript Sandbox</h1>
        <form id="codeForm">
            <textarea id="code" placeholder="// Write your JavaScript code here...
return 1+1;
"></textarea>
            <button type="submit" id="runBtn">Run Code</button>
        </form>
        <div id="output"></div>
    </div>
    <script>
        document.getElementById('codeForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const code = document.getElementById('code').value;
            const btn = document.getElementById('runBtn');
            const output = document.getElementById('output');

            btn.disabled = true;
            btn.textContent = 'Running...';
            output.className = '';
            output.innerHTML = '<span style="color:#888">Executing...</span>';

            try {
                const res = await fetch('/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ code })
                });
                const data = await res.json();

                if (data.success) {
                    output.className = 'success';
                    output.innerHTML = data.result !== undefined
                        ? '<div class="result">Result: ' + data.result + '</div>'
                        : '<span style="color:#888">No output</span>';
                } else {
                    output.className = 'error';
                    output.innerHTML = '<div class="error-msg">Error: ' + data.error + '</div>';
                }
            } catch (err) {
                output.className = 'error';
                output.innerHTML = '<div class="error-msg">Request failed: ' + err.message + '</div>';
            } finally {
                btn.disabled = false;
                btn.textContent = 'Run Code';
            }
        });
    </script>
</body>
</html>`);
});

app.post('/run', async (req, res) => {
    const { code, token } = req.body;

    if (!token || token !== ADMIN_TOKEN) {
        return res.status(403).json({ success: false, error: 'Unauthorized' });
    }

    if (!code || typeof code !== 'string') {
        return res.status(400).json({ success: false, error: 'Code is required' });
    }

    if (code.length > MAX_CODE_LENGTH) {
        return res.status(400).json({
            success: false,
            error: `Code too long. Maximum ${MAX_CODE_LENGTH} characters allowed.`
        });
    }

    const result = await executeCode(code);
    res.json(result);
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`JS Sandbox running on port ${PORT}`);
});
