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
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            SELECT * FROM student WHERE id = %s
            """)
        cursor.execute(get_all_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"id": row[0], "name": row[1], "grade": row[2], "sphere": row[3], "bio": row[4]}
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


async def get_all_teachers():
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_teachers_query = sql.SQL("""
            SELECT name, grade, sphere, description FROM teacher WHERE show = true
            """)
        cursor.execute(get_all_teachers_query)

        rows = cursor.fetchall()

        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3]}
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


async def get_filter_teachers(grade, sphere):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        fteachers_query = sql.SQL("""
        SELECT name, grade, sphere, description FROM teacher 
        WHERE 
        grade similar to %s and
        sphere similar to %s and 
        show = true
        """)

        if not grade and sphere:
            cursor.execute(fteachers_query, ("%("+"|".join(all_grades)+")%", "%("+"|".join(sphere.split(", "))+")%"))
        elif not sphere and grade:
            cursor.execute(fteachers_query, ("%("+"|".join(grade.split(", "))+")%", "%("+"|".join(all_spheres)+")%"))
        elif not grade and not sphere:
            cursor.execute(fteachers_query, ("%("+"|".join(all_grades)+")%", "%("+"|".join(all_spheres)+")%"))
        else:
            cursor.execute(fteachers_query, ("%("+"|".join(grade.split(", "))+")%", "%("+"|".join(sphere.split(", "))+")%"))
        # print(("%("+"|".join(grade.split(","))+")%", "%("+"|".join(sphere.split(","))+")%"))
        rows = cursor.fetchmany(size=4)
        user_info = [
            {"name": row[0], "grade": row[1], "sphere": row[2], "bio": row[3]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error

    finally:
        if connection:
            cursor.close()
            connection.close()

# print(get_filter_teachers("Senior, Junior", "CV, NLP"))