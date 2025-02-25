Requesting Data

1. The account manager must be running. You can run it with the code below:
    python account_manager.py

2. To request data you first have to have the request library imported:
    import requests

3. Then you can send a request in this format:
    API_URL = "http://localhost:5005/account"
    data = {"action": action, "username": username, "password": password}
    response = requests.post(API_URL, json=data)

4. Options for actions:
    0 - Check credentials: this will check that the given username exists and that the password is correct for it.
        - If the username is incorrect it returns: 
            400, {"error": "No Account with that Username"}
        - If the password is incorrect it returns:
            400, {"error": "Password Incorrect"}
        - If the username and password are correct it will return:
            200, {"message": "Credentials verified.", "account_id": accounts[username]['id']}
    
    1 - Create account: this will create a new account with the given username and password.
        - If an account with the username already exists it will return:
            400, {"error": "Account already exists."}
        - If it's a new username it will give the account an account id and will store the  account information in account_information.txt, and return:
            201, {"message": "Account created successfully.", "account_id": account_id}
    
    2 - Delete account: this will delete the account information of the account corresponding to the given username and password.
        - If there is no account with that username:
            400, {"error": "No Account with that Username"}
        - If the password is incorrect:
            400, {"error": "Password Incorrect"}
        - If the account exists, it's information will be permanently deleted from account_information.txt and it will return:
            200, {"message": "Account deleted successfully."}
            

Client (Your Program)              Port 5005        Server (Account Manager)

Writes data and sends w/                            Server takes in request &
requests.post(API_URL, data) ---> ]--------[ --->   parses arguments
                                                                ||
                                                                ||
                                                                \/
                                                    Server checks credetials &
                                                    performs task
                                                                ||
                                                                ||
                                                                \/
Client recieves and parses                          Server gets response data 
return message               <--- ]--------[ <---   and returns it
