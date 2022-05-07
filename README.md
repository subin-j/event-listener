# Auditor Microservice


## Description
Auditor Microservice listens to set of events from other system, with ability to store and retrieve such events data.
For convinience we assume that the system is a basic CRUD web service.
Examples of events to be recorded:

- a new customer account was created for a given identity
- a user performed an action on a resource
- a user was deactivated


## Initial design decisions
To make Auditor Microservice runs on HTTP server and provides HTTP endpoint efficiently, this project was built with Python micro web framework Flask and Sqlite3 as a data storage mechanism.
Note that this project only utilizes the bare minimum of Flask mainly for routing and running HTTP server.

Audit logs should be generated whenever there is a meaningful change to database of host system. Auditor Microservice would be listening to changes coming to the system, and interpret:

1.what entity was changed?  ex) customer.updated or event.updated 
2.what was the type of event? ex) among CRUD
3.When was the event happened? ex) 2022-20-04 GMT 12:00 (10 min ago)
4.By Who? ex) customer id with name 

Before commiting to write code I have decided to imagine what would request and response look like.
In their raw form, they will look something like below:

### http method = GET
    #### request
    payload =
        {
        # query strings of choice
        user: username
        entity : resource
        event_type: CREATE
        }

    #### response
        sucess response=
            {
                user: username
                target entity: resource
                property: name
                event_uuid : qrwr2014a9sfahalwf2840
                event_type: UPDATE
                datetime: 2022-04-02 GMT 12:00
            }

        log(" user {username} performed {event_type} on {property} in{entity} at{datetime} " ,200)

        failed response=
            {
                result: failed
                reason: does not exist
            }
        log("failed to fetch the data: {reason}, 500)


### http method = POST
    #### request
    payload ={
        user: username
        entity : resource
        event_type: CREATE
    }

    #### response
        success response=
        log(success, 201)

        failed response=
        log(failed,500)


Auditor API and does not provide a full front-end feature.
It will provide response in basic JSON format to given requests.


## Deployment (Ubuntu)
- to be written


## Testing
send curl request with very specific json strings to simulate the system's requests.

- GET
    querying by different field values
    - by user 
    - by datetime
    - by eventtype
    - by entity

curl -X GET localhost:5000/search?<user_id>
curl -X GET localhost:5000/search?<event_id>

- POST
curl -X POST {json_data} localhost:5000/
