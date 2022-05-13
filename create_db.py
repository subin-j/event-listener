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


# def post_new_data(user,type,entity):
#     connection.execute("INSERT INTO events(user_id, type_id, entity_id) VALUES (?,?,?);",
#     (user,type,entity))

# def get_table(table):
#     result = connection.execute("select * from events").fetchall()
#     return result

# tempt json data below for quick testing
# event_list=[
#     {   
#         "id":1,
#         "uuid":"wefhalf",
#         "type":"UPDATE(type id: 2)",
#         "created_at":"2022-04-24",
#         "entity":"user(entity id:1) ",
#         "user_id":1
#     }
# ]

# event_type_list=[
#     {
#         "id":1,
#         "type":"CREATE"
#     },
#     {
#         "id":2,
#         "type":"UPDATE",
        
#     }
# ]

# entity_list=[
#     {
#         "id":1,
#         "name":"users",
#     },
#     {
#         "id":2,
#         "name":"resources",
#     }
# ]
# user_list =[
#     {   
#         "id":1,
#         "entity_id":1,
#         "username":"jojo",
#         "user_uuid":"sdabwefabs",
#         "password":"12341234",
#         "is_active":1,
#     }
# ]

# resource_list = [
#     {
#         "id":1,
#         "entity_id":2,
#         "price":30.5,
#     }
# ]
# import sqlite3
# import datetime
# import uuid


# #connect to sqlite3 db and create cursor
# conn = sqlite3.connect(':memory:')
# c = conn.cursor()

# # clears table
# # c.execute("DROP TABLE events")

# #creates table
# c.execute("""CREATE  TABLE events(
#             event_uuid text,
#             event_name text,
#             event_type int,
#             datetime text
#             )""")

# # uuid = sqlite3.register_adapter(uuid.UUID, lambda b: u.bytes_le)

# # #inserting a new event
# c.execute(
#     "INSERT INTO events (event_uuid, event_name, event_type, datetime) VALUES (?, ?, ?, datetime('now'))",('1755c702-12fc-4303-8f15-599042078447','hueng','1')
#     )

# #print what we have
# c.execute("SELECT * FROM events")
# print(c.fetchall())

# #close connection safely
# conn.commit()
# conn.close()

