import imaplib
import email
from email.header import decode_header
import sqlite3
import logging
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Logging configuration
logging.basicConfig(filename='email_processor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DB_NAME = "emails.db"

def get_env_variable(name, default=None, required=False):
    """
    Get an environment variable or a default value.
    Raise an error if the variable is required but not set.
    """
    value = os.getenv(name, default)
    if required and value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value

def setup_database():
    """
    Setup SQlite database
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            subject TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
def connect_to_email_server(imap_host, username, password):
    """
    Connect to the IMAP server
    """
    try:
        server = imaplib.IMAP4_SSL(imap_host)
        server.login(username, password)
        return server
    except Exception as e:
        logging.error("Failed to connect to email server: %s", e)
        raise

def fetch_and_process_emails(server):
    """
    Fetch emails from the inbox and process the unread emails
    """
    try:
        server.select("inbox")
        status, messages = server.search(None, 'UNSEEN')
        if status != "OK" or not messages[0]:
            logging.info("No unread emails found.")
            return
        
        email_ids = messages[0].split()
        for email_id in email_ids:
            res, msg = server.fetch(email_id, "(RFC822)")
            if res != "OK":
                logging.error("Failed to fetch email ID %s", email_id)
                continue

            for response_part in msg:
                if isinstance(response_part, tuple):
                    msg_obj = email.message_from_bytes(response_part[1])
                    sender = decode_header(msg_obj["From"])[0][0]
                    subject = decode_header(msg_obj["Subject"])[0][0]
                    timestamp = msg_obj["Date"]

                    # Decode bytes to string
                    if isinstance(sender, bytes):
                        sender = sender.decode()
                    if isinstance(subject, bytes):
                        subject = subject.decode()

                    # Save email details to the database
                    save_email_to_db(sender, subject, timestamp)
                    logging.info("Processed email from: %s, Subject: %s", sender, subject)

            # Flag the processed emails as seen
            server.store(email_id, '+FLAGS', '\\Seen')

    except Exception as e:
        logging.error("Error processing emails: %s", e)

def save_email_to_db(sender, subject, timestamp):
    """
    Save the processed emails to the sqlite database
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO emails (sender, subject, timestamp) VALUES (?, ?, ?)',
                   (sender, subject, timestamp))
    conn.commit()
    conn.close()


def main():
    """
    Main function to run email processor
    """
    setup_database()
    IMAP_HOST = get_env_variable("IMAP_HOST", required=True)
    USERNAME = get_env_variable("EMAIL_USERNAME", required=True)
    PASSWORD = get_env_variable("EMAIL_PASSWORD", required=True)

    server = connect_to_email_server(IMAP_HOST, USERNAME, PASSWORD)
    fetch_and_process_emails(server)
    server.logout()

if __name__ == "__main__":
    main()