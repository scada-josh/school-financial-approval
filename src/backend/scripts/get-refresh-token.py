#!/usr/bin/env python3
"""
Generate Google OAuth refresh token for Google Drive uploads.

Usage:
    python3 src/backend/scripts/get-refresh-token.py path/to/client_secret.json

The script will:
1. Read OAuth client credentials from the JSON file
2. Open a browser for you to authorize the app
3. Print the refresh token

Copy the refresh token and set it as GOOGLE_DRIVE_REFRESH_TOKEN in Render.
"""

import sys
import json
import urllib.parse
import urllib.request
import http.server
import socketserver
import threading
import webbrowser
import os

# Google OAuth endpoints
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
REDIRECT_URI = 'http://localhost:8080/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/drive']

authorization_code = None


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global authorization_code
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        if parsed.path == '/oauth2callback':
            if 'code' in query:
                authorization_code = query['code'][0]
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("""
                <html>
                <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                    <h2>Authorization successful!</h2>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
                """.encode('utf-8'))
            else:
                error = query.get('error', ['unknown'])[0]
                self.send_response(400)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"""
                <html>
                <body>
                    <h2>Authorization failed: {error}</h2>
                </body>
                </html>
                """.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress server logs
        pass


def find_free_port(start=8080, end=8100):
    """Find a free port in the given range"""
    for port in range(start, end):
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue
    raise RuntimeError("No free port found")


def get_refresh_token(client_secret_path):
    with open(client_secret_path, 'r') as f:
        client_config = json.load(f)

    # Handle both Google Cloud client_secret_xxx.json and Desktop app formats
    if 'installed' in client_config:
        client = client_config['installed']
    elif 'web' in client_config:
        client = client_config['web']
    else:
        client = client_config

    client_id = client['client_id']
    client_secret = client['client_secret']

    # Find free port and start local callback server
    port = find_free_port()
    redirect_uri = f'http://localhost:{port}/oauth2callback'

    # Start local callback server
    with socketserver.TCPServer(("localhost", port), CallbackHandler) as httpd:
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        try:
            auth_params = {
                'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': ' '.join(SCOPES),
                'access_type': 'offline',
                'prompt': 'consent'
            }
            auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

            print("")
            print("=" * 60)
            print(f"Opening browser for Google authorization on port {port}...")
            print("=" * 60)
            print("")

            webbrowser.open(auth_url)

            print("Waiting for authorization...")
            while authorization_code is None:
                import time
                time.sleep(0.5)

        finally:
            httpd.shutdown()

    if not authorization_code:
        print("Failed to get authorization code")
        sys.exit(1)

    # Exchange code for refresh token
    token_data = {
        'code': authorization_code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    req = urllib.request.Request(
        TOKEN_URL,
        data=urllib.parse.urlencode(token_data).encode('utf-8'),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        token_response = json.loads(response.read().decode('utf-8'))

    refresh_token = token_response.get('refresh_token')
    access_token = token_response.get('access_token')

    print("")
    print("=" * 60)
    print("Success! Here are your credentials:")
    print("=" * 60)
    print(f"GOOGLE_DRIVE_CLIENT_ID={client_id}")
    print(f"GOOGLE_DRIVE_CLIENT_SECRET={client_secret}")
    print(f"GOOGLE_DRIVE_REFRESH_TOKEN={refresh_token}")
    print("")
    print("Copy these values and set them as environment variables in Render.")
    print("=" * 60)

    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'access_token': access_token
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 src/backend/scripts/get-refresh-token.py path/to/client_secret.json")
        sys.exit(1)

    client_secret_path = sys.argv[1]
    if not os.path.exists(client_secret_path):
        print(f"File not found: {client_secret_path}")
        sys.exit(1)

    get_refresh_token(client_secret_path)
