import sqlite3
import datetime
import uuid
import logging


# initially I made get, post functions in each Daos.
# making some command get, post functions. I can make it a parent class and use for other dao.

class Dao:
    def __init__(self,table):
        self.connection = sqlite3.connect('audit-log.sqlite',check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.table = table
        
    # doing below causes threading issue..
    # def execute_query(self,query,param={}):
    #     self.cursor.execute(query,param)

    def _get_placeholders(self,values):
        # {'event_uuid': '90c48355-b274-4966-a894-7c80febfbf94', 'creatd_at': '2022-05-06 19:43:26.798362', 'user_id': 1, 'type_id': 'UPDATE', 'entity_id': 2}
        # :event_uuid, :creatd_at, :user_id, :type_id, :entity_id

        key_list = [key for key in values.keys()]
        placeholders = ""
        for key in key_list:
            placeholders = placeholders +  ":{key},".format(key=key)
        placeholders = placeholders[:-1]

        return placeholders
            
    def get(self): 
        query = "SELECT * FROM {}".format(self.table)
        rows = self.cursor.execute(query).fetchall()
        return rows

    def post(self, **values):
        placeholders = self._get_placeholders(values)

        query ="""
        INSERT INTO {table}
        VALUES ({placeholders})
        """.format(table=self.table, placeholders=placeholders)

        rows = self.cursor.execute(query,values)


class EventDao(Dao):
    def __init__(self):
        super().__init__("events")
        # self.table = 'events'

    def get_all_events(self):
        # instance method(inhereted)
        return self.get()

    # event_dao.post_event(user=user_id,type=type_id,entity=entity_id)
    def post_event(self, **fields):
        event_uuid = str(uuid.uuid4())
        created_at = str(datetime.datetime.now())
        user_id = fields['user']
        type = fields['type']
        entity = fields['entity']

        # either this or extract time from request.header
        self.post(event_uuid=event_uuid, creatd_at=created_at,user_id=user_id,type_id=type,entity_id=entity)



# EventDao.post_events()
    # def post_event(self,user,type,entity):
    #     event_uuid = (str(uuid.uuid4()))
    #     # either this or extract time from request.header
    #     created_at = datetime.datetime.now()

    #     # parser = {"user":user,"type":type,"entity":entity}
    #     # user_id = self.db.execute("SELECT rowid FROM users WHERE username=:user",{"username":user})
    #     # type_id = self.db.execute("SELECT rowid FROM eventtypes WHERE type=:type",{"type":type})
    #     # entity_id = self.db.execute("SELECT rowid FROM entities WHERE name=:entity",{"name":entity})\

    #     # have to insert user, type, entity first to their table to retreive rowids..
    #     self.db.execute("""
    #     INSERT INTO events(
    #         event_uuid,
    #         created_at,
    #         user_id,
    #         type_id,
    #         entity_id)
    #     VALUES (?,?,?,?,?);""",
    #     (event_uuid,created_at,user,type,entity))

    def update_event(self, event_id):
        pass


class UserDao:
    def __init__(self, database):
        self.db = database

    def get_user():
        pass

    def post_user(self,**values):
        self.post(values)
        
        pass


class EventtypeDao:
    def __init__(self, database):
        self.db = database
    def get_eventtype():
        pass

    def post_eventtype(self,**values):
        self.post(values)
        
        pass


class EntityDao:
    def __init__(self, database):
        self.db = database
    def get_entitytype():
        pass

    def post_entitytype(self,**values):
        self.post(values)
    
        pass


class ResourceDao:
    def __init__(self, database):
        self.db = database
    def get_resource():
        pass
    def post_resource():
        pass