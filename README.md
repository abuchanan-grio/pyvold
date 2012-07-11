Pyvold is a simple [Pyramid](http://docs.pylonsproject.org/en/latest/docs/pyramid.html)-based wrapper around [Voldemort](http://project-voldemort.com/) providing a clientless RESTful API.

---

###Installation###

* Install Pyramid following the [directions on their site](http://docs.pylonsproject.org/projects/pyramid/en/1.3-branch/narr/install.html#installing-pyramid-on-a-unix-system), which more or less boil down to:

        $ sudo easy_install virtualenv  # if you don't already have it
        $ virtualenv --no-site-packages env
        $ cd env
        $ ./bin/easy_install pyramid

* Install and start Voldemort following [their quickstart guide](http://project-voldemort.com/quickstart.php), which boils down to:

        $ curl -O http://cloud.github.com/downloads/voldemort/voldemort/voldemort-0.90.1.tar.gz
        $ tar -xzf voldemort-0.90.1.tar.gz
        $ cd voldemort-0.90.1
        $ ./bin/voldemort-server.sh config/single_node_cluster 2>&1 > ../voldemort.log &
        $ cd ..

* Install the Voldemort python client in the virtualenv following [the instructions in their README](https://github.com/voldemort/voldemort/tree/release-090/clients/python):

    * Install Google protobuf > 2.3.0
    
            $ # (in the env directory from above)
            $ curl -O https://protobuf.googlecode.com/files/protobuf-2.4.1.tar.bz2
            $ tar -xzf protobuf-2.4.1.tar.bz2 
            $ cd protobuf-2.4.1
            $ ./configure $(dirname $(pwd)) && make && make check && make install
        
    * Install the voldemort python client itself
  
            $ cd ../voldemort-0.90.1 # (back in the voldemort directory)
            $ cd clients/python
            $ ../../../bin/python setup.py install
            $ cd ../../..

* Install and run pyvold:

        $ # (in the env directory from above)
        $ git clone git://github.com/abuchanan-grio/pyvold.git
        $ ./bin/python pyvold/pyvold.py 2>&1 >pyvold.log &

* That should do it.

###Startup and shutdown###

This is for reference for the second+ time around, the installation process includes starting both of these.

Startup:

    $ cd env
    $ cd voldemort-0.90.1
    $ ./bin/voldemort-server.sh config/single_node_cluster 2>&1 > ../voldemort.log &
    $ cd ..
    $ ./bin/python pyvold/pyvold.py 2>&1 >pyvold.log &

Shutdown:

    $ cd env/voldemort-0.90.1
    $ ./bin/voldemort-stop.sh
    $ # and then just send pyvold a SIGHUP however makes you happy, e.g.,
    $ fg
    ^C  # if you haven't changed terminals, or
    $ killall python    # if you don't have any other python processes you need running
    
###The API###

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
    deleted 'key'


*Potential additions*: Fleshing out the RESTfulness by making better use of HTTP response codes when values aren't found, errors, etc.
