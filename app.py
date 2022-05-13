from flask import (
    Flask,
    request,
    jsonify,
)

from config import JWT_KEY, ALGORITHM, API_KEY
from utils.decorators import authorization_required
from model import dao

app = Flask(__name__)
event_dao = dao.EventDao()


@app.route("/search", methods=['GET']) 
@authorization_required
def get_event_log():
    """ Endpoint for querying data in Events table. """
    try:
        payload = request.get_json()
        if payload == {} :
            result = event_dao.get_all_event()
        else:
            by_user = payload.get("username",None)
            by_datetime = payload.get("datetime",None)
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
    except Exception:
        return {'message': 'JSON_DECODE_ERROR'}


@app.route("/", methods=['POST'])
@authorization_required
def post_event_log():
    """ Endpoint for querying data in Events table. """
    try:
        payload = request.get_json()
        event_dao.post_event(
            username=payload.get("username"),
            type=payload.get("event-type"),
            entity=payload.get("target-entity"),
            )
        return jsonify("success",201)
    except Exception:
        return {'message': 'JSON_DECODE_ERROR'}


if __name__ == "__main__":
    app.run()
