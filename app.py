import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

# Replace these with your details
SPREADSHEET_ID = '1dzFr-m5fv3F_f4R9-LJ06w7sd7Tmkw8Oy9XJTLmJvmA'  # ID of your Google Sheet
SHEET_NAME = 'Sheet1'  # Name of the sheet within the spreadsheet
SERVICE_ACCOUNT_FILE = '/spreedsheet-423616-72516d1ef538.json'  # Path to your service account key file
RAZORPAY_EVENT_NAME = 'payment.captured'  # Specific Razorpay event to listen for

# Configure Google Sheets API connection
def get_google_sheets_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
    http = credentials.authorize(Http())
    return build('sheets', 'v4', http=http)

# Function to update spreadsheet row
def update_spreadsheet_row(sheet_service, data, row_index):
    body = {
        'values': [
            [data['Internship Period'], data['Name'], data['Email'], data['Domain'], data['Phone No'], data['Gender'], data['Referred By']],
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
    if data['event'] == RAZORPAY_EVENT_NAME:  # Check for specific event
        # Extract relevant data from webhook payload (adjust based on your Razorpay data format)
        row_index = data['payment']['metadata'].get('row_index')  # Handle potential missing key
        update_data = {
            'Internship Period': data['payment']['metadata'].get('amount'),  # Handle potential missing key
            'Name': data['payment']['metadata'].get('Notes Name'),  # Handle potential missing key
            'Email': data['payment']['metadata'].get('email'),  # Handle potential missing key
            'Domain': data['payment']['metadata'].get('Notes Choose Internship'),  # Handle potential missing key
            'Phone No': data['payment']['metadata'].get('Notes Phone'),  # Handle potential missing key
            'Referred By': data['payment']['metadata'].get('Notes Referred by'),  # Handle potential missing key
        }
        sheet_service = get_google_sheets_service()
        update_spreadsheet_row(sheet_service, update_data, row_index)
        print(f"Successfully updated row {row_index} in spreadsheet.")

# Handle incoming webhook data
def handle_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.get_data())
            process_webhook(data)
        except Exception as e:
            print(f"Error processing webhook: {e}")
    else:
        print("Invalid request method")

# Example usage (replace with your server logic)
if __name__ == '__main__':
    from flask import Flask, request

    app = Flask(__name__)
    app.route('/', methods=['POST'])
    def webhook():
        handle_webhook(request)
        return 'Webhook received'

    app.run(debug=True)
