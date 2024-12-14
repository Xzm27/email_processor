# Email Processor Script

This script connects to an email server using IMAP, fetches unread emails, and processes them by saving details such as the sender, subject, and timestamp into a SQLite database. It uses environment variables for sensitive information and logs activities for debugging and monitoring.

## Features

- Connects to an IMAP server (Gmail or other).
- Fetches and processes unread emails.
- Decodes the sender and subject from the email headers.
- Saves the email details (sender, subject, timestamp) to an SQLite database.
- Logs the processing activities for monitoring purposes.
- Flags processed emails as "read" (marked as seen) on the server.

## Requirements

- Python 3.12
- Libraries:
  - `imaplib` (Standard library)
  - `email` (Standard library)
  - `sqlite3` (Standard library)
  - `logging` (Standard library)
  - `python-dotenv` (for loading environment variables from a `.env` file)

You can install the required external libraries by running:

```bash
pip install -r requirements.txt
```

## Setup

1. Clone the repository
```bash
git clone https://github.com/Xzm27/email_processor.git
cd email-processor
```

2. Create a `.env` file.

Environment variables can be found in `.env.example`
Replace `your-imap-server.com`, `your-email@example.com`, and `your-email-password` with your actual email server and credentials.

3. Run script
To run the script, execute the following command:
```
python email_retrieval_service.py
```
This will start the email processing, and unread emails will be fetched, processed, and logged.

## Logging
All logs are saved in `email_processor.log`. It includes details about the email processing status and any errors encountered.

## Notes
- The script assumes the email server supports IMAP (such as Gmail, Outlook, etc.).
- Ensure that you have enabled IMAP access in your email account settings.
- The `.env` file is used to load sensitive information and should not be shared publicly.


