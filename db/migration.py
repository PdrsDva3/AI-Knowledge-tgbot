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


def migration_up():
    conn = db_connection()
    cur = conn.cursor()
    try:
        create = sql.SQL("""
        CREATE TABLE IF NOT EXISTS teacher  (
    id              bigint NOT NULL PRIMARY KEY,
    type varchar,
    name            varchar,
    surname        varchar,
    grade varchar,
    sphere varchar, 
    description varchar,
    sort integer default 1,
    show bool default false);
        """)

        cur.execute(create)  # Выполняем запрос на создание таблицы
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn:
            cur.close()
            conn.close()


def migration_down():
    conn = db_connection()
    cur = conn.cursor()
    try:
        drop = sql.SQL("""DROP TABLE IF EXISTS teacher """)

        cur.execute(drop)  # Выполняем запрос на создание таблицы
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn:
            cur.close()
            conn.close()

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



if __name__ == "__main__":
    migration_down()
    migration_up()
