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
            SELECT * FROM users WHERE id = %s
            """)
        cursor.execute(get_all_query, (user_id,))

        rows = cursor.fetchall()

        user_info = [
            {"id": row[0], "role": row[1], "name": row[2], "grade": row[3], "sphere": row[4], "bio": row[5]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()


async def insert_all(user_id, role, name, grade, sphere, bio, nickname):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            insert into users (id, role, name, grade, sphere, bio, nickname) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
        cursor.execute(get_all_query, (user_id, role, name, grade, sphere, bio, nickname))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()

async def update_all(user_id, role, name, grade, sphere, bio):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            UPDATE users
            SET role = %s,
                name = %s,
                grade = %s,
                sphere = %s,
                bio = %s
            WHERE id = %s
            """)
        cursor.execute(get_all_query, (role, name, grade, sphere, bio, user_id))

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
            SELECT name, grade, sphere, bio FROM users WHERE role = %s and flag = true
            """)
        cursor.execute(get_all_teachers_query, ("teacher",))

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

