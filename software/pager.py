import imapclient
import datetime
import time
import email

from log import logger

def show(message):
  print(message.text)

username_and_password = input("username password: ")
(username, password) = username_and_password.split(" ", 1)

commands = {
  "show": show
}

# Some definitions
# email: The email object returned by email.message_from_bytes
# command: The action that should be carried out
# message: The text inside a "show" command

def fetch_emails(server, message_ids):
  return [email.message_from_bytes(message_data[b'RFC822']) for uid, message_data in server.fetch(message_ids, 'RFC822').items()]

def process_emails(server):
  logger.debug("Processing unseen messages...")
  message_ids = server.search("UNSEEN")
  emails = fetch_emails(server, message_ids)
  logger.debug("Unseen: " + str(len(emails)))

  for mail in emails:
    logger.debug(mail.get('From') + " " + mail.get('Subject'))


while (True):
  with imapclient.IMAPClient("imap.gmail.com") as server:
    server.login(username, password)
    server.select_folder("INBOX")

    process_emails(server)
    logger.debug("Entering IDLE mode.")
    server.idle()

    while(True):
      try:
        logger.debug("IDLE check...")
        responses = server.idle_check(timeout=20)
        
        if responses:
          logger.debug("Exiting IDLE mode.")
          server.idle_done()
          process_emails(server)

          logger.debug("Entering IDLE mode.")
          server.idle()

      except KeyboardInterrupt:
        break

    server.idle_done()
    logger.debug("\nIDLE mode done")
    server.logout()
