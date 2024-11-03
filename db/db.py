import psycopg2
from psycopg2 import sql

import config
import teacher.model

db_config = {
    'dbname': config.DB_NAME,
    'user': config.DB_USER,
    'password': config.DB_PASSWORD,
    'host': config.DB_HOST,
    'port': config.DB_PORT,
}


def db_connection():
    return psycopg2.connect(**db_config)


def check_id(user_id: int) -> (teacher.model.Teacher, int):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        # Проверяем наличие пользователя с данным user_id
        check_query = sql.SQL("""SELECT EXISTS (SELECT 1 FROM users WHERE id = %s)        """)
        cursor.execute(check_query, user_id)
        exists = cursor.fetchone()[0]

        if exists:
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("""SELECT * FROM %s WHERE id = %s      """)
            cursor.execute(get_all_query, user_id)
            rows = cursor.fetchmany(size=4)
            user = teacher.model.Teacher
            if len(rows) == 1:
                user.id = rows[0][0]
                user.type = rows[0][1]
                user.name = rows[0][2]
                user.surname = rows[0][3]
                user.grade = rows[0][4]
                user.sphere = rows[0][5]
                user.description = rows[0][6]
            return user, 1
        else:
            user = teacher.model.Teacher
            user.id = user_id
            return user, 0

    except (Exception, psycopg2.DatabaseError) as error:
        return error, -1,
    finally:
        if connection:
            cursor.close()
            connection.close()


async def get_all(user_id: int, role: str):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""SELECT * FROM %s WHERE id = %s""")
        cursor.execute(get_all_query, (role, user_id))

        rows = cursor.fetchmany(size=4)

        user_info = [
            {"name": row[0], "last_name": row[1], "father_name": row[2], "profession": row[3]}
            for row in rows
        ]

        return user_info

    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if connection:
            cursor.close()
            connection.close()