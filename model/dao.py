import sqlite3
import datetime
import uuid
import re
import logging

from config import DATABASE

connection = sqlite3.connect(DATABASE,check_same_thread=False)
cursor = connection.cursor()


# Utility functions
def _get_insert_placeholders(values :dict) ->str:
    """ Helper function to get query placeholders for _insert_into function """
    key_list = [key for key in values.keys()]
    placeholders = ""
    for key in key_list:
        placeholders = placeholders +  ":{key},".format(key=key)
    return placeholders[:-1]


def _get_select_placeholders(filters :dict) ->str:
    """ Helper function to get query placeholders for _select_filtered function """
    filters = {k:v for k,v in filters.items() if v is not None}
    filter_list = [key for key in filters.keys()] #["username"]
    placeholders=""
    for item in filter_list:
        placeholders = placeholders + "{}=:{} AND ".format(item,item)
    return placeholders[:-5]


# SQL functions
def _select(table :str) ->list: 
    """ Performs select query with no constraints """
    query = "SELECT * FROM {}".format(table)
    rows = cursor.execute(query).fetchall()
    return rows


def _select_filtered(**kwargs :dict) ->list:
    """ Performs select query with constrains : table, columns """
    placeholders = _get_select_placeholders(kwargs["query_param"])
    query = """
    SELECT {fields}
    FROM {table}
    WHERE {placeholders}
    """.format(fields=kwargs["fields"],table=kwargs["table"],placeholders=placeholders)
    rows = cursor.execute(query,kwargs["query_param"]).fetchall()
    return rows


def _insert_into(table :str,**kwargs :dict):
    """ Performs insert query with constrains : table and values """
    placeholders = _get_insert_placeholders(kwargs)
    query ="""
    INSERT INTO {table}
    VALUES ({placeholders})
    """.format(table=table, placeholders=placeholders)
    cursor.execute(query,kwargs)
    connection.commit()


# DAOs
class EventDao:
    def __init__(self):
        """ Master class with query methods for master table events.
            :param table: literal name of table.
            :param user_dao, eventtype_dao, entity_dao: 
                instance of other table classes, used for posting
                data to store foreign keys in table  events.
        """
        self.table = "events"
        self.user_dao = UserDao()
        self.eventtype_dao = EventtypeDao()
        self.entity_dao = EntityDao()


    def get_all_event(self) ->list:
        """ Returns all rows from table events """
        events = _select(self.table)
        return events


    def get_events(self, query_param: dict) ->list:
        """ Returns rows filtered by constraints from table events with keys.
            :param query_param: dictionary of request body key value.
        """
        fields = "*"
        # PROBLEM: fails when running get_something_id  
        # SOLUTION: default ids to None
        user_id = self.user_dao.get_user_rowid(username=query_param.get("username"))
        created_at = query_param.get("datetime",None)
        type_id = self.eventtype_dao.get_type_rowid(type=query_param.get("event-type"))
        entity_id = self.entity_dao.get_entity_rowid(entity=query_param.get("target-entity"))

        query_param = {
            "user_id":user_id,
            "created_at": created_at,
            "type_id":type_id,
            "entity_id":entity_id,
        }
        #fetch filtered rows and turn them into key:value pairs
        rows = _select_filtered(
            table=self.table,
            fields=fields,
            query_param=query_param)
        key_dict ={
                "event-uuid":"",
                "created-at":"",
                "username": "",
                "created-at":"",
                "event-type":"",
                "target-entity":"",
        }
        rows_dict = [dict(zip(key_dict,row)) for row in rows]
        for row in rows_dict:
            print(row)

        # getting the real values based on the rowid. where rowid=rowid
        for row in rows_dict: #row['username']
            row['username'] = self.user_dao.get_user({"rowid":row["username"]})[0][0]

        for row in rows_dict:
            row['event-type'] = self.eventtype_dao.get_eventtype({"rowid":row["event-type"]})[0][0]

        for row in rows_dict:
            row['target-entity'] = self.entity_dao.get_entity({"rowid":row["target-entity"]})[0][0]

        return rows_dict


    def post_event(self, **kwargs :dict):
        """ Performs insert query on table events.
            kwargs["user"] : username of request body.
            kwargs["type"] : event-type of request body.
            kwargs["entity"] : target-entity of request body.
        """
        event_uuid = str(uuid.uuid4())
        created_at = datetime.datetime.now().strftime("%d-%m-%Y")
        username = kwargs.get("username")
        type = kwargs.get("type")
        entity = kwargs.get("entity")

        # if user_id: get rowid form users/ else: post user
        # I probably can filter it better..
        user_id = self.user_dao.get_user_rowid(username=username)
        if user_id == "":
            self.user_dao.post_user(username=username)
        user_id = self.user_dao.get_user_rowid(username=username)

        type_id = self.eventtype_dao.get_type_rowid(type=type)
        if type_id == "":
            self.eventtype_dao.post_type(type=type)
        type_id = self.eventtype_dao.get_type_rowid(type=type)            

        entity_id = self.entity_dao.get_entity_rowid(entity=entity)
        if entity_id == "":
            self.entity_dao.post_entity(entity=entity)
        entity_id = self.entity_dao.get_entity_rowid(entity=entity)      
                    
        # the parameter order matters, now sure why
        _insert_into(
            self.table,
            event_uuid=event_uuid,
            created_at=created_at,
            user_id=user_id,
            type_id=type_id,
            entity_id=entity_id)


class UserDao:
    """Class with query methods for table users.
        :param table: literal name of table.
    """
    def __init__(self):
        self.table = "users"


    def get_user(self,query_param : dict) ->list:
        """ Returns all rows from table users """
        fields = "username"
        user = _select_filtered(
            table=self.table,
            fields=fields,
            query_param=query_param
            )
        return user


    def get_user_rowid(self, **query_param :dict) ->str:
        """ Returns rowid filtered by constraints from table users.
            :param query_param: dictionary of request body key value.
        """
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


    def post_user(self, **kwargs: dict):
        """ Performs insert query on table users.
        """
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
    """Class with query methods for table eventtypes.
        :param table: literal name of table.
    """
    def __init__(self):
        self.table = "eventtypes"


    def get_eventtype(self,query_param : dict) ->list:
        """ Returns all rows from table types """
        fields = "type"
        type = _select_filtered(
            table=self.table,
            fields=fields,
            query_param=query_param
            )
        return type


    def get_type_rowid(self, **query_param :dict) ->str:
        """ Returns rowid filtered by constraints from table eventtypes/
            :param query_param: dictionary of request body key value.
        """
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


    def post_type(self, **kwargs :dict):
        """ Performs insert query on table eventtypes.
        """
        type = kwargs.get("type")
        _insert_into(
            self.table,
            type=type,
        )


class EntityDao:
    """Class with query methods for table entities.
        :param table: literal name of table.
    """
    def __init__(self):
        self.table = "entities"


    def get_entity(self,query_param : dict) ->list:
        """ Returns all rows from table types """
        fields = "entity"
        entity = _select_filtered(
            table=self.table,
            fields=fields,
            query_param=query_param
            )
        return entity



    def get_entity_rowid(self, **query_param :dict) ->str:
        """ Returns rowid filtered by constraints from table entities.
            :param query_param: dictionary of request body key value.
        """
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


    def post_entity(self, **kwargs :dict):
        """ Performs insert query on table entities.
        """
        type = kwargs.get("entity")
        _insert_into(
            self.table,
            type=type,
        )
