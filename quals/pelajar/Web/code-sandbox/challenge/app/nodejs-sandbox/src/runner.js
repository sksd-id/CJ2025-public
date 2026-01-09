const sandbox = require('@nyariv/sandboxjs');
const fs = require('fs');

const s = new sandbox.default();

const codePath = process.argv[2];
if (!codePath) {
    console.error(JSON.stringify({ success: false, error: 'No code file provided' }));
    process.exit(1);
}

try {
    const code = fs.readFileSync(codePath, 'utf-8');
    const exec = s.compile(code);
    const result = exec().run();

    console.log(JSON.stringify({
        success: true,
        result: result !== undefined ? String(result) : undefined,
    }));
} catch (error) {
    console.log(JSON.stringify({
        success: false,
        error: error.message,
    }));
}
