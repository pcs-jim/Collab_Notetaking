from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

"""



"""


# Get Google Drive authentication

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

drive_service = build('drive', 'v3', credentials=creds)

doc_service = build('docs', 'v1', credentials=creds)


parent_folder_name = "Collaborative Notes for Spring 2020"
section_folder_names = ['Section A', 'Section B', 'Section C']
group_folder_names = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']
doc_file_names = ['Week 1 & 2', 'Week 3', 'Week 4', 'Week 5']

d_header = """Scientific Writing, CC500
Group Notes for """
d_body = """

Greetings, students. This document is used for taking collaborative notes with your group members during the semester. Please write your notes for each video below the appropriate headings. Use as much space as needed.

Please use different colored text so that I can distinguish what you wrote.

Use the following colors:

Bob - Brown
Sam - Purple
Jenny - Green
Cindy - Blue
"""

def create_drive_folder(folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }

    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')


def create_drive_folder_in_parent(folder_name, parent_id):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id]
    }

    file = drive_service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')






















