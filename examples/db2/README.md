# Set up IBM DB2 DB

## Setup IBM DB2 docker
This will bring up a IBM DB2 database test with the sample user.  Change user and password in docker-compose.yml file

### choose a DB2 compatible tool
one option is RazorSQL
#### download RazorSQL and install using the instruction on top right of [this page](https://razorsql.com)
```bash
docker-compose up -d
```
###  make sure db2 instance is ready
```bash
docker logs db2 
```
#### Connect to DB2 with RazorSQL with following parameters
Click the necessary *Continue* and *CONNECT* buttons along the way
| Parameter               | Value                    |
|-------------------------|--------------------------|
| Database Type           | DB2                      |
| Connection Type         | Keep Default of Type 4   |
| Connection Profile Name | DB2 Docker Sample        |
| Login                   | db2inst1                 |
| Password                | jasonrocks               |
| Save Password Checkbox  | (easier if you check it) |
| Host                    | localhost                |
| Port                    | 50000                    |
| Database Name           | SAMPLE                   |


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
## Running the recipe
```bash
gears-cli run --host 127.0.0.1 --port 6379 sample.py --requirements requirements.txt
```

## Test
Using redis-cli perform:
```bash
 docker exec -it redis redis-cli hset emp:11 first WILLIAM last SMITH middle H education 9
```

Make sure data reached IBM Db2:
* Connect using the *DB2 Docker Sample* connection
* Under *Schemas*, open the *DB2INST1* folder
* Under *DB2INST1* open the *Tables* folder and right-click on the *EMPLOYEE* folder
* choose *Generate SQL* and *SELECT*
* running this generated select statement will show the row inserted from the hset command

