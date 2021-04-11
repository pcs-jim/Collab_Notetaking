import os
import sqlite3
from sqlite3 import Error


database = os.path.dirname(os.path.realpath(__file__)) + '\collabo.db'


def create_connection(db_file):
    """
    Create a database connection
    :param db_file:
    :return:
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_table(conn, create_table_sql):
    '''
    Create database table.
    :param conn:
    :param create_table_sql:
    :return:
    '''

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_semester(semester_name):
    """
    Creates a new semester entry.
    :param semester_name:
    :return:
    """

    sql = ''' INSERT INTO semesters(semester_name) VALUES(?) '''
    sql_values = (semester_name, )

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    conn.commit()
    return cur.lastrowid


def select_semesters():
    """
    Geta all of the available semesters.
    :return:
    """

    sql = 'SELECT * FROM semesters'
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def create_course_name(semester_id, course_name):
    """
    Creates a new course name entry.
    :param semester_id:
    :param course_name:
    :return:
    """

    sql = ''' INSERT INTO course_names(semester_id, course_name) VALUES(?, ?) '''
    sql_values = (semester_id, course_name, )

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    conn.commit()
    return cur.lastrowid


def check_course_name(semester_id, course_name):
    """
    Check if a course exists within each semester.
    e.g. CC500 D, CC500 J, etc.
    :param semester_id:
    :param course_name:
    :return True or False:
    """
    sql = 'SELECT * FROM course_names WHERE semester_id=? AND course_name=?'
    sql_values = (semester_id, course_name,)
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    rows = cur.fetchall()

    if len(rows) == 1:
        return rows[0]['id']
    elif len(rows) > 1:
        return 'Error in statement'
    else:
        return False


def select_course_names():
    """
    Geta all of the available course names.
    :return:
    """

    sql = 'SELECT * FROM course_names'
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def create_class_group(course_name_id, class_group_name):
    """
    Creates a new group entry.
    :param course_name_id:
    :param group_name:
    :return:
    """

    sql = ''' INSERT INTO class_groups(course_name_id, class_group_name) VALUES(?, ?) '''
    sql_values = (course_name_id, class_group_name, )

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    conn.commit()
    return cur.lastrowid


def check_class_group(course_name_id, class_group_name):
    """
    Checks to see if a class group exists.
    e.g. Group 1, Group 2, etc.
    :param course_name_id:
    :param class_group_name:
    :return:
    """
    sql = 'SELECT * FROM class_groups WHERE course_name_id=? AND class_group_name=?'
    sql_values = (course_name_id, class_group_name,)
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    rows = cur.fetchall()

    if len(rows) == 1:
        return rows[0]['id']
    elif len(rows) > 1:
        return 'Error in statement'
    else:
        return False


def create_student(class_group_id, school_student_id, KLMS_name):
    """
    Create a new student entry.
    :param class_group_id:
    :param school_student_id:
    :param KLMS_name:
    :return:
    """
    sql = ''' INSERT INTO students(class_group_id, school_student_id, KLMS_name) VALUES(?, ?, ?) '''
    sql_values = (class_group_id, school_student_id, KLMS_name, )

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    conn.commit()
    return cur.lastrowid


def check_student(class_group_id, KLMS_name):
    """
    Checks if the student already exists in the database.
    :param class_group_id:
    :param school_student_id:
    :param KLMS_name:
    :return:
    """
    sql = 'SELECT * FROM students WHERE class_group_id=? AND KLMS_name=?'
    sql_values = (class_group_id, KLMS_name,)
    conn = create_connection(database)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    rows = cur.fetchall()

    if len(rows) == 1:
        return rows[0]['id']
    elif len(rows) > 1:
        return 'Error in statement'
    else:
        return False


def create_note_taking(
        student_id,
        note_taking_name,
        note_taking_color,
        week_number,
        google_doc_name,
        oth_edit_i,
        vol_i,
        stg_i,
        trn_i,
        cmt_i,
        evn_1):

    sql = ''' INSERT INTO note_taking(
        student_id, 
        note_taking_name, 
        note_taking_color, 
        week_number, 
        google_doc_name, 
        oth_edit_i,
        vol_i,
        stg_i,
        trn_i,
        cmt_i,
        evn_1
      ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''

    sql_values = (
        student_id,
        note_taking_name,
        note_taking_color,
        week_number,
        google_doc_name,
        oth_edit_i,
        vol_i,
        stg_i,
        trn_i,
        cmt_i,
        evn_1,
    )

    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql, sql_values)
    conn.commit()
    return cur.lastrowid


def main():
    sql_create_semesters_table = """ CREATE TABLE IF NOT EXISTS semesters (
      id integer PRIMARY KEY,
      semester_name text NOT NULL
      );"""
    sql_create_coursename_table = """ CREATE TABLE IF NOT EXISTS course_names (
      id integer PRIMARY KEY,
      semester_id integer NOT NULL,
      course_name text NOT NULL,
      FOREIGN KEY (semester_id) REFERENCES semesters (id)
      );"""
    sql_create_classgroups_table = """ CREATE TABLE IF NOT EXISTS class_groups (
      id integer PRIMARY KEY,
      course_name_id integer NOT NULL,
      class_group_name text NOT NULL,
      FOREIGN KEY (course_name_id) REFERENCES course_names (id)
      );"""
    sql_create_students_table = """ CREATE TABLE IF NOT EXISTS students (
      id integer PRIMARY KEY,
      class_group_id integer NOT NULL,
      school_student_id text,
      KLMS_name text,
      FOREIGN KEY (class_group_id) REFERENCES class_groups (id)
      );"""
    sql_create_notetaking_table = """ CREATE TABLE IF NOT EXISTS note_taking (
      id integer PRIMARY KEY,
      student_id integer NOT NULL,
      note_taking_name text,
      note_taking_color text,
      week_number text NOT NULL,
      google_doc_name text NOT NULL,
      oth_edit_i integer,
      vol_i integer,
      stg_i integer,
      trn_i integer,
      cmt_i integer,
      evn_1 float,      
      FOREIGN KEY (student_id) REFERENCES students (id)
      );"""

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_semesters_table)
        create_table(conn, sql_create_coursename_table)
        create_table(conn, sql_create_classgroups_table)
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_notetaking_table)

    else:
        print('Error! Cannot create the database connection.')


if __name__ == '__main__':
    main()

















