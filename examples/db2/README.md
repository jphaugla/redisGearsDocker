# Set up IBM DB2 DB

## Setup IBM DB2 docker
This will bring up a IBM DB2 database test with the sample user.  Change user and password in docker-compose.yml file

```bash
docker-compose up -d
```
###  make sure db2 instance is ready
```bash
docker logs db2 
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
## Running the recipe
```bash
gears-cli run --host 127.0.0.1 --port 6379 example.py --requirements requirements.txt
```

## Test
Using redis-cli perform:
```bash
 docker exec -it redis redis-cli hset person:1 first_name foo last_name bar age 20
```

Make sure data reached postgres server:
* Click on select Employee on left pane at the bottom
* the data from the hset in redis-cli will be visible in the db2 EMPLOYEE table
