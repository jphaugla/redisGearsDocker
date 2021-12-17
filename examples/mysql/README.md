# Set up MySql DB

## Setup MySql docker
This will bring up a mysql database test with a root user and a demo user.  Change user and password in docker-compose.yml file

```bash
docker-compose up -d
```

## Create Persons table
* Log into adminer using following URL in your browser
[http://localhost:8080
](http://localhost:8080)

| Prompt   | Value      |
|----------|------------|
| System   | Mysql      |
| Server   | mysql      |
| Username | root       |
| Password | jasonrocks |
| Database | test       |

* Click on "SQL Command"
* Copy Create Table statement into the SQL command window
```bash
CREATE TABLE test.persons (person_id VARCHAR(100) NOT NULL, first VARCHAR(100) NOT NULL, last VARCHAR(100) NOT NULL, age INT NOT NULL, PRIMARY KEY (person_id));
```
* Click Execute in Adminer to create the table
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
# Running the recipe
```bash
gears-cli run --host 127.0.0.1 --port 6379 example.py --requirements requirements.txt
```

# Test
Using redis-cli perform:
```bash
 docker exec -it redis redis-cli hset person:1 first_name foo last_name bar age 20
```

Make sure data reached MySql server:
* Log into adminer using following URL in your browser 
[http://localhost:8080
](http://localhost:8080)

| Prompt   | Value      |
|----------|------------|
| System   | Mysql      |
| Server   | mysql      |
| Username | root       |
| Password | jasonrocks |
| Database | test       |
* Click on select persons on left pane at the bottom
* the data from the hset in redis-cli will be visible in the mysql persons table
