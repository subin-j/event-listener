# Auditor Microservice


## Description
Auditor Microservice listens to set of events from other system, with ability to store and retrieve such events data.\
For convinience we assume that the system is a basic CRUD web service.


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
#### `request` 

```python
    get_me_logs_with_this_values =
        {
        # query of choice, can be multiple
        "username": "jojo"
        }
```
#### `response` will return all data containing the given field value.
```python
    [response=
        {
            "username": "jojo"}
            "target-entity": "resource"
            "event-uuid" : "qrwr2014a9-sfahalwf2840"
            "event-type": "CREATE"
            "datetime": "2022-04-02
        }

    ("SUCCESS" ,200)]
```


### `http method = POST`
#### `request`
```python
    payload ={
        "username": "jojo"
        "target-entity": "resource"
        "event-type": "CREATE"
    }
```
#### `response`
```python
    [(success, 201)]
```

Auditor API and does not provide a front-end feature.
It will provide response in basic JSON format to given requests.


## Deployment (Ubuntu)
- to be written


## Testing
Send curl request with prepared json strings to simulate incoming requests.

contents of **--data-raw** can be modified.
Make sure to include the token in header as written, this API does not provide login endpoint. 

`GET`\
    querying is possible by different field values, it will return the intersection.

    keys: username, datetime, event-type, target-entity.

    if there are no key:value given, it will get all rows.

```bash
$curl -L -X GET 'localhost:5000/search' \
-H 'Content-Type: application/json' \
-H 'Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5Ijoic3VwZXJfc2VjcmV0ZV9hcGlfa2V5In0.3JG2tIV1pfrDLgXnO0e6mDsyjmQe9ZkKmhXxkhtKtE8' \
--data-raw '{
    "username" : "jojo",
    "event-type": "CREATE",
    "datetime": "13-05-2022",
    "target-entity": "resource"

}'
```

`POST`

fixed keys: username, event-type, target-entity
if not all key:values are provided, it will log error
```bash
$curl -L -X POST 'http://127.0.0.1:5000/' \
-H 'Content-Type: application/json' \
-H 'Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGlfa2V5Ijoic3VwZXJfc2VjcmV0ZV9hcGlfa2V5In0.3JG2tIV1pfrDLgXnO0e6mDsyjmQe9ZkKmhXxkhtKtE8' \
--data-raw '{
    "username": "hello",
    "event-type": "NEW_EVENT_TYPE",
    "target-entity":"new_entity"
}'
```
