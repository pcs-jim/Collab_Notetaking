class student_revisions:

    def __init__(self, revision_id):
        self.revision_id = revision_id
        self.student_list = []

    def add_student(self, student_name, student_color):
        stu = Student(student_name, student_color)
        self.student_list.append(stu)


class Student:

    def __init__(self, student_name, student_color):
        self.student_name = student_name
        self.student_color = student_color
        self.number_of_turns = 1
        self.number_of_characters = 0
        self.word_list = []

        self.total_char_edits = 0
        self.total_word_edits = 0

