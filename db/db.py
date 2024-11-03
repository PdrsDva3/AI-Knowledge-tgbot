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
    print(user_id)
    print(1)
    connection = db_connection()
    print(2)
    cursor = connection.cursor()
    print(3)

    try:
        print(4)
        # Проверяем наличие пользователя с данным user_id
        check_query = sql.SQL("SELECT EXISTS (SELECT 1 FROM users WHERE id = %s)")
        cursor.execute(check_query, (user_id,))

        print(6)
        exists = cursor.fetchone()[0]
        print(7)

        if exists:
            print(8)
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("SELECT * FROM users WHERE id = %s")
            print(9)
            cursor.execute(get_all_query, (user_id,))
            print(10)
            rows = cursor.fetchone()
            print(11)
            user = teacher.model.Teacher(
                id=rows[0],
                type=rows[1],
                name=rows[2],
                surname=rows[3],
                grade=rows[4],
                sphere=rows[5],
                description=rows[6],
            )
            # if len(rows) == 1:
            #     user.id = rows[0][0]
            #     user.type = rows[0][1]
            #     user.name = rows[0][2]
            #     user.surname = rows[0][3]
            #     user.grade = rows[0][4]
            #     user.sphere = rows[0][5]
            #     user.description = rows[0][6]
            print(1)
            return user, 1
        else:
            print(0)
            user = teacher.model.Teacher
            user.id = user_id
            return user, 0

    except (Exception, psycopg2.DatabaseError) as error:
        print(-1)
        return error, -1,
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_user(usr: teacher.model.Teacher):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        user, i = check_id(usr.id)

        if i == 1:  # Пользователь уже существует
            # Обновляем данные пользователя
            update_query = sql.SQL("""
                UPDATE users 
                SET type = %s, name = %s, surname = %s, grade = %s, sphere = %s, description = %s
                WHERE id = %s
            """)
            cursor.execute(update_query, (
                usr.type,
                usr.name,
                usr.surname,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.id,
            ))
            cursor.connection.commit()
            affected_rows = cursor.rowcount
            print(f"Изменено {affected_rows} строк")

            print(f"Пользователь с ID {usr.id} обновлен")

        elif i == 0:  # Пользователь новый
            # Добавляем нового пользователя
            insert_query = sql.SQL("""
                INSERT INTO users (id, type, name, surname, grade, sphere, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (
                user.id,
                user.type,
                user.name,
                user.surname,
                user.grade,
                user.sphere,
                user.description
            ))

            print(f"Новый пользователь с ID {user.id} добавлен")

        else:  # Произошла ошибка при проверке ID
            print(f"Ошибка при проверке ID: {i}")
            return False

        connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Произошла ошибка при добавлении/обновлении пользователя: {error}")
        return False

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
