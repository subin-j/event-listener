import sqlite3
import datetime
import uuid
import logging

connection = sqlite3.connect('audit-log.sqlite',check_same_thread=False)
cursor = connection.cursor()


#utility functions------------------------------------------------------------
def _get_insert_placeholders(values):
    """ Helper function to clean up keys for sqlite parameters"""
    key_list = [key for key in values.keys()]
    placeholders = ""
    for key in key_list:
        placeholders = placeholders +  ":{},".format(key)
    return placeholders[:-1]

def _get_select_placeholders(filters):
    filters = {k:v for k,v in filters.items() if v is not None}
    filter_list = [key for key in filters.keys()]
    placeholders=""
    for item in filter_list:
        placeholders = placeholders + "{}=:{} AND ".format(item,item)
    return placeholders[:-5]


# SQL functions------------------------------------------------------------
def _select(table): 
    query = "SELECT * FROM {}".format(table)
    rows = cursor.execute(query).fetchall()
    return rows

def _select_filtered(**kwargs): #{rowid=} table,*fields,**filters
    placeholders=_get_select_placeholders(kwargs["filters"])
    query = "SELECT {fields} FROM {table} WHERE {placeholders}".format(fields=kwargs["fields"],table=kwargs["table"],placeholders=placeholders)
    rows = cursor.execute(query,kwargs["filters"]).fetchall()
    return rows

def _insert_into(table,**values):
    placeholders = _get_insert_placeholders(values)
    query ="""
    INSERT INTO {table}
    VALUES ({placeholders})
    """.format(table=table, placeholders=placeholders)
    cursor.execute(query,values)
    connection.commit()

# DAOs -------------------------------------------------------------------
class EventDao:
    def __init__(self):
        self.table = "events"

    def get_event(self):
        events = _select("events")
        return events

    def get_filtered_event(self,filters):
        rows = _select_filtered(table=self.table,fields="*",filters=filters)
        return rows

    def post_event(self,**fields):
        event_uuid = str(uuid.uuid4())
        created_at = str(datetime.datetime.now())

        # if user_id: get rowid form users/ else: post user
        # same for entity and type
        user_id = fields['user']
        entity_id = fields['entity']
        type_id = fields['type']


        _insert_into("events",user=user_id,type=type_id,entity=entity_id,event_uuid=event_uuid,created_at=created_at)

        # user_id = UserDao.get_user(user)["id"] # -> object {}

        # type = fields['type']
        # type_id = EventtypeDao.get_type(type)["id"]
        
        # entity = fields['entity']
        # entity_id = EntityDao.get_type(entity)["id"]

        # either this or extract time from request.header

        # parser = {"user":user,"type":type,"entity":entity}
        # user_id = self.db.execute("SELECT rowid FROM users WHERE username=:user",{"username":user})
        # type_id = self.db.execute("SELECT rowid FROM eventtypes WHERE type=:type",{"type":type})
        # entity_id = self.db.execute("SELECT rowid FROM entities WHERE name=:entity",{"name":entity})\


class UserDao:
    def __init__(self,db):
        self.db = db

    def get_event(self,values):
        pass

    def post_user(self,**fields):
        pass


class EventtypeDao:
    def __init__(self):
        super().__init__("eventtypes")
        
    def get_eventtype():
        pass

    def post_eventtype(self,**values):
        pass


class EntityDao:
    def __init__(self, database):
        super().__init__("entities")

    def get_entitytype(self):
        pass

    def post_entitytype(self,**values):
        self.post(values)
        pass
