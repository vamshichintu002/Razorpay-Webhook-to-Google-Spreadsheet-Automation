import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request
import os
from datetime import datetime

# Replace these with your details
SPREADSHEET_ID = '1dzFr-m5fv3F_f4R9-LJ06w7sd7Tmkw8Oy9XJTLmJvmA'  # ID of your Google Sheet
SHEET_NAME = 'Sheet1'  # Name of the sheet within the spreadsheet
SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'spreedsheet-423616-7b116f800da5.json')  # Correct path to your service account key file
RAZORPAY_EVENT_NAME = 'payment.captured'  # Specific Razorpay event to listen for

app = Flask(__name__)

# Configure Google Sheets API connection
def get_google_sheets_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    http = credentials.authorize(Http())
    return build('sheets', 'v4', http=http)

# Function to append data to the next available row in the spreadsheet
def append_to_next_available_row(sheet_service, data):
    # Find the next available row index
    response = sheet_service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A:G',  # Assuming your data is in columns A to G
    ).execute()
    values = response.get('values', [])
    next_row_index = len(values) + 1  # Index of the next available row

    # Get the current timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Prepare the data to append
    row_data = [
        timestamp,  # Add the timestamp as the first column
        data.get('Amount'),
        data.get('Name'),
        data.get('Email'),
        data.get('Domain'),
        data.get('Phone No'),
        data.get('Referred By')
    ]

    # Append the data to the next available row
    body = {
        'values': [row_data]
    }
    sheet_service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A{next_row_index}:H{next_row_index}',  # Adjusted to column H to include the timestamp
        valueInputOption='RAW',
        body=body
    ).execute()

# Function to process Razorpay webhook data
def process_webhook(data):
    print("Webhook data received:", data)  # Debug print
    if data.get('event') == payment.capture:  # Check for specific event
        try:
            print("Processing payment captured event...")  # Debug print
            payment_metadata = data['payload']['payment']['entity']['notes']  # Adjust based on Razorpay payload structure
            update_data = {
                'Amount': payment_metadata.get('amount'),
                'Name': payment_metadata.get('name'),
                'Email': payment_metadata.get('email'),
                'Domain': payment_metadata.get('choose_internship'),
                'Phone No': payment_metadata.get('phone'),
                'Referred By': payment_metadata.get('referred_by'),
            }
            print("Update data prepared:", update_data)  # Debug print
            sheet_service = get_google_sheets_service()
            append_to_next_available_row(sheet_service, update_data)
            print("Successfully appended data to the next available row in the spreadsheet.")
        except KeyError as e:
            print(f"Missing expected data in payload: {e}")
        except Exception as e:
            print(f"Error updating spreadsheet: {e}")
    else:
        print(f"Unexpected event type: {data.get('event')}")

# Handle incoming webhook data
@app.route('/', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            process_webhook(data)
        except Exception as e:
            print(f"Error processing webhook: {e}")
    else:
        print("Invalid request method")
    return 'Webhook received'

if __name__ == '__main__':
    app.run(debug=True)
