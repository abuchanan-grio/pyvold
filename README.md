Pyvold is a simple [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html)-based wrapper around [Voldemort](http://project-voldemort.com/) providing a clientless RESTful API.

---
=The API=

POST or PUT a value to set or modify it:

    $ curl -X POST -d key=value http://localhost:8080
    key => value
    $
    $ curl -X PUT -d key=value http://localhost:8080
    key => value
    
GET a value to get its current value

    $ curl -X GET http://localhost:8080?key
    value

Delete a value to remove that key

    $ curl -X DELETE http://localhost:8008?key
    deleted key


*Potential additions*: Fleshing out the RESTfulness by making better use of HTTP response codes when values aren't found, errors, etc.
