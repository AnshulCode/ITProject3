import socket
import signal
import sys
import random


passwords = {}
secrets = {}
cookies = {}


# Read a command line argument for the port where the server
# must run.
port = 8070
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print "Here is the", tag
    print "\"\"\""
    print value
    print "\"\"\""
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users

######################## OUR CODE ########################

# sends response if no cookie is present
def if_no_cookie(client,username,password):

    html_content_to_send = login_page
    if (not username and password) or (username and not password): # One field is missing
        print("One field is missing")
        html_content_to_send = bad_creds_page
    elif (username in passwords) and (username in secrets): # Username and Password match
        print("Properly Authenticated")
        if passwords.get(username) == password:
            html_content_to_send = success_page + secrets.get(username)
        else:
            html_content_to_send = bad_creds_page
    r = random.getrandbits(64)
    
    headers_to_send = 'Set-Cookie: token='+str(r)+"\r\n"
   
         
    cookies[r] = (username,password,html_content_to_send)
    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    cookie_id = -1
    print "Served one request/connection!"
    print

# Read the username & passwords and store them
with open('passwords.txt') as file:
    for line in file:
        username_password = line.split()
        passwords[username_password[0]] = username_password[1]

# Read the username & secret and store them
with open('secrets.txt') as file:
    for line in file:
        username_secret = line.split()
        secrets[username_secret[0]] = username_secret[1]


######################## OUR CODE ########################


### Loop to accept incoming HTTP connections and respond.
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)
    l = headers.split('\n')
    is_cookie = False
    cookie_id = -1

    #search for cookie header
    for h in l:
        if(h.startswith("Cookie: token=")):
            s = h.replace("Cookie: token=","")
            print("Cookie ID : "+ str(s))
            is_cookie = True
            cookie_id = int(s)
            if cookie_id in cookies:
                print("ID Presennt")
            
            break

    username_and_password = body.split('&')
    username = None
    password = None

    for item in username_and_password:
            line = item.split('=')
            print(line)
            if line[0] == 'username':
                 username = line[1]
            elif line[0] == 'password':
                password = line[1]

    # main code for responses
    if(is_cookie):
        if(cookie_id not in cookies):
            headers_to_send = ""
            response  = 'HTTP/1.1 200 OK\r\n'
            response += headers_to_send
            response += 'Content-Type: text/html\r\n\r\n'
            response += bad_creds_page
            client.send(response)
            client.close()
        else:
            client.send(cookies[cookie_id][2])
            client.close()
    else:
        # does if cookie header not present
        if_no_cookie(client,username,password)


   # print("USERNAME: ", username)
   # print("PASSWORD: ", password)

    
   

   
    print(cookies)
    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions

######################## OUR CODE ########################

    # Parsing the username and password from the body entity. If they are not present, username and password are set to None type
    

# We will never actually get here.
# Close the listening socket
sock.close()
