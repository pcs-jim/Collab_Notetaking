from __future__ import print_function
import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.file import Storage
import httplib2

"""
Created by: Jim Chang
On: 10/4/2019

The purpose of this is to set up the initial folders and files for a collaborative notetaking study
under the guidance of Professor Mik Fanguy of KAIST university of Daejeon, South Korea.

You'll need to download the 'credentials.json' from your Google account.
"""


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


# Create parent folder
parent_folder_id = create_drive_folder(parent_folder_name)

# Create section folders
for section_names in section_folder_names:
    section_id = create_drive_folder_in_parent(section_names, parent_folder_id)

    # Create group folders
    for group_names in group_folder_names:
        group_folder_id = create_drive_folder_in_parent(group_names, section_id)

        # Create Google Document.
        for doc_file_name in doc_file_names:

            file_metadata = {
                'name': doc_file_name,
                'mimeType': 'application/vnd.google-apps.document',
                'parents': [group_folder_id]
            }
            file = drive_service.files().create(body=file_metadata, fields='id').execute()
            doc_id = file.get('id')

            # TODO: Give permission to each document.

            bold_long_header = 0
            if len(doc_file_name) > 6:
                bold_long_header = 4
            else:
                bold_long_header = 0

            requests = [
                {
                    'insertText': {
                        'text': d_header + doc_file_name + d_body,
                        'location': {
                            'index': 1,
                        }
                    }

                }
            ]

            result = doc_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': requests}).execute()

            # Header
            update_requests = [
                {
                    'updateTextStyle': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': 50 + bold_long_header
                        },
                        'textStyle': {
                            'bold': True,
                            'fontSize': {
                                'magnitude': 18,
                                'unit': 'PT'
                            }
                        },
                        'fields': 'bold, fontSize'
                    }

                }
            ]

            update_result = doc_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': update_requests}).execute()

            # Change the font colors of the example students.
            update_requests = [
                {
                    'updateTextStyle': {
                        'range': {
                            'startIndex': 400 + bold_long_header,
                            'endIndex': 414 + bold_long_header
                        },
                        'textStyle': {
                            'foregroundColor': {
                                'color': {
                                    'rgbColor': {
                                        'blue': 0.0,
                                        'green': 1.0,
                                        'red': 0.0
                                    }
                                }
                            }
                        },
                        'fields': 'foregroundColor'
                    }

                }
            ]

            update_result = doc_service.documents().batchUpdate(
                documentId=doc_id, body={'requests': update_requests}).execute()











