# Configuring Mongo write-behind

Unlike other recipes, this recipe requires a valid redis-server with RedisJSON.  This is in the redismod image in the docker-compose.yml file

# Docker Redis to Redis gears example
## Set up Redis Server
To setup a Redis server and a second redis serer to replicate data to, use docker compose
```bash
docker-compose up -d
```
## Setup python environment
### Create python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### Install gears_cli into python environment
```bash
pip install gears-cli
```
-----------------
## Create MongoDB database using mongo express
* Log into mongo express using following URL in your browser
[http://localhost:8081
](http://localhost:8081)
* Enter "db" and Click on "Create Database"

# Running the recipe
```bash
gears-cli run --host 127.0.0.1 --port 6379 example.py --requirements requirements.txt
```
### Data storage examples
open redis cli with container
```bash
 docker exec -it redis redis-cli
```

Data should be stored in Redis using the various JSON commands from [RedisJSON](https://redisjson.io). In all cases, initial writes, and updates rely on the same underlying mechanism.

**Storing data**

```
json.set person:1 . '{"hello": "world"}'
```

**Storing data, then adding more fields**

```
json.set person:1 . '{"hello": "world", "my": ["list", "has", "things"]}'
json.set person:1 . '{"someother": "fieldtoadd"}'
```

**Storing data, then updating**

```
json.set person:1 . '{"hello": "world", "my": ["list", "has", "things"]}'
json.set person:1 . '{"hello": "there!"}'
```
**Verify Data stored in MongoDB**
* Log into mongo express using following URL in your browser
[http://localhost:8081
](http://localhost:8081)
* Click on "db"
* Click on "persons" to see records flowing in from MongoDB

**Storing data, then deleting**

```
json.set person:1 . '{"hello": "world"}'
json.del person:1
```

## How this works

A connection is made to Mongo, by the Redis server, running RedisGears.  A JSON mapping is created (see below), so that we can update sub-sections of the JSON document.

The recipe below will write data to a collection called *persons* on the Mongo server.  All data stored in *persons* will be part of a JSON document containing a standard id, and a JSON document containing the key *gears* at the top level. This JSON document will contain the data migrated from Redis to Mongo.

Let's assume the Redis JSON data contains the following:

```{'hello': 'world'}```

In that case the data would be replicated to Mongo, appearing as below. Note that Mongo will add an *_id* field for its entry. The *person_id* below refers to the key used to store data in Redis. Assuming that example above was stored in Redis (i.e JSON.SET), using the key *person:1*, the following would be the output in Mongo.

**NOTE**: redisgears reserves the internal key name **redisgears**, so you must ensure that your json hierarchy does not contain a root element with that name.

```
{'_id': ObjectId('617953191b814c4c150bddd4'),
  'person_id': 1,
  'hello': 'world'
]

```

### Connecting to Mongo

#### Standalong Mongo instance

The example below illustrates how one can build a connection to Mongo. First, we build a MongoConnection, and the following are the inputs:

1. The first field is the *username* in our example below this is **admin**
2. 
2. The second field is the *password* in our example below this is **jasonrocks**
3. 
3. The third field is the *mongodb connection url* in our example below this is **172.17.0.1:27017/admin**. This means that the user is connecting to the Mongo instance on:

    a. The host with IP address *mongodb*

    b. Port 27017

    c. The database in Mongo used for validating authentication. The default is admin, as above, but in your setup this could be anything.

4. The [optional] fourth argument is the authentication source. By default we authenticate using the standard Mongo authentication source (admin). For more details on authentication sources see [this link](https://docs.mongodb.com/manual/core/authentication-mechanisms/).


```
from rgsync.Connectors import MongoConnector, MongoConnection
connection = MongoConnection('admin', 'adminpassword', '172.17.0.1:27017/admin')
jConnector = MongoConnector(connection, 'yourmongodbname', 'persons', 'person_id')
```

#### Connecting to a cluster

The cluster connection is similar to standalone, except that the MongoConnection object must be initialized differently. *None*s must be passed in for both the username and password, and a **mongodb://** style connection string specified using a variable named *conn_string*. Note: the database must be specified in this instance, as the Connector, still needs to create a connection to the database

```

from rgsync.Connectors import MongoConnector, MongoConnection
db = 'yourmongodbname'
connection = MongoConnection(None, None, db, conn_string='mongodb://172.17.0.1:27017,172.17.0.5:27017,172.17.0.9:27017')
jConnector = MongoConnector(connection, db, 'persons', 'person_id')
```

## Examples

### Gears Recipe for a single write behind

This example replicates all data written to Redis whose key is named *person:<something>*, to the Mongo collection named *persons*. The collection name is specified in the instantiation of the MongoConnector below.

```
from rgsync import RGJSONWriteBehind, RGJSONWriteThrough
from rgsync.Connectors import MongoConnector, MongoConnection

connection = MongoConnection('admin', 'adminpassword', '172.17.0.1:27017/admin')
db = 'yourmongodbname'

personConnector = MongoConnector(connection, db, 'persons', 'person_id')


RGJSONWriteBehind(GB,  keysPrefix='person',
              connector=personConnector, name='PersonsWriteBehind',
              version='99.99.99')

RGJSONWriteThrough(GB, keysPrefix='__', connector=personConnector,
                   name='PersonJSONWriteThrough', version='99.99.99')
```

### Gears recipe writing to multiple collections

This example recipe builds on the previous case,  and introduces as second replication recipe. In this example, anything stored in Redis under the key *person:<some key>* (eg: person:1, person:15) will be replicated to the *persons* collection in Mongo. Anything written to Redis, and stored under the key  *thing:<some other key>* (eg: thing:42, thing:450) will be replicated to the *things* collection in Mongo.

```
from rgsync import RGJSONWriteBehind, RGJSONWriteThrough
from rgsync.Connectors import MongoConnector, MongoConnection

connection = MongoConnection('admin', 'adminpassword', '172.17.0.1:27017/admin')
db = 'yourmongodbname'

personConnector = MongoConnector(connection, db, 'persons', 'person_id')

RGJSONWriteBehind(GB,  keysPrefix='person',
              connector=personConnector, name='PersonsWriteBehind',
              version='99.99.99')

RGJSONWriteThrough(GB, keysPrefix='__', connector=personConnector,
                   name='PersonJSONWriteThrough', version='99.99.99')

thingConnector = MongoConnector(connection, db, 'things', 'thing_id')
RGJSONWriteBehind(GB,  keysPrefix='thing',
              connector=thingConnector, name='ThingWriteBehind',
              version='99.99.99')

RGJSONWriteThrough(GB, keysPrefix='__', connector=thingConnector,
                   name='ThingJSONWriteThrough', version='99.99.99')
```

