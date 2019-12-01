"""
Created by: Jaemyong Chang
On: 11/29/2019

After initial setup of the folders and files,
this counts the words and the number of turns of the Google Doc
in each of the specified folders.



"""


import json
import os
import re

import httplib2
import nltk
import requests
from docx import Document
from collections import Counter
from googleapiclient import errors
from googleapiclient.discovery import build
from nltk.corpus import stopwords
from oauth2client.file import Storage
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from student_revisions import student_revisions
import collabo_db


def retrieve_revisions(service, file_id):
    """
        Retrieve a list of revisions.

        Args:
        service: Drive API service instance.
        file_id: ID of the file to retrieve revisions for.
        Returns:
        List of revisions.
    """
    try:

        revisions = service.revisions().list(fileId=file_id).execute()
        return revisions.get('items', [])
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
    return None

# Get permission via web browser.
gauth = GoogleAuth()
gauth.LoadCredentialsFile('my_creds.txt')

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile('my_creds.txt')

drive = GoogleDrive(gauth)

# Get authorization.
storage = Storage('my_creds.txt')

credentials = storage.get()

http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)
stop = stopwords.words('english')


'''
    Folder names and IDs:
    Notetaking PhD study Spring 2019 FOLDER_ID1
    Collaborative Notes FOLDER_ID2
    CC500 D FOLDER_ID3
    CC500 J FOLDER_ID4
    CC500 T FOLDER_ID5
    CC500 B FOLDER_ID6
    
    
    Look in folder:
    'Notetaking PhD study Spring 2019' -> 'Collaborative Notes'
'''

folder_id = 'ADD FOLDER ID HERE'  # Collaborative Notes ID

mimetypes = {
    # Microsoft Word Document.
    'application/vnd.google-apps.document': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',

}

download_mimetype = None

# Directory of current folder.
dir_path = os.path.dirname(os.path.realpath(__file__))

# Create a download folder.
if not os.path.exists(dir_path + '\googledrive\\'):
    os.makedirs(dir_path + '\googledrive\\')

current_semester_id = 1  # Database ID for 'Notetaking PhD study Spring 2019'
db_class_id = 0
db_group_id = 0
db_student_id = 0
db_notetaking_id = 0

db_week_number = ''

collaborative_notes_list = drive.ListFile({'q': "'%s' in parents" % folder_id}).GetList()
for class_list in collaborative_notes_list:
    # List of sub-folders in 'Collaborative Notes'
    # 'Class e.g. CC500 D, CC500 J, etc.'
    if class_list['mimeType'] == 'application/vnd.google-apps.folder':

        # print(class_list['title'], class_list['id'])

        # Check database if class exists in the database.
        course_name_result = collabo_db.check_course_name(current_semester_id, class_list['title'])
        if course_name_result != False:
            db_class_id = course_name_result
        else:
            db_class_id = collabo_db.create_course_name(current_semester_id, class_list['title'])

        # List of groups in a class e.g. Group 1, Group 2, Group 3, etc
        group_list = drive.ListFile({'q': "'%s' in parents" % class_list['id']}).GetList()
        for group_number in group_list:

            # print('   ', group_number['title'], group_number['id'])

            # Check if group exists in the database.
            # Check database if class exists in the database.
            group_name_result = collabo_db.check_class_group(db_class_id, group_number['title'])
            if group_name_result != False:
                db_group_id = group_name_result
            else:
                db_group_id = collabo_db.create_class_group(db_class_id, group_number['title'])

            # List of files in each of the groups.
            group_files = drive.ListFile({'q': "'%s' in parents" % group_number['id']}).GetList()
            for group_file in group_files:
                # List only Word Document type.
                if group_file['mimeType'] != 'application/vnd.google-apps.folder':

                    # print('      ', group_file['title'], group_file['id'])
                    if group_file['title'][:1] != 'G':
                        break

                    # TODO: Change this to further analyze. Currently analyzing up to week 9
                    try:
                        if int(group_file['title'][-2:]) > 9:
                            break
                        else:
                            db_week_number = str(int(group_file['title'][-2:]))
                    except:
                        break

                    # Get revisions and download as a Word Document file.
                    revisions = retrieve_revisions(drive_service, group_file['id'])
                    cred_file = open('my_creds.txt')
                    headers = json.loads(cred_file.read())

                    # Create a list of revisions.
                    doc_revision_list = {}

                    for revision in revisions:
                        # Add a revision to the dictionary.
                        doc_revision_list[revision['id']] = student_revisions(revision['id'])

                        switch1 = ''
                        switch2 = ''

                        # Download revision.
                        try:
                            r = requests.get(revision['exportLinks'].get('application/vnd.openxmlformats-officedocument.wordprocessingml.document', ''), headers)
                        except:
                            pass
                        # Open and move document.
                        with open(dir_path + '\googledrive\\' + revision['id'] + '.docx', 'wb') as file_to_save:
                            file_to_save.write(r.content)

                        doc = Document(dir_path + '\googledrive\\' + revision['id'] + '.docx')

                        # Look at each paragraph in document.
                        for paragraph in doc.paragraphs:
                            for run in paragraph.runs:
                                # If run is a color, then it is a student.
                                if run.font.color.rgb is not None:
                                    switch1 = run.font.color.rgb

                                student_exist = False

                                # Check to see if the student exists.
                                if len(doc_revision_list[revision['id']].student_list) > 0:
                                    for student in doc_revision_list[revision['id']].student_list:
                                        if student.student_color == str(run.font.color.rgb):
                                            student_exist = True

                                # If not, create a student object.
                                if student_exist:
                                    pass
                                else:
                                    try:
                                        if run.font.color.rgb is not None:
                                            doc_revision_list[revision['id']].add_student(run.text[0:(str(run.text).index('-'))].strip(), str(run.font.color.rgb))
                                    except:
                                        pass

                                # Check the run. Add run to corresponding student.
                                if run.font.color.rgb is not None and student_exist:
                                    # This adds a turn for a student.
                                    if switch1 != switch2:
                                        for student in doc_revision_list[revision['id']].student_list:
                                            if student.student_color == str(run.font.color.rgb):
                                                student.number_of_turns += 1

                                    # Count the number of characters
                                    # Add word list for a student.
                                    tokenized_words = nltk.word_tokenize(re.sub(r'[^\w\s]', '', str(run.text)))
                                    for student in doc_revision_list[revision['id']].student_list:
                                        if student.student_color == str(run.font.color.rgb):
                                            student.number_of_characters += len(str(run.text))
                                            student.word_list.extend(tokenized_words)

                                if run.font.color.rgb is not None:
                                    switch2 = run.font.color.rgb

                        # Remove docx from local hard drive.
                        os.remove(dir_path + '\googledrive\\' + revision['id'] + '.docx')

                    revision_list_length = len(doc_revision_list)
                    print('Class:', class_list['title'], 'Group:', group_number['title'], 'Document:', group_file['title'])
                    for item in doc_revision_list:
                        # print('   Revision ID: ', item, 'Index', revision_list_length)

                        revision_previous = doc_revision_list[item].student_list
                        if revision_list_length == 1:
                            for stu in doc_revision_list[item].student_list:

                                # Check if student exists in the database. If not create a new student.
                                student_result = collabo_db.check_student(db_group_id, stu.student_name)
                                if student_result != False:
                                    db_student_id = student_result
                                else:
                                    db_student_id = collabo_db.create_student(db_group_id, '', stu.student_name)

                                # TODO: Check if statistic is already entered.
                                '''
                                    If the statistic exists update the information.
                                '''
                                # Add in statistic for each student.
                                db_notetaking_id = collabo_db.create_note_taking(
                                    db_student_id,
                                    stu.student_name,
                                    stu.student_color,
                                    db_week_number,
                                    group_file['title'],
                                    0,
                                    len(stu.word_list),
                                    0,
                                    stu.number_of_turns,
                                    0,
                                    0
                                )

                                print('Result of entry', db_notetaking_id, stu.student_name, stu.number_of_turns, len(stu.word_list), stu.number_of_characters)

                            print('')

                        revision_list_length -= 1








