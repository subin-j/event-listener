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
        (str(uuid.uuid4()),"2922-02-30",1,1,1),
        (str(uuid.uuid4()),"2002-07-31",2,2,2),
        ]

    user_data = [
        ("iamuser1",str(uuid.uuid4()),'pass123',True,1),
        ("iamuser2",str(uuid.uuid4()),'pass123',True,1),
    ]

    """ table EVENTS """
    c.executemany("""INSERT INTO events(
                event_uuid,
                created_at,
                user_id,
                type_id,
                entity_id)
                VALUES(?,?,?,?,?)
                ;""",events_data)

    """ table EVENTTYPES """
    c.execute("""INSERT INTO eventtypes(
                type
                )
                VALUES("CREATE"),("UPDATE");""")

    """ table ENTITIES """
    c.execute("""INSERT INTO entities(
                name        
                )
                VALUES("user"),("resource");""")

    c.executemany("""INSERT INTO users(
                username,
                uuid,
                is_active,
                entity_id
                )
                VALUES(?,?,?,?);""",user_data)

    c.execute("""INSERT INTO resources(
                price,
                entity_id
                )
                VALUES(
                    30.5,
                    1
                );""")

    connection.commit()
    connection.close()


if __name__ == "__main__":
    connection = connect_db()
    populate_tables(connection)
