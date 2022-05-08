import sqlite3
import datetime
import uuid
import logging


# initially I made get, post functions in each Daos.
# making some command get, post functions. I can make it a parent class and use for other dao.

class Dao:
    def __init__(self):
        self.connection = sqlite3.connect('audit-log.sqlite',check_same_thread=False)
        self.cursor = self.connection.cursor()

        
    # doing below causes threading issue..
    # def execute_query(self,query,param={}):
    #     self.cursor.execute(query,param)

    def _get_placeholders(self,values):
        """ Helper function to clean up keys for sqlite parameters"""
        # {'event_uuid': '90c48355-b274-4966-a894-7c80febfbf94', 'creatd_at': '2022-05-06 19:43:26.798362', 'user_id': 1, 'type_id': 'UPDATE', 'entity_id': 2}
        # :event_uuid, :creatd_at, :user_id, :type_id, :entity_id
        key_list = [key for key in values.keys()]
        placeholders = ""
        for key in key_list:
            placeholders = placeholders +  ":{key},".format(key=key)
        return placeholders[:-1]
            
    def get(self): 
        query = "SELECT * FROM {}".format(self.table)
        rows = self.cursor.execute(query).fetchall()
        return rows

    def get_filtered(self, **values): #{rowid=}
        query = "SELECT * FROM {} WHERE {}".format(self.table,values)
        rows = self.cursor.execute(query).fetchone()
        return rows

    def post(self, **values):
        placeholders = self._get_placeholders(values)
        query ="""
        INSERT INTO {table}
        VALUES ({placeholders})
        """.format(table=self.table, placeholders=placeholders)
        print(query,values)
        rows = self.cursor.execute(query,values)


class EventDao(Dao):
    def __init__(self):
        self.user_dao= UserDao()
        self.table = "events"
        # super().__init__(self.table)
        # self.user_dao=UserDao()
        # self.eventtype_dao=EventtypeDao()
        # self.entity_dao=EntityDao()

    def get_all_events(self):
        # instance method(inhereted)
        return self.get()

    # event_dao.post_event(user=user_id,type=type_id,entity=entity_id)
    def post_event(self, **fields):
        
        event_uuid = str(uuid.uuid4())
        created_at = str(datetime.datetime.now())

        # have to get rowid from values
        # but to do that, have to post (user type entity) first
        # solution : just do it only for user
        print(fields)
        user = fields['user'] # "jojo"
        entity = fields['entity']
        type = fields['type']
        # u =self.cursor.execute("""SELECT rowid from users WHERE username=:user""",{'username':user})
        # this picksup events table..! instanciate first?
        self.user_dao.post_user(self,user=user,entity=entity,type=type)

        # user_id = UserDao.get_user(user)["id"] # -> object {}

        # type = fields['type']
        # type_id = EventtypeDao.get_type(type)["id"]
        
        # entity = fields['entity']
        # entity_id = EntityDao.get_type(entity)["id"]

        # either this or extract time from request.header
        self.post(event_uuid=event_uuid, creatd_at=created_at,user_id=user_id,type_id=type,entity_id=entity)

        # parser = {"user":user,"type":type,"entity":entity}
        # user_id = self.db.execute("SELECT rowid FROM users WHERE username=:user",{"username":user})
        # type_id = self.db.execute("SELECT rowid FROM eventtypes WHERE type=:type",{"type":type})
        # entity_id = self.db.execute("SELECT rowid FROM entities WHERE name=:entity",{"name":entity})\


    def update_event(self, event_id):
        pass


class UserDao:
    def __init__(self):
        self.table="users"
        # super().__init__(self.table)


    def get_user(self):
        return self.get()

    # import pdb 
    # pdb.set_trace()
    def post_user(self,**fields):
        print(fields)
        username = fields["user"]
        user_uuid = str(uuid.uuid4())
        is_active = True
        # entity_id = EntityDao.get(name='user')
        entity_id = fields["entity"]

        self.post(user_uuid=user_uuid,username=username,is_active=is_active,entity_id=entity_id)
        pass


class EventtypeDao:
    def __init__(self, database):
        super().__init__("eventtypes")
        
    def get_eventtype():
        pass

    def post_eventtype(self,**values):
        self.post(values)
        
        pass


class EntityDao:
    def __init__(self, database):
        super().__init__("entities")

    def get_entitytype(self):
        pass

    def post_entitytype(self,**values):
        self.post(values)
    
        pass


class ResourceDao:
    def __init__(self, database):
        super().__init__("resources")

    def get_resource():
        pass

    def post_resource():
        pass