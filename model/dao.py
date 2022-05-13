import sqlite3
import datetime
import uuid
import re
import logging

connection = sqlite3.connect('audit-log.sqlite',check_same_thread=False)
cursor = connection.cursor()


# Utility functions------------------------------------------------------------
def _get_insert_placeholders(values):
    """ Helper function to get query placeholders for _insert_into function """
    key_list = [key for key in values.keys()]
    placeholders = ""
    for key in key_list:
        placeholders = placeholders +  ":{key},".format(key=key)
    return placeholders[:-1]

def _get_select_placeholders(filters): #{"entity":None}
    """ Helper function to get query placeholders for _select_filtered function """
    filters = {k:v for k,v in filters.items() if v is not None}
    filter_list = [key for key in filters.keys()] #["username"]
    placeholders=""
    for item in filter_list:
        placeholders = placeholders + "{}=:{} AND ".format(item,item)
    return placeholders[:-5]


# SQL functions------------------------------------------------------------
def _select(table): 
    """ Performs """
    query = "SELECT * FROM {}".format(table)
    rows = cursor.execute(query).fetchall()
    return rows


def _select_filtered(**kwargs): # table,*fields,**filters
    placeholders = _get_select_placeholders(kwargs["query_param"]) # query_parmeter ={"username":"jojo"}
    query = """
    SELECT {fields}
    FROM {table} 
    WHERE {placeholders}
    """.format(fields=kwargs["fields"],table=kwargs["table"],placeholders=placeholders)

    print("-select_filtered: ",query,kwargs["query_param"])
    rows = cursor.execute(query,kwargs["query_param"]).fetchall()
    return rows


def _insert_into(table,**kwargs):
    placeholders = _get_insert_placeholders(kwargs)
    query ="""
    INSERT INTO {table}
    VALUES ({placeholders})
    """.format(table=table, placeholders=placeholders)
    cursor.execute(query,kwargs)
    connection.commit()

# DAOs -------------------------------------------------------------------
class EventDao:
    def __init__(self):
        self.table = "events"
        self.user_dao = UserDao()
        self.eventtype_dao = EventtypeDao()
        self.entity_dao = EntityDao()

    def get_event(self):
        events = _select(self.table)
        return events


    def get_events(self, query_param):
        fields = "*"

        user_id = self.user_dao.get_user_rowid(username=query_param.get("username"))
        created_at = query_param.get("datetime",None)
        type_id = self.eventtype_dao.get_type_rowid(type=query_param.get("event-type"))
        entity_id = self.entity_dao.get_entity_rowid(entity=query_param.get("target-entity"))
        # PROBLEM: when get_something_id is None  SOLUTION: just default them to None

        query_param = {
            "user_id":user_id,
            "created_at": created_at,
            "type_id":type_id,
            "entity_id":entity_id,
        }

        rows = _select_filtered(
            table=self.table,
            fields=fields,
            query_param=query_param)

        return rows

    def post_event(self,**kwargs):
        event_uuid = str(uuid.uuid4())
        created_at = datetime.datetime.now().strftime("%d-%m-%Y")
        # Here i will fetch row ids from payload, for now i'm sending int values on request

        print("post_event kwargs: ",kwargs)
        # if user_id: get rowid form users/ else: post user
        # I probably can filter it better..
        user_id = self.user_dao.get_user_rowid(username=kwargs.get("user"))
        if user_id == "":
            self.user_dao.post_user(username=kwargs.get("user"))
        user_id = self.user_dao.get_user_rowid(username=kwargs.get("user"))

        type_id = self.eventtype_dao.get_type_rowid(type=kwargs.get("type"))
        if type_id == "":
            self.eventtype_dao.post_type(type=kwargs.get("type"))
        type_id = self.eventtype_dao.get_type_rowid(type=kwargs.get("type"))            

        entity_id = self.entity_dao.get_entity_rowid(entity=kwargs.get("entity"))
        if entity_id == "":
            self.entity_dao.post_entity(entity=kwargs.get("entity"))
        entity_id = self.entity_dao.get_entity_rowid(entity=kwargs.get("entity"))      
                    

        # user_id = kwargs.get('user')
        # type_id = kwargs.get('type')
        # entity_id = kwargs.get('entity')


        # the parameter order matters, now sure why
        _insert_into(
            self.table,
            event_uuid=event_uuid,
            created_at=created_at,
            user_id=user_id,
            type_id=type_id,
            entity_id=entity_id)

        # parser = {"user":user,"type":type,"entity":entity}
        # user_id = self.db.execute("SELECT rowid FROM users WHERE username=:user",{"username":user})
        # type_id = self.db.execute("SELECT rowid FROM eventtypes WHERE type=:type",{"type":type})
        # entity_id = self.db.execute("SELECT rowid FROM entities WHERE name=:entity",{"name":entity})\


class UserDao:
    def __init__(self):
        self.table = "users"

    def get_user(self,values):
        users = _select(self.table)

        return users

    def get_user_rowid(self, **query_param): #{"user":"jojo"}
        fields = "rowid"
        try:
            rows = _select_filtered(
                table=self.table,
                fields=fields,
                query_param=query_param)
            rowid = re.sub('[^A-Za-z0-9]+','',str(rows))
        except:
            return None

        return rowid

    # just to fill in user rowid to be used in events
    def post_user(self, **kwargs): #{,"username":"jojo"}
        username = kwargs.get("username")
        user_uuid = str(uuid.uuid4())
        is_active = True

        _insert_into(
            self.table,
            username=username,
            user_uuid=user_uuid,
            is_active=is_active,
        )

class EventtypeDao:
    def __init__(self):
        self.table = "eventtypes"
        
    def get_eventtype():
        pass

    def get_type_rowid(self, **query_param):
        fields = "rowid"
        try:
            rows = _select_filtered(
                table=self.table,
                fields=fields,
                query_param=query_param)
            rowid = re.sub('[^A-Za-z0-9]+','',str(rows))
        except:
            return None

        return rowid

    def post_type(self, **kwargs):
        type = kwargs.get("type")
        _insert_into(
            self.table,
            type=type,
        )


class EntityDao:
    def __init__(self):
        self.table = "entities"

    def get_entity_rowid(self, **query_param):
        fields = "rowid"
        try:
            rows = _select_filtered(
                table=self.table,
                fields=fields,
                query_param=query_param)
                # query_param={'entity':None})
            rowid = re.sub('[^A-Za-z0-9]+','',str(rows))
        except:
            return None
        return rowid

    def post_entity(self, **kwargs):
        type = kwargs.get("entity")
        _insert_into(
            self.table,
            type=type,
        )
