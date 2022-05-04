import sqlite3
import datetime
import uuid

class EventDao:
    def __init__(self, database):
        self.db = database
        
    def get_event(self):
        events = self.db.execute("""
        SELECT
            * 
        FROM events   
        """).fetchall()
        for field in events:
            print(field)
        return events

    def post_event(self,user,type,entity):
        event_uuid = (str(uuid.uuid4()))
        # either this or extract time from request.header
        created_at = datetime.datetime.now()
        self.db.execute("""
        INSERT INTO events(
            event_uuid,
            created_at,
            user_id,
            type_id,
            entity_id)
        VALUES (?,?,?,?,?);""",
        (event_uuid,created_at,user,type,entity))


    def update_event(self, event_id):
        pass