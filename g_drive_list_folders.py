from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.file import Storage
import httplib2


# Get Google Drive authentication
storage = Storage('my_creds.txt')
credentials = storage.get()

http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v3', http=http)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

creds = None

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

doc_service = build('docs', 'v1', credentials=creds)

# Name of the folder to stop at.
folder_name = 'Collaborative Notes for Spring 2020'

page_token = None
while True:
    response = drive_service.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        if folder_name == file.get('name'):
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            print(file)
    page_token = response.get('nextPageToken', None)
    if page_token is None:
        break









