import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, request

# Replace these with your details
SPREADSHEET_ID = '1dzFr-m5fv3F_f4R9-LJ06w7sd7Tmkw8Oy9XJTLmJvmA'  # ID of your Google Sheet
SHEET_NAME = 'Sheet1'  # Name of the sheet within the spreadsheet
SERVICE_ACCOUNT_FILE = r'/path/to/spreedsheet-423616-72516d1ef538.json'  # Correct path to your service account key file
RAZORPAY_EVENT_NAME = 'payment.captured'  # Specific Razorpay event to listen for

app = Flask(__name__)

# Configure Google Sheets API connection
def get_google_sheets_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    http = credentials.authorize(Http())
    return build('sheets', 'v4', http=http)

# Function to update spreadsheet row
def update_spreadsheet_row(sheet_service, data, row_index):
    body = {
        'values': [
            [data.get('Internship Period'), data.get('Name'), data.get('Email'), data.get('Domain'), data.get('Phone No'), data.get('Gender'), data.get('Referred By')],
        ]
    }
    sheet_service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A{row_index}:G{row_index}',
        valueInputOption='RAW',
        body=body
    ).execute()

# Function to process Razorpay webhook data
def process_webhook(data):
    print("Webhook data received:", data)  # Debug print
    if data.get('event') == RAZORPAY_EVENT_NAME:  # Check for specific event
        try:
            print("Processing payment captured event...")  # Debug print
            payment_metadata = data['payload']['payment']['entity']['notes']  # Adjust based on Razorpay payload structure
            row_index = payment_metadata.get('row_index')  # Handle potential missing key
            update_data = {
                'Internship Period': payment_metadata.get('amount'),  # Handle potential missing key
                'Name': payment_metadata.get('name'),  # Handle potential missing key
                'Email': payment_metadata.get('email'),  # Handle potential missing key
                'Domain': payment_metadata.get('domain'),  # Handle potential missing key
                'Phone No': payment_metadata.get('phone_no'),  # Handle potential missing key
                'Gender': payment_metadata.get('gender'),  # Handle potential missing key
                'Referred By': payment_metadata.get('referred_by'),  # Handle potential missing key
            }
            print("Update data prepared:", update_data)  # Debug print
            sheet_service = get_google_sheets_service()
            update_spreadsheet_row(sheet_service, update_data, row_index)
            print(f"Successfully updated row {row_index} in spreadsheet.")
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
