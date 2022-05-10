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


@app.route("/search", methods=['GET']) 
def get_event_log():
    # try:
    payload = request.get_json()

    by_user = payload.get("username",None)
    by_datetime = payload.get("datetime",None) #ascending and decending options
    by_type = payload.get("event-type",None)
    by_entity = payload.get("target-entity",None)
    
    query_param = {
        "username": by_user,
        "datetime": by_datetime,
        "event-type": by_type,
        "target-entity": by_entity
    }

    result = event_dao.get_events(query_param)
    return jsonify("result: ",result,200)

    # except Exception as e:
    #     return {'message': 'JSON_DECODE_ERROR'}


@app.route("/", methods=['POST'])
def post_event_log():
    payload = request.get_json()

    event_dao.post_event(
        username=payload.get("username"),
        type=payload.get("event-type"),
        entity=payload.get("target-entity"),
        )
    return jsonify("success",201)


if __name__ == "__main__":
    app.run()
