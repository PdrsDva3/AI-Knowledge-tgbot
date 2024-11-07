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
        check_query = sql.SQL("SELECT EXISTS (SELECT 1 FROM teacher WHERE id = %s)")
        cursor.execute(check_query, (user_id,))
        exists = cursor.fetchone()[0]
        TMP = sql.SQL("SELECT * from teacher WHERE id = %s")
        cursor.execute(TMP, (user_id,))
        if exists:
            # Если пользователь существует, извлекаем информацию
            get_all_query = sql.SQL("SELECT * FROM teacher WHERE id = %s")
            cursor.execute(get_all_query, (user_id,))
            rows = cursor.fetchone()
            user = teacher.model.Teacher(
                id=rows[0],
                name=rows[1],
                grade=rows[2],
                sphere=rows[3],
                description=rows[4],
                show=rows[5]
            )
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


def add_user(usr: teacher.model.Teacher):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        user, i = check_id(usr.id)


        if i == 1:  # Пользователь уже существует
            # Обновляем данные пользователя
            update_query = sql.SQL("""
                UPDATE teacher 
                SET  name = %s, grade = %s, sphere = %s, description = %s, show = %s
                WHERE id = %s
            """)
            cursor.execute(update_query, (
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.show,
                usr.id,
            ))
            cursor.connection.commit()
        elif i == 0:  # Пользователь новый
            # Добавляем нового пользователя
            insert_query = sql.SQL("""
                INSERT INTO teacher (id, name, grade, sphere, description, show)
                VALUES (%s, %s, %s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (
                usr.id,
                usr.name,
                usr.grade,
                usr.sphere,
                usr.description,
                usr.show
            ))

        else:  # Произошла ошибка при проверке ID
            return False

        connection.commit()
        return True

    except (Exception, psycopg2.DatabaseError) as error:
        return False

    finally:
        if connection:
            cursor.close()
            connection.close()


def change_show(user_id: int, show: bool):
    connection = db_connection()
    cursor = connection.cursor()
    try:
        update_query = sql.SQL("""
                UPDATE teacher 
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


async def get_all(user_id: int, role: str):
    connection = db_connection()
    cursor = connection.cursor()

    try:
        get_all_query = sql.SQL("""
            SELECT * FROM %s WHERE id = %s
            """)
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




async def get_all_student():
    connection = db_connection()
    cursor = connection.cursor()
    try:
        get_all_teachers_query = sql.SQL("""
            SELECT name, grade, sphere, description FROM student WHERE show = true
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
        SELECT name, grade, sphere, description FROM student 
        WHERE 
        grade in %s and 
        sphere in %s and 
        show = true
        """)

        if not grade and sphere:
            cursor.execute(fteachers_query, (all_grades, sphere))
        elif not sphere and grade:
            cursor.execute(fteachers_query, (grade, all_spheres))
        elif not grade and not sphere:
            cursor.execute(fteachers_query, (all_grades, all_spheres))
        else:
            cursor.execute(fteachers_query, (grade, sphere))

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