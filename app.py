import json
import sqlite3
from flask import (
    Flask,
    request,
    jsonify,
)

import config
from model.data_access import EventDao,EntityDao, EventtypeDao, ResourceDao, UserDao
from view import * 
from service import *

app = Flask(__name__)
app.debug = True


# service layers-------------------------------
# only GET methods take query parameter, rest is json

event_dao = EventDao()
# user_dao = UserDao()
# type_dao = EventtypeDao()
# entity_dao = EntityDao()
# resource_dao = ResourceDao()


@app.route("/search", methods=['GET']) 
def get_event_log():
    # get methods: default/ by user uuid/ by event type/ by target entity
    # chain multiple filters
    query = request.args.to_dict()

    by_user = query.get("by-user",None)
    by_datetime=query.get("by-datetime",None) #ascending and decending options
    by_event_type=query.get("by-event-type",None)
    by_target_entity=query.get("by-target-entity",None)

    if by_user:
        user = by_user
        # search by uuid or username.
        """SELECT * from Events WHERE (user_id = user_uuid)"""
        pass

    if by_datetime:
        datetime = by_datetime
        pass
        """ SELECT * from events by (?), (order)"""
    
    if by_event_type:
        event_type = by_event_type
        """ SELECT * from events WHERE (event_type = event_type) """
        pass

    if by_target_entity:
        pass
    
    result = event_dao.get_all_events()
    # connection.commit()
    # c.close()

    print(result)
    return jsonify("query result: ",result,200)


@app.route("/", methods=['POST'])
def post_event_log():
    # request.get_json returns python dict in body of request
    content = request.get_json()

    user = content["user"] # "jojo"
    type = content["eventType"] # "UPDATE"
    entity= content["entity"] # "resource"

    # user_dao.post_user(user=user)
    # user = user_dao.get_user(user) # returns rowid
    event_dao.post_event(user=user,type=type,entity=entity)
    return jsonify("success"),201



if __name__ == "__main__":
    app.run()
