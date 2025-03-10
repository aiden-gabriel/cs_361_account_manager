import os
import time

ACCOUNT_FILE = "account_information.txt"
REQUEST_RESPONSE_FILE = "am_comm.txt"
accounts = {}  # Format: {username: {"id": user_id, "password": password}}
next_account_id = 1

def load_accounts():
    global accounts, next_account_id
    accounts = {}
    if not os.path.exists(ACCOUNT_FILE):
        next_account_id = 1
        return

    with open(ACCOUNT_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                continue
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
    with open(ACCOUNT_FILE, "w") as f:
        for username, info in accounts.items():
            f.write(f"{username}, {info['password']}, {info['id']}\n")

# Load accounts at startup
load_accounts()

def process_request():
    global next_account_id, accounts

    if not os.path.exists(REQUEST_RESPONSE_FILE):
        return

    with open(REQUEST_RESPONSE_FILE, "r") as f:
        request_line = f.readline().strip()

    if not request_line:
        return  # No request to process

    parts = request_line.split(",")  # Format: action, username, password

    if len(parts) != 3:
        return
    
    try:
        action = int(parts[0].strip())
        username = parts[1].strip()
        password = parts[2].strip()
    except ValueError:
        return

    # Processing actions
    if action == 0:
        if username not in accounts:
            response = "ERROR: No account with that username"
        elif accounts[username]['password'] != password:
            response = "ERROR: Password incorrect"
        else:
            response = f"SUCCESS: Verified, ID {accounts[username]['id']}"
    
    elif action == 1:
        if username in accounts:
            response = "ERROR: Account already exists"
        else:
            account_id = next_account_id
            accounts[username] = {'id': account_id, 'password': password}
            next_account_id += 1
            save_accounts()
            response = f"SUCCESS: Account created, ID {account_id}"

    elif action == 2:
        if username not in accounts:
            response = "ERROR: No account with that username"
        elif accounts[username]['password'] != password:
            response = "ERROR: Password incorrect"
        else:
            del accounts[username]
            save_accounts()
            response = "SUCCESS: Account deleted"
    else:
        response = "ERROR: Invalid action (use 0, 1, or 2)"

    write_response(response)

def write_response(response):
    """
    Writes the response and clears the previous request.
    """
    with open(REQUEST_RESPONSE_FILE, "w") as f:
        f.write(response + "\n")

def run_server():
    print("Server running... Waiting for requests in am_comm.txt")

    while True:
        if os.path.exists(REQUEST_RESPONSE_FILE):
            process_request()
        time.sleep(1)  # Poll every second

if __name__ == "__main__":
    run_server()
