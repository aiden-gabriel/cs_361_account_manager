Requesting Data

1. The account manager must be running. You can run it with the code below:
    python account_manager.py


2. Then you can send a request in this format:
    Requests should be written to the am_comm.txt file in the form:
    action, username, password
    
    username and password can be any string
    actions will be single integers (0, 1, 2) and are described below


3. Options for actions:
    0 - Check credentials: this will check that the given username exists and that the password is correct for it.
        - If the username is incorrect it returns: 
            ERROR: No account with that username
        - If the password is incorrect it returns:
            ERROR: Password incorrect
        - If the username and password are correct it will return:
            SUCCESS: Verified, ID 1
    
    1 - Create account: this will create a new account with the given username and password.
        - If an account with the username already exists it will return:
            ERROR: Account already exists
        - If it's a new username it will give the account an account id and will store the  account information in account_information.txt, and return:
            SUCCESS: Account created, ID 1
    
    2 - Delete account: this will delete the account information of the account corresponding to the given username and password.
        - If there is no account with that username:
            ERROR: No account with that username
        - If the password is incorrect:
            ERROR: Password incorrect
        - If the account exists, it's information will be permanently deleted from account_information.txt and it will return:
            SUCCESS: Account deleted
            










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
