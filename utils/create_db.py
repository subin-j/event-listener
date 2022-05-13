import sqlite3
from datetime import datetime


def connect_db():
    """ Set up connection to SQLite3 database
        return: connection(obj)
    """
    try:
        connection = sqlite3.connect('audit-log.sqlite', check_same_thread=False)
    except sqlite3.Error as error:
        print(error)
    return connection


def create_tables(connection):
    """ Create tables in database """

    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS events(
                event_uuid text NOT NULL,
                created_at text NOT NULL,
                user_id interger NOT NULL,
                type_id interger NOT NULL,
                entity_id interger NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(rowid),
                FOREIGN KEY(type_id) REFERENCES eventtypes(rowid),
                FOREIGN KEY(entity_id) REFERENCES entities(rowid)
                );""")

    c.execute("""CREATE TABLE IF NOT EXISTS eventtypes(
                type text NOT NULL UNIQUE
                );""")

    c.execute("""CREATE TABLE IF NOT EXISTS entities(
                entity text NOT NULL UNIQUE
                );""")

    c.execute("""CREATE TABLE IF NOT EXISTS users(
                username text NOT NULL UNIQUE,
                user_uuid text NOT NULL UNIQUE,
                is_active bool NOT NULL
                );""")

    # c.execute("""CREATE TABLE IF NOT EXISTS resources(
    #             price FLOAT NOT NULL,
    #             FOREIGN KEY(entity_id) REFERENCES entities(rowid)
    #             );""")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    connection = connect_db()
    create_tables(connection)


