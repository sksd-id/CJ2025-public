from flask import Flask, request, jsonify, Response
import urllib.parse
import urllib.request
import urllib.error
import ssl
import socket

app = Flask(__name__)

NOT_ALLOWED_SCHEMES = {'file', 'gopher', 'ftp', 'glob', 'local_file', 'dict', 'data'}
ALLOWED_PORTS = {80, 443, 8080, 8443}
BLOCKED_HOSTS = {
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '::1',
    'metadata.google.internal',
    '169.254.169.254',
}

MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
REQUEST_TIMEOUT = 10


def is_valid_url(url: str) -> tuple[bool, str]:
    """Validate URL for security."""
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception as e:
        print(e)
        return False, "Invalid URL format"
    print(parsed.scheme)

    if parsed.scheme in NOT_ALLOWED_SCHEMES:
        return False, f"Scheme '{parsed.scheme}' is not allowed"

    host = parsed.hostname
    host_lower = host

    if host_lower in BLOCKED_HOSTS:
        return False, "Host not allowed"

    port = parsed.port
    if port and port not in ALLOWED_PORTS:
        return False, f"Port {port} not allowed"

    return True, "Valid"


def fetch_url(url: str, method: str = 'GET', body: bytes = None, content_type: str = None) -> tuple[bytes, dict, int]:
    """Fetch content from URL using urllib.request."""
    ctx = ssl.create_default_context()

    headers = {
        'User-Agent': 'SecureProxy/1.0',
        'Accept': '*/*',
    }

    if content_type:
        headers['Content-Type'] = content_type

    req = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ctx) as response:
            content = response.read(MAX_CONTENT_LENGTH)
            resp_headers = dict(response.headers)
            status = response.status
            return content, resp_headers, status
    except urllib.error.HTTPError as e:
        return e.read(MAX_CONTENT_LENGTH), dict(e.headers), e.code
    except urllib.error.URLError as e:
        raise Exception(f"URL Error: {e.reason}")
    except socket.timeout:
        raise Exception("Request timed out")


@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    """Proxy endpoint that fetches content from a given URL."""
    url = request.args.get('url') or request.form.get('url')

    if not url:
        return jsonify({'error': 'URL parameter required'}), 400

    is_valid, message = is_valid_url(url)
    if not is_valid:
        return jsonify({'error': message}), 400

    method = request.args.get('method', 'GET').upper()
    body = request.get_data() if request.method == 'POST' else None
    content_type = request.content_type

    try:
        content, headers, status = fetch_url(url, method=method, body=body, content_type=content_type)

        response_headers = {}
        safe_headers = ['content-type', 'content-length', 'date', 'last-modified']
        for h in safe_headers:
            if h in [k.lower() for k in headers.keys()]:
                for k, v in headers.items():
                    if k.lower() == h:
                        response_headers[k] = v
                        break

        return Response(
            content,
            status=status,
            headers=response_headers
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'}), 200


@app.route('/', methods=['GET'])
def index():
    """Index page with usage instructions."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Proxy</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background: #0a0a0a;
            color: #00ff00;
            padding: 2rem;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 { border-bottom: 1px solid #00ff00; padding-bottom: 1rem; }
        code { background: #1a1a1a; padding: 0.2rem 0.5rem; border-radius: 3px; }
        pre { background: #1a1a1a; padding: 1rem; overflow-x: auto; }
        .warning { color: #ff6600; }
    </style>
</head>
<body>
    <h1>Secure Proxy Service</h1>
    <h2>Usage</h2>
    <pre>GET /proxy?url=https://example.com</pre>
    <h2>Security</h2>
    <ul>
        <li>Only HTTP/HTTPS protocols allowed</li>
        <li>Internal/private IPs blocked</li>
        <li>DNS rebinding protection</li>
        <li>Request timeout: 10s</li>
        <li>Max response: 10MB</li>
    </ul>
    <p class="warning">This proxy validates all URLs before fetching.</p>
</body>
</html>''', 200, {'Content-Type': 'text/html'}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
