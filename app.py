import json
import sqlite3
from flask import (
    Flask,
    request,
    jsonify,
)

import config
from model import dao
from view import * 
from service import *

app = Flask(__name__)
app.debug = True


# service layers-------------------------------
# all method takes json as data

event_dao = dao.EventDao()
# user_dao = UserDao()
# type_dao = EventtypeDao()
# entity_dao = EntityDao()
# resource_dao = ResourceDao()


@app.route("/search", methods=['GET']) 
def get_event_log():
    payload = request.get_json() #{key:val}

    by_user = payload.get("username",None)
    by_datetime = payload.get("datetime",None) #ascending and decending options
    by_type = payload.get("event-type",None)
    by_entity = payload.get("target-entity",None)
    
    filters = {
        "user_id": by_user,
        "created_at": by_datetime,
        "type_id": by_type,
        "entity_id": by_entity
    }

    result = event_dao.get_filtered_event(filters)
    return jsonify("result: ",result,200)


@app.route("/", methods=['POST'])
def post_event_log():
    # request.get_json returns python dict in body of request
    payload = request.get_json()

    user = payload["user"] # "jojo"
    type = payload["eventType"] # "UPDATE"
    entity= payload["entity"] # "resource"

    event_dao.post_event(user=user,type=type,entity=entity)
    return jsonify("success",201)


if __name__ == "__main__":
    app.run()
