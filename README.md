# Razorpay Webhook to Google Spreadsheet Automation

## Overview

This project automates the process of updating a Google Spreadsheet with payment details from Razorpay via webhooks and sending automated emails to the customers. It listens to the Razorpay webhook, captures the relevant information, updates it in the specified Google Spreadsheet, and sends an email based on a predefined template. This project is deployed on [Railway.app](https://railway.app) for seamless automation.

### Features:
- Automatically captures Razorpay payment details via webhooks.
- Updates the payment details (like amount, name, email, etc.) into a Google Spreadsheet.
- Sends an automated email to the customer when a payment is received.

## How It Works

1. Razorpay sends a webhook when a payment is captured.
2. The Flask-based app listens for the webhook, processes the payload, and extracts relevant information (amount, name, email, etc.).
3. This information is appended to the next available row in a Google Spreadsheet.
4. Another script (within the Google Spreadsheet) automatically sends an email to the customer based on the email template when their details are added to the spreadsheet.

### Google Spreadsheet Structure:
The following fields are captured and updated:
- Timestamp (when the payment was captured)
- Amount
- Customer Name
- Email Address
- Domain (from Razorpay form)
- Phone Number
- Referred By
- Current Year (from Razorpay form)
- College Name

## Prerequisites

- A Razorpay account with webhook functionality.
- A Google Spreadsheet.
- A service account key for Google Sheets API.
- Python 3.7 or higher.

### API and Libraries:
- **Flask** for setting up the webhook server.
- **Google Sheets API** for updating the spreadsheet.
- **pytz** for handling timezone data.
- **Razorpay Webhooks** for capturing payment information.

## Setup

1. Clone the repository.
2. Install the required dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a service account in Google Cloud and download the JSON credentials file.
4. Set the correct path to your Google Sheets service account credentials in the code:
   ```python
   SERVICE_ACCOUNT_FILE = 'path_to_your_json_file.json'
   ```
5. Update the Google Spreadsheet ID and Sheet name in the code:
   ```python
   SPREADSHEET_ID = 'your_spreadsheet_id'
   SHEET_NAME = 'Sheet1'
   ```
6. Deploy the app on [Railway.app](https://railway.app).

## Running Locally

1. Start the Flask server:
   ```bash
   python app.py
   ```
2. Set up a tunnel (e.g., using Ngrok) to expose the local server to the internet and connect it with Razorpay webhook.

## Webhook Handling

- The app listens for the `payment.captured` event from Razorpay.
- Once a payment is captured, the app processes the webhook data and appends the relevant details to the Google Spreadsheet.

## Automatic Email Script

- Another script runs on Google Sheets that triggers an email to the customer when a new row is added. Ensure the script is set to trigger automatically for each row update.

## Deployment

The project is deployed on [Railway.app](https://railway.app) for automated and scalable webhook handling and Google Sheets integration.

## Requirements

- Python 3.7 or higher
- `requirements.txt` includes:
   ```text
   flask==1.1.4 
   werkzeug==1.0.1
   gunicorn==20.1.0
   google-api-python-client==2.34.0
   httplib2==0.20.2
   oauth2client==4.1.3
   jinja2==2.11.3 
   markupsafe==1.1.1
   pytz==2024.1
   ```

## License

This project is licensed under the MIT License.

---
