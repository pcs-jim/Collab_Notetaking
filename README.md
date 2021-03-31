# Collaborative Notetaking Study

This study is conducted by Professor Mik Fanguy of KAIST university.

Collab_Notetaking is a custom system to download multiple Google Docs from various folders for the purpose of counting the number of words (volume; vol) and the number of turns (turn taking; trn) each contributor makes and stores the information in a local Sqlite database file. This system counts the number of words, for volume, and breaks in font colors while ignoring the black default font, for turn taking, in each of the designated font colors which is a representative of each contributor. The designation of each of the font colors are determined at the beginning of the document by contributors’ name in that font color. The black font (i.e. black default font) is designated to the professor and their teaching assistants.

## Creating Files and Folders

### Create Document Templates
1. Open Google Drive and create a folder with a unique name from all other folders that are currently on your Google Drive.

2. Within the newly created folder, create Google Doc(s) and name them appropriately.

### Run create_files_and_folders.py
1. Enter in the unique template folder's name into the 'Template Folder' search box.
2. Wait for the completion message.
3. Enter the name of the 'Root Folder' and press the 'Create Folder' just underneath.
4. Enter in the section names seperated by spaces. Individual names must not have spaces.
5. Enter in the class names seperated by spaces. Individual names must not have spaces.
6. Enter in the group names seperated by spaces. Individual names must not have spaces.

*(Recommended to use underscores instead of spaces.
