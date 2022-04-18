#!/usr/bin/python3

## PY-MAILER
##
## Python-based utility for sending server emails over SMTP (primarily geared
## for working with gmail SMTP service)


# IMPORTS AND CONSTANTS
import json
import io
import smtplib
import logging
import argparse
import sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

confFile = "__CONF__"  # Location of pymailer config file


# FUNCTIONS
def loadConfig(file):
    # Loads and parses the configuration file. Returns a dictionary containing
    # program configuration values.
    configBuffer = io.StringIO("")
    with open(file, 'r') as f:
        for line in f:           # This loop is to strip comments out of the
            line = line.strip()  # config file, thus leaving pure JSON for
            if not line == "":   # json.loads()
                if not line[0] == "#":
                    configBuffer.write(line)
    config = json.loads(configBuffer.getvalue())
    configBuffer.close()
    return config

def build_eMail(to, subject, content):
    # Creates the email as a MIME object, returned as a string
    email = MIMEMultipart()
    email['From'] = config['username']
    email['To'] = to
    email['Subject'] = subject
    email.attach(MIMEText(content, 'plain'))
    return email.as_string()

def send_eMail(email, to):
    # Sends an email over an SMTP connection
    sender = config['username']
    session = smtplib.SMTP(config['url'], int(config['port']))
    session.starttls()

    try:
        session.login(sender, config['passwd'])
    except:
        logging.error("Unable to send: Couldn't log in to {}".format(config['username']))
        session.quit()
        return
    
    try:
        session.sendmail(sender, to, email)
        logging.info("Email successfully sent to {}".format(to))
    except:
        logging.error("Unable to send email!")
    session.quit()
    return

def isValidEmail(address):
    # Returns True if the supplied string is a valid email address, otherwise
    # returns False
    if "@" in address and "." in address:
        return True
    else:
        return False

def buildTo(to):
    # Figures out where we're sending the email to. If a valid address was
    # supplied at the command line then it will use that, otherwise it will use
    # the default address as defined in the config file.
    if to == None or not isValidEmail(to):
        return config['sendTo']
    else:
        return to

def buildSubject(subject):
    # Figures out the subject line for the email. If a subject was supplied at
    # the command line then it will use that, otherwise it will use the default
    # subject as defined in the config file. 
    if subject == None:
        return config['subject']
    else:
        return subject

def buildContent(sin, msg):
    # Decides the message content. Prioritizes stdin, if that isn't available
    # then it uses the -m argument.
    if sin:
        return sin.read()
    elif msg:
        return msg
    else:
        logging.error("No message content was provided!")
        sys.exit()


# INITIALIZE
config = loadConfig(confFile)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(config['logFile']),
        logging.StreamHandler()
    ]
)

parser = argparse.ArgumentParser()  # Process command-line arguments
parser.add_argument("--to", "-t", type=str, help="Email address to send the message to")
parser.add_argument("--subject", "-s", type=str, help="Email subject")
parser.add_argument("--message", "-m", type=str, help="Message text")
parser.add_argument("--stdin", type=argparse.FileType('r'), default=(None if sys.stdin.isatty() else sys.stdin), help="Message text from stdin")
parser.add_argument("--version", "-v", action="store_true", default=False)
args = parser.parse_args()


# MAIN
if args.version:
    print("PyMailer version:  {}".format(config['version']))
    sys.exit()

to = buildTo(args.to)
subject = buildSubject(args.subject)
content = buildContent(args.stdin, args.message)

email = build_eMail(to, subject, content)
send_eMail(email, to)