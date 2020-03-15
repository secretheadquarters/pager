#!python3

import imapclient
import datetime
import time
import email
import re
import smtplib

# Fix the locale so we behave the same in all locations. 
import locale
locale.setlocale(locale.LC_ALL, "C")

import log
logger = log.logger

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
  
def get_logs(mail):
  with open(log.log_filename) as log_file:
    message = log_file.read()
    return message

def command_not_parsed(mail, subject):
  message = "No command found in email subject '" + str(subject) + "'"
  return message

commands = {
  "show": show,
  "info": info,
  "get logs": get_logs,
}

# Some definitions
# email: The email object returned by email.message_from_bytes
#   Note that, to avoid name shadowing the email import, local variables
#   will be called mail, mails, etc. 
# command: The action that should be carried out
# message: The text inside a "show" command

def process_emails(server, commands):
  # It seems that search can get stuck always returning the 
  # same result (usually 0 messages) if you keep asking the 
  # same thing. Doing a SELECT to refresh the search results
  # seems to avoid this. 
  server.select_folder("INBOX")
  message_ids = server.search("ALL")
  uids_and_emails = fetch_emails(server, message_ids)
  logger.debug("Messages: " + str(len(uids_and_emails)))

  for uid, mail in uids_and_emails:
    command = get_command(commands, mail)
    result = command(mail)
    send_response(result)
    move_mail_to_done(server, uid)

    logger.debug(mail.get('From') + " " + mail.get('Subject'))

def fetch_emails(server, uids):
  return [(uid, email.message_from_bytes(message_data[b'RFC822'])) for uid, message_data in server.fetch(uids, 'RFC822').items()]

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

def move_mail_to_done(server, uid):
  server.move(uid, "Done")

with imapclient.IMAPClient(imap_server) as server:
  server.login(imap_username, imap_password)
  server.select_folder("INBOX")
  
  if not server.folder_exists("Done"):
    server.create_folder("Done")

  while True:
    try: 
      process_emails(server, commands)
      time.sleep(10)
    except KeyboardInterrupt:
      break
