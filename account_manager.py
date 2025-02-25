import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ACCOUNT_FILE = "account_information.txt"
accounts = {}  # Format: {username: {"id": user_id, "password": password}}
next_account_id = 1

def load_accounts():
    """
    Loads account information from ACCOUNT_FILE.
    Expected format per line: username, password, user_id
    """
    global accounts, next_account_id
    accounts = {}
    if not os.path.exists(ACCOUNT_FILE):
        next_account_id = 1
        return

    with open(ACCOUNT_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # skip blank lines
            parts = line.split(",")
            if len(parts) != 3:
                continue  # skip malformed lines
            username = parts[0].strip()
            password = parts[1].strip()
            try:
                user_id = int(parts[2].strip())
            except ValueError:
                continue
            accounts[username] = {"id": user_id, "password": password}
    
    if accounts:
        next_account_id = max(info["id"] for info in accounts.values()) + 1
    else:
        next_account_id = 1

def save_accounts():
    """
    Saves the current account information to ACCOUNT_FILE.
    """
    with open(ACCOUNT_FILE, "w") as f:
        for username, info in accounts.items():
            f.write(f"{username}, {info['password']}, {info['id']}\n")

# Load accounts at startup
load_accounts()

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, response_data):
        """
        Sends a JSON response to the client.
        """
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

    def do_POST(self):
        global next_account_id, accounts
        
        if self.path != "/account":
            self._send_response(404, {"error": "Not found"})
            return
        
        # Read and parse JSON request body
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self._send_response(400, {"error": "Invalid JSON format"})
            return
        
        action = data.get("action")
        username = data.get("username")
        password = data.get("password")

        if action is None or username is None or password is None:
            self._send_response(400, {"error": "Missing parameters. Provide action, username, and password."})
            return
        
        # Action 0: Check credentials and return account ID
        if action == 0:
            if username not in accounts:
                self._send_response(400, {"error": "No Account with that Username"})
                return
            if accounts[username]['password'] != password:
                self._send_response(400, {"error": "Password Incorrect"})
                return
            self._send_response(200, {"message": "Credentials verified.", "account_id": accounts[username]['id']})
            return

        # Action 1: Create a new account
        if action == 1:
            if username in accounts:
                self._send_response(400, {"error": "Account already exists."})
                return
            account_id = next_account_id
            accounts[username] = {'id': account_id, 'password': password}
            next_account_id += 1
            save_accounts()
            self._send_response(201, {"message": "Account created successfully.", "account_id": account_id})
            return

        # Action 2: Delete an account
        if action == 2:
            if username not in accounts:
                self._send_response(400, {"error": "No Account with that Username"})
                return
            if accounts[username]['password'] != password:
                self._send_response(400, {"error": "Password Incorrect"})
                return
            del accounts[username]
            save_accounts()
            self._send_response(200, {"message": "Account deleted successfully."})
            return

        self._send_response(400, {"error": "Invalid action. Use 1 (create), 2 (delete), or 0 (verify)."})

def run_server(port=5005):
    server_address = ("", port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
