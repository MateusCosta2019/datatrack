import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
import os
import pickle

def get_data_from_google_sheets(SAMPLE_SPREADSHEET_ID_input, SAMPLE_RANGE_NAME):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    global values_input, service
    creds = None
    if os.path.exists('tokeOAutho.pickle'):
        with open('tokeOAutho.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("application/token.json", SCOPES) # here enter the name of your downloaded JSON file
            creds = flow.run_local_server(port=8080)
        with open('tokeOAutho.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result_input = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID_input,
                                range=SAMPLE_RANGE_NAME).execute()
    values_input = result_input.get('values', [])

    return values_input

# get_data_from_google_sheets(SAMPLE_SPREADSHEET_ID_input='12CmUYRkE25oNLItluFRkFDG_OyrcKARdBHOlTuKce7U', 
# SAMPLE_RANGE_NAME='1:1003')