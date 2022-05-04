import json
import sqlite3
from flask import (
    Flask,
    request,
    jsonify,
)

import config
from model import EventDao
from view import * 
from service import *

app = Flask(__name__)
app.debug = True

# def log_audit_trail(contents):
#     """ 
#     Front-end sends curl request with action data in body -> body= {"Who When on What}
#     1. is method GET? -> filter result by field & print result
#     2. is method POST/PUT? -> do DB action & print result
#     """

#     ip="ip"
#     performed_at="performed_at"
#     user="user"
#     event_type = contents["event_type"]
#     entity_type_field="entity_type_field"
#     outcome="outcome"
    
#     field="field varies on entity type."

#     print("Ip{ip} at{performed_at} by{user} performed{event_type} on{entity_type} on field{field} // outcome={outcome}"
#     .format(
#         ip=ip,
#         performed_at=performed_at,
#         user=user,
#         event_type=event_type,
#         field=entity_type_field,
#         outcome=outcome
#     ))

#     return 
connection = sqlite3.connect('audit-log.sqlite',check_same_thread=False)
c = connection.cursor()
event_dao = EventDao(c)


# service layers-------------------------------
# only GET methods take query parameter, rest is json

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
    
    result = event_dao.get_event()


    return jsonify("query result: ",result,200)


@app.route("/", methods=['POST'])
def post_event_log():
    # request.get_json returns python dict in body of request
    content = request.get_json()

    user = content["user_id"]
    type = content["type"]
    entity = content["entity_id"]

    event_dao.post_event(user,type,entity)

    connection.commit()
    connection.close()
    return jsonify("success"),201



@app.route("/", methods=['DELETE'])
def delete_event_log():
# connection = connect_db()
# cursor = connection.cursor()
#do something and get data from DB and serealize to return as json
# if event log is not empty:
    pass

    # if event_type == 0:
    #     #look up user with the uuid
    #     if uuid == account["user_uuid"]:
    #         if account["is_active"] == 1:
    #             account["is_active"] = 0
    #         else:
    #             result = "account already is deactivated"
    #     else:
    #         result = "didnt find matching account uuid"


if __name__ == "__main__":
    app.run()
    

# @app.route('/', methods=['GET'])
# def query_logs():
#     name = request.args.get('name')
#     print(name)
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for record in records:
#             if record['name'] == name:
#                 return jsonify(record)
#         return jsonify({'error': 'data not found'})

# @app.route('/', methods=['POST'])
# def create_record():
#     record = json.loads(request.data)
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#     if not data:
#         records = [record]
#     else:
#         records = json.loads(data)
#         records.append(record)
#     with open('/tmp/data.txt', 'w') as f:
#         f.write(json.dumps(records, indent=2))
#     return jsonify(record)

# @app.route('/', methods=['PUT'])
# def update_record():
#     record = json.loads(request.data)
#     new_records = []
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#     for r in records:
#         if r['name'] == record['name']:
#             r['email'] = record['email']
#         new_records.append(r)
#     with open('/tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
#     return jsonify(record)
    
# @app.route('/', methods=['DELETE'])
# def delte_record():
#     record = json.loads(request.data)
#     new_records = []
#     with open('/tmp/data.txt', 'r') as f:
#         data = f.read()
#         records = json.loads(data)
#         for r in records:
#             if r['name'] == record['name']:
#                 continue
#             new_records.append(r)
#     with open('/tmp/data.txt', 'w') as f:
#         f.write(json.dumps(new_records, indent=2))
#     return jsonify(record)
