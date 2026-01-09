import { $ } from 'bun';
import { readdir } from 'fs/promises';
import { join } from 'path';
import { execSync } from 'child_process';

const scriptsDir = join(__dirname, '../scripts');

async function handleRequest(req: Request) {
  if (req.method === 'GET') {
    let files;
    try {
      files = await readdir(scriptsDir);
    } catch (error) {
      console.error(error);
      return new Response(JSON.stringify({ error: 'Failed to list scripts' }), { status: 500 });
    }

    const options = files.map(file => `<option value="${file}">${file}</option>`).join('');

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Unknown</title>
    <style>
        body {
            background-color: #050505;
            color: #d0d0d0;
            font-family: 'Courier New', Coupon, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            overflow: hidden;
            text-align: center;
        }
        .container {
            max-width: 800px;
            padding: 2rem;
            position: relative;
        }
        .quote {
            font-size: 1.2rem;
            line-height: 1.6;
            margin-bottom: 4rem;
            opacity: 0.8;
            font-style: italic;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
            animation: fadein 3s ease-in;
        }
        .controls {
            opacity: 0;
            animation: fadein 3s ease-in 2s forwards;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 1rem;
        }
        select {
            background: transparent;
            border: none;
            border-bottom: 1px solid #333;
            color: #888;
            padding: 0.5rem;
            font-family: inherit;
            font-size: 1rem;
            outline: none;
            cursor: pointer;
            transition: all 0.3s;
        }
        select:hover, select:focus {
            color: #fff;
            border-bottom-color: #fff;
        }
        button {
            background: transparent;
            border: 1px solid #333;
            color: #555;
            padding: 0.5rem 2rem;
            font-family: inherit;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.5s;
            margin-top: 1rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        button:hover {
            border-color: #fff;
            color: #fff;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
        }
        pre#result {
            margin-top: 3rem;
            color: #fff;
            font-size: 0.9rem;
            white-space: pre-wrap;
            opacity: 0.9;
        }
        .hidden-label {
            display: none;
        }
        @keyframes fadein {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="quote">
            "The oldest and strongest emotion of mankind is fear, and the oldest and strongest kind of fear is fear of the unknown. To attempt to solve what remains unseen is an act of defiance against that primal instinct. Yet, the one who always succeeds is the one who never stops searching for the unknown."
        </div>
        
        <form id="commandForm" class="controls">
            <label for="cmd" class="hidden-label">Choose your path:</label>
            <select id="cmd" name="cmd">
                <option value="" disabled selected>Select the unseen...</option>
                ${options}
            </select>
            <button type="submit">Defy the Instinct</button>
        </form>

        <pre id="result"></pre>
    </div>

    <script>
        document.getElementById('commandForm').addEventListener('submit', async (event) => {
            event.preventDefault();
            const cmd = document.getElementById('cmd').value;
            if (!cmd) return;

            const btn = document.querySelector('button');
            const originalText = btn.textContent;
            btn.textContent = 'Searching...';
            btn.disabled = true;

            try {
                const response = await fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ cmd })
                });

                const data = await response.json();
                const result = data.result || data.error;
                
                // Typing effect for result
                const resultEl = document.getElementById('result');
                resultEl.textContent = '';
                let i = 0;
                const typeResult = () => {
                    if (i < result.length) {
                        resultEl.textContent += result.charAt(i);
                        i++;
                        setTimeout(typeResult, 10);
                    }
                };
                typeResult();

            } catch (e) {
                document.getElementById('result').textContent = "The unknown remains elusive.";
            } finally {
                btn.textContent = originalText;
                btn.disabled = false;
            }
        });
    </script>
</body>
</html>`;

    return new Response(html, {
      headers: { 'Content-Type': 'text/html' }
    });
  } else if (req.method === 'POST') {
    let cmd;
    try {
      const body = await req.formData();
      cmd = body.get("cmd") || "id";
    } catch (e) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400 });
    }

    if (!cmd || typeof cmd !== 'string') {
      return new Response(JSON.stringify({ error: 'Command not provided or invalid' }), { status: 400 });
    }

    let result;
    try {
      result = await $`bash ./scripts/${cmd}`.text();
    } catch (error: any) {
      console.error(error);
      return new Response(JSON.stringify({ error: error.message }), { status: 500 });
    }

    return new Response(JSON.stringify({ result }), {
      headers: { 'Content-Type': 'application/json' }
    });
  }

  return new Response('Method Not Allowed', { status: 405 });
}

Bun.serve({
  port: 3000,
  fetch: handleRequest
});
