import imapclient
import datetime
import time
import email
import re
import smtplib

# Fix the locale so we behave the same in all locations. 
import locale
locale.setlocale(locale.LC_ALL, "C")

from log import logger

imap_server = input("IMAP server: ")
imap_username = input("IMAP username: ")
imap_password = input("IMAP password: ")
smtp_server = input("SMTP server: ")
smtp_username = input("SMTP username: ")
smtp_password = input("SMTP password: ")
smtp_to = input("SMTP to: ")
smtp_from = input("SMTP from: ")

def show(mail):
  message = mail.get("Subject")
  return "Showed message: " + message

def info(mail):
  logger.debug("info command - ignoring")
  return None

def command_not_parsed(mail, subject):
  message = "No command found in email subject '" + str(subject) + "'"
  return message

def command_unrecognised(mail, command_name):
  message = "Command '" + command_name + "' not recognised. "
  return message

commands = {
  "show": show,
  "info": info,
}

# Some definitions
# email: The email object returned by email.message_from_bytes
#   Note that, to avoid name shadowing the email import, local variables
#   will be called mail, mails, etc. 
# command: The action that should be carried out
# message: The text inside a "show" command

def process_emails(server):
  logger.debug("Processing unseen messages...")
  message_ids = server.search("UNSEEN")
  emails = fetch_emails(server, message_ids)
  logger.debug("Unseen: " + str(len(emails)))

  for mail in emails:
    command = get_command(mail)
    result = command(mail)
    send_response(result)

    logger.debug(mail.get('From') + " " + mail.get('Subject'))

def fetch_emails(server, message_ids):
  return [email.message_from_bytes(message_data[b'RFC822']) for uid, message_data in server.fetch(message_ids, 'RFC822').items()]

def get_command(mail):
  # The command is the first word in the subject line. 
  # Commands are made up of "word" characters as defined by Python regex \w
  # Commands will be converted to lowercase using the "C" locale
  # The "info" command is ignored to avoid infinite loops if the pager is replying to its own inbox.

  subject = mail.get("Subject")
  command_name_match = re.match("\w+", subject)
  if not command_name_match:
    return lambda mail: command_not_parsed(mail, subject)

  command_name = command_name_match.group(0).lower()
  if command_name in commands:
    return commands[command_name]
  else:
    return lambda mail: command_unrecognised(mail, command_name)

def send_response(result):
  if not result:
    logger.debug("No command response (probably an info command)")
    return

  message = email.message.EmailMessage()
  message["Subject"] = "info: Response from pager"
  message["To"] = smtp_to
  message["From"] = smtp_from
  message.set_content(result)

  with smtplib.SMTP_SSL(smtp_server) as smtp:
    smtp.login(smtp_username, smtp_password)
    smtp.send_message(message)

  logger.debug(result)

with imapclient.IMAPClient(imap_server) as server:
  server.login(imap_username, imap_password)
  server.select_folder("INBOX")

  while True:
    try: 
      process_emails(server)
      time.sleep(10)
    except KeyboardInterrupt:
      break
