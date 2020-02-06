import imapclient
import datetime
import time
import email

def show(message):
  print(message.text)

username_and_password = input("username password: ")
(username, password) = username_and_password.split(" ", 1)

commands = {
  "show": show
}

while (True):
  with imapclient.IMAPClient("imap.gmail.com") as server:
    server.login(username, password)
    server.select_folder("INBOX")
    server.idle()
    
    while(True):
      try:
        responses = server.idle_check(timeout=20)
        print(str(datetime.datetime.now()) +"  Server sent:", responses if responses else "nothing")
        
        if responses:
          server.idle_done()
          print("Getting unseen messages...")
          messages = server.search("UNSEEN")
          
          for uid, message_data in server.fetch(messages, 'RFC822').items():
            email_message = email.message_from_bytes(message_data[b'RFC822'])
            print(uid, email_message.get('From'), email_message.get('Subject'))
          
          server.idle()
      except KeyboardInterrupt:
        break

    server.idle_done()
    print("\nIDLE mode done")
    server.logout()
