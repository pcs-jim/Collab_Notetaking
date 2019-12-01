# Collaborative Notetaking Study

This study is conducted by Professor Mik Fanguy of KAIST university.

Collab_Notetaking is a custom system to download multiple Google Docs from various folders for the purpose of counting the number of words (volume; vol) and the number of turns (turn taking; trn) each contributor makes and stores the information in a local Sqlite database file. This system counts the number of words, for volume, and breaks in font colors while ignoring the black default font, for turn taking, in each of the designated font colors which is a representative of each contributor. The designation of each of the font colors are determined at the beginning of the document by contributors’ name in that font color. The black font (i.e. black default font) is designated to the professor and their teaching assistants.
