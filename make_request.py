import requests

API_URL = "http://localhost:5005/account"

def send_request(action, username, password):
    """
    Sends a request to the account server.

    :param action: 0 (verify), 1 (create), 2 (delete)
    :param username: Account username
    :param password: Account password
    :return: API response as a dictionary
    """
    data = {"action": action, "username": username, "password": password}

    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        return response.json()  # Return the server's JSON response
    except requests.exceptions.HTTPError as http_err:
        try:
            error_response = response.json()  # Attempt to get error details
        except ValueError:
            error_response = {"error": "Unknown error occurred"}

        return {"error": f"Request failed: {http_err}", "details": error_response}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request failed: {req_err}"}

# Testing the different cases
if __name__ == "__main__":
    # print("Create Account:", send_request(1, "testuser2", "password123"))
    # print("Verify Account:", send_request(0, "testuser2", "password123"))
    # print("Verify Account (Wrong Password):", send_request(0, "testuser2", "wrongpassword"))
    # print("Verify Account (Non-existent User):", send_request(0, "nonexistent", "password123"))
    print("Delete Account:", send_request(2, "testuser", "password123"))
