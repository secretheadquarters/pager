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

def process_emails(server, commands):
  logger.debug("Processing unseen messages...")
  message_ids = server.search("UNSEEN")
  emails = fetch_emails(server, message_ids)
  logger.debug("Unseen: " + str(len(emails)))

  for mail in emails:
    command = get_command(commands, mail)
    result = command(mail)
    send_response(result)

    logger.debug(mail.get('From') + " " + mail.get('Subject'))

def fetch_emails(server, message_ids):
  return [email.message_from_bytes(message_data[b'RFC822']) for uid, message_data in server.fetch(message_ids, 'RFC822').items()]

def get_command(cmmands, mail):
  # The command is the text at the start of the subject line. 
  # Commands are matched by case insensitive regex using the "C" locale
  # Command matches are performed in an arbitrary order, and the first match will be taken.
  # Commands are passed the email object and can perform further analysis on this as required.

  subject = mail.get("Subject")
  for command_regex in commands.keys():
    if re.match(command_regex, subject, re.I):
      return commands[command_regex]
      
  return lambda mail: command_not_parsed(mail, subject)

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
      process_emails(server, commands)
      time.sleep(10)
    except KeyboardInterrupt:
      break
