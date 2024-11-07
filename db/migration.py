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
        create = sql.SQL("""CREATE TABLE IF NOT EXISTS teacher
(
    id          bigint NOT NULL PRIMARY KEY,
    name        varchar,
    grade       varchar,
    sphere      varchar,
    description varchar,
    show        bool default false
);

CREATE index filters_grade on teacher using gin (to_tsvector('english', grade));
CREATE index filters_sphere on teacher using gin (to_tsvector('english', sphere));


CREATE TABLE IF NOT EXISTS student
(
    id          bigint NOT NULL PRIMARY KEY,
    name        varchar,
    grade       varchar,
    sphere      varchar,
    description varchar,
    show        bool default false,
    nickname    varchar
);
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
        drop = sql.SQL("""DROP TABLE IF EXISTS teacher, student;""")

        cur.execute(drop)  # Выполняем запрос на создание таблицы
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        return error
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    migration_down()
    migration_up()
