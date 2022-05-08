# Auditor Microservice


## Description
Auditor Microservice listens to set of events from other system, with ability to store and retrieve such events data.\
For convinience we assume that the system is a basic CRUD web service.\


## Initial design decisions
To make Auditor Microservice runs on HTTP server and provides HTTP endpoint efficiently, this project was built with Python micro web framework Flask and Sqlite3 as a data storage mechanism.\
Note that this project only utilizes the bare minimum of Flask mainly for routing and running HTTP server.

Audit logs should be generated whenever there is a meaningful change to database of host system.\
Auditor Microservice would be listening to changes coming to the system, and interpret:

1. what entity was changed?  -> resource, account ...
2. what was the type of event? -> UPDATE, DELETE ...
3. When was the event happened? - 2022-01-01 2:00 GTM 
4. By Who? -> username

Before commiting to write code I have decided to imagine what would request and response look like.\
In their raw form, they will look something like below:

### `http method = GET `
#### request

    get_me_logs_with_this_values =
        {
        # query of choice, can be multiple
        username: jojo
        }

#### response

    response=
        {
            user =[
                {username: jojo}
                {user-uuid: iwjfak2hl1jaslf-alwejflasjd}
            ]
            target-entity: resource
            event-uuid : qrwr2014a9-sfahalwf2840
            event-type: CREATE
            datetime: 2022-04-02 GMT 12:00
        }

        log(" user {username, user-uuid} performed {event-type} on {target-entity}  at{datetime} " ,200)



### `http method = POST`
#### request
    payload ={
        username: username
        target-entity: resource
        event-type: CREATE
    }

#### response
    log(success, 201)

Auditor API and does not provide a full front-end feature.
It will provide response in basic JSON format to given requests.


## Deployment (Ubuntu)
- to be written


## Testing
send curl request with prepared json strings to simulate incoming requests.

`GET`\
    querying is possible by different field values
  - by user 
  - by datetime
  - by eventtype
  - by entity

keys: user, datetime, event-type, target-entity
if there are no key:value given, it will get all rows
```bash
$curl --location --request GET 'localhost:5000/search' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"jojo",
    "datetime":"2002-07-31",
    "event-type":"UPDATE",
    "target-entity":"resource"
}'
```

`POST`

fixed keys: username, event-type, target-entity
if not all key:values are provided, it will log error
```
$curl --location --request POST 'http://127.0.0.1:5000/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "jojo",
    "event-type": "UPDATE",
    "target-entity": "resource"
}'
```
