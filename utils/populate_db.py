from html import entities
import sqlite3
import uuid
from datetime import datetime


def connect_db():
    """Set up connection to SQLite3 database
        return: connection(obj)
    """
    try:
        connection = sqlite3.connect('audit-log.sqlite', check_same_thread=False)
    except sqlite3.Error as error:
        print(error)
    return connection


def populate_tables(connection):
    """ Populates audit-log database tables """
    c = connection.cursor()

    events_data = [
        (str(uuid.uuid4()),datetime.now().strftime("%d-%m-%Y"),1,1,1),
        (str(uuid.uuid4()),"13-02-2022",2,1,1),
        (str(uuid.uuid4()),"02-05-2022",3,1,1),
        ]

    user_data = [
        ("jojo",str(uuid.uuid4()),True),
        ("subin",str(uuid.uuid4()),True),
        ("canonical",str(uuid.uuid4()),True),
        ("pythonlover",str(uuid.uuid4()),False),
    ]

    """ table EVENTS """
    c.executemany("""INSERT INTO events(
                event_uuid,
                created_at,
                user_id,
                type_id,
                entity_id)
                VALUES(?,?,?,?,?);""",events_data)

    """ table EVENTTYPES """
    c.execute("""INSERT INTO eventtypes(
                type
                )
                VALUES("CREATE"),("UPDATE");""")

    """ table ENTITIES """
    c.execute("""INSERT INTO entities(
                entity
                )
                VALUES("resource"),("account");""")

    c.executemany("""INSERT INTO users(
                username,
                user_uuid,
                is_active
                )
                VALUES(?,?,?);""",user_data)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    connection = connect_db()
    populate_tables(connection)
