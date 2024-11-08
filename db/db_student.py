"""
Обращения к БД для 'студента'
"""
import psycopg2
from psycopg2 import sql

import config

db_config = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'port': config.DB_PORT,
}


def db_connection():
    return psycopg2.connect(**db_config)


async def get_all(user_id: int):
    """
    :param user_id:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            SELECT * FROM student WHERE id = %s
            """)
        cursor.execute(get_all_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "bio": row[4], "show": row[5],
             "nickname": row[6]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def insert_all(user_id, name, grade, sphere, bio, nickname):
    """
    :param user_id:
    :param name:
    :param grade:
    :param sphere:
    :param bio:
    :param nickname:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            insert into student (id, name, grade, sphere, description, nickname) VALUES (%s, %s, %s, %s, %s, %s)
            """)
        cursor.execute(get_all_query, (user_id, name, grade, sphere, bio, nickname))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def update_all(user_id, name, grade, sphere, bio):
    """
    :param user_id:
    :param name:
    :param grade:
    :param sphere:
    :param bio:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            UPDATE student
            SET name = %s,
                grade = %s,
                sphere = %s,
                description = %s
            WHERE id = %s
            """)
        cursor.execute(get_all_query, (name, grade, sphere, bio, user_id))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_all_teachers(id_student: int):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_teachers_query = sql.SQL("""
            SELECT name, grade, sphere, description, id 
            FROM teacher 
            WHERE show = true
            and id != %s
            and NOT EXISTS (
                SELECT 1 
                FROM teacher_student 
                WHERE teacher.id = teacher_student.id_teacher
                AND teacher_student.id_student = %s
                AND teacher_student.id_student != teacher_student.id_teacher
            )""")
        cursor.execute(get_all_teachers_query, (id_student, id_student,))

        rows = cursor.fetchall()

        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "id": row[4]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


all_grades = ["No_work", "Intern", "Junior", "Middle", "Senior"]
all_spheres = ["NLP", "CV", "RecSys", "Audio", "Classic_ML", "Any"]


async def get_filter_teachers(grade, sphere, id_student):
    """
    :param grade:
    :param sphere:
    :param id_student:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        fteachers_query = sql.SQL("""
        SELECT name, grade, sphere, description, id FROM teacher 
        WHERE 
        grade similar to %s and
        sphere similar to %s and 
        show = true
        and id != %s
        AND NOT EXISTS (
                SELECT 1 
                FROM teacher_student 
                WHERE teacher.id = teacher_student.id_teacher
                AND teacher_student.id_student = %s
                AND teacher_student.id_student != teacher_student.id_teacher
        )""")

        if not grade and sphere:
            cursor.execute(fteachers_query,
                           ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%", id_student,
                            id_student))
        elif not sphere and grade:
            cursor.execute(fteachers_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(all_spheres) + ")%", id_student,
                            id_student))
        elif not grade and not sphere:
            cursor.execute(fteachers_query,
                           ("%(" + "|".join(all_grades) + ")%", "%(" + "|".join(all_spheres) + ")%", id_student,
                            id_student))
        else:
            cursor.execute(fteachers_query,
                           ("%(" + "|".join(grade.split(", ")) + ")%", "%(" + "|".join(sphere.split(", ")) + ")%",
                            id_student, id_student))
        rows = cursor.fetchall()
        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "id": row[4]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_teacher_by_id(user_id):
    """
    :param user_id:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_teachers_query = sql.SQL("""
            SELECT name, grade, sphere, description, nickname FROM teacher WHERE id = %s
            """)
        cursor.execute(get_all_teachers_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3], "nickname": row[4]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def insert_into_ts(id_teacher, id_student, nick_teacher, nick_student):
    """
    :param id_teacher:
    :param id_student:
    :param nick_teacher:
    :param nick_student:
    """
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_teachers_query = sql.SQL("""
            INSERT INTO teacher_student (id_teacher, id_student, nick_teacher, nick_student)
            values (%s, %s, %s, %s)
            """)
        cursor.execute(get_all_teachers_query, (id_teacher, id_student, nick_teacher, nick_student))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_teacher_list(id_student: int):
    """
    :param id_student:
    :return:
    """
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_student_query = sql.SQL("""SELECT name, grade, sphere, description, nickname
FROM teacher 
WHERE EXISTS (
    SELECT 1 
    FROM teacher_student 
    WHERE teacher.id = teacher_student.id_teacher
    and teacher_student.id_student = %s
    AND teacher_student.id_student != teacher_student.id_teacher
)""")
        cursor.execute(get_all_student_query, (id_student,))

        rows = cursor.fetchall()
        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "description": row[3], "nickname": "@" + row[4]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def change_show_student(user_id: int, show: bool):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        update_query = sql.SQL("""
                UPDATE student 
                SET show = %s
                WHERE id = %s
            """)
        cursor.execute(update_query, (
            show, user_id
        ))
        cursor.connection.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()
