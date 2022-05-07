Auditor Microservice


# Description
Auditor Microservice listens to set of events from other system, with ability to store and retrieve such events data.
For convinience we assume that the system is a basic billing service.
Examples of events to be recorded:

- a new customer account was created for a given identity
- a customer performed an action on a resource
- a customer was billed a certain amount
- a customer account was deactivated


# Initial design decisions
To make Auditor Microservice runs on HTTP server and provides HTTP endpoint efficiently, this project was built with Python micro web framework Flask and Sqlite3 as a data storage mechanism.
Note that this project only utilizes the bare minimum of Flask mainly for routing and running HTTP server.

Audit logs should be generated whenever there is a meaningful change to database of host system. Auditor Microservice would be listening to changes coming to the system, and interpret:

1.what entity was changed?  ex) customer.updated or event.updated
2.what was the type of event? ex) among CRUD
3.When was the event happened? ex) 2022-20-04 GMT 12:00 (10 min ago)
4.By Who? ex) customer id with name 

Before commiting writing code I have decided to imagine what would request and response look like.
In their raw form, they will look something like below:

<request json example >
payload =
    {
    entity : CustomerData
    datetime: 2022-02-02,
    event_type: CREATE
    
    }

<response json example >
sucess response=
    {
        result: success
        entity: CustomerData
        property: name
        event_uuid : qrwr2014a9sfahalwf2840
        event_type: UPDATE
        datetime: 2022-04-02 GMT 12:00
        customer: 073 SUBIN JEONG ,125.22.33.22
    }

failed response=
    {
        result: failed
        reason: does not exist
    }

Auditor API and does not provide a full front-end feature.
It will provide response in basic JSON format to given requests.


# Deployment (Ubuntu)

# Testing
send curl request with very specific json strings to simulate the system's requests.

- Ping
curl -X GET localhost:5000/ping

- GET
curl -X GET localhost:5000/get_log/customer/<user_id>


curl -X GET localhost:5000/get_log/event/<event_id>

- POST
curl -X POST {key:value} localhost:5000/create_log/<user_id>
curl -X POST localhost:5000/create_log/<event_id>

- PUT
curl -X PUT localhost:5000/update_log/<user_id>
curl -X PUT localhost:5000/update_log/<event_id>

- DELETE




Querying by different field values
- by User 
- by datetime
- by 



로그 시스템 

# GET 백->프
-> 딴 시스템에서 '아이디'=조조 '뭐햇냐면'='업뎃' 이 기록 내놔라 보냄

-> 내 db 뒤져

-> 잘 json 으로 예쁘게 정리해서 프론트에 싣어보내줌 
    json={
    '유저 아이디' = 'jojo',
    '비번' = '1234,,
    '뭐했냐면' = '업뎃',
    '언제' = '오늘'
    }


# POST  주로 프->백
-> 다른 시스템(백엔드 or 프론트) 에서 저장할 새 데이터 보냄
    아마 잘 정리되서 보냈으면 이렇게 생겼겠음
    json={
    메소드 = POST
    '유저 아이디' = 'jojo',
    '비번' = '1234,,
    '뭐했냐면' = '업뎃',
    '언제' = '오늘'
    }

-> 어떤식으로 들어오는지에 따라 잘 정리해서

-> 누가 언제 뭐했다 정보를 로그 DB 저장



