import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Requirements should suffice on a remote server
SCOPES = ["https://www.googleapis.com/auth/drive"]


def back_up():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    try:
        service = build('drive', 'v3', credentials=creds)

        response = service.files().list(
            q="name='MagicChillBackUp' and mimeType='application/vnd.google-apps.folder'",
            spaces='drive'
        ).execute()

        if not response['files']:
            file_metadata = {
                'name': "MagicChillBackUp",
                'mimeType': 'application/vnd.google-apps.folder'
            }

            file = service.files().create(body=file_metadata, fields='id').execute()
            folder_id = file.get('id')

        else:
            folder_id = response['files'][0]['id']

        for file in os.listdir('to_backup'):
            file_metadata = {
                'name': file,
                'parents': [folder_id]
            }

            media = MediaFileUpload(f"to_backup/{file}")

            upload_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f'Backed up file: {str(file)}')


    except HttpError as e:
        print(f"Error: {str(e)}")



def get_items():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=20, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    # back_up()
    get_items()