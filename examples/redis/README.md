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
## Run the recipe
For example, run the sample [redis](example-redis-standalone.py) recipe (contains the mapping of primary DB Redis Hashes with secondary DB Redis Hashes and RedisGears registrations) and install its dependencies with the following command:

```bash
gears-cli run --host 127.0.0.1 --port 6379 example-redis-standalone.py --requirements requirements.txt
```
NOTE:   This recipe is installed into the redis1 docker container running on port 6379 and it connects to the redis2 docker container running on port 9001 

NOTE:	Exactly once property is not valid for Redis cluster, because Redis cluster do not support transaction over multiple shards.

## Test
Using redis-cli perform:
```bash
redis-cli
127.0.0.1:6379> hset key:1 bin1 1 bin2 2 bin3 3 bin4 4 bin5 5
(integer) 5
```

Make sure data reached the second Redis server:
```bash
redis-cli -p 9001
127.0.0.1:9001> hgetall key:1
 1) "bin1"
 2) "1"
 3) "bin2"
 4) "2"
 5) "bin4"
 6) "4"
 7) "bin3"
 8) "3"
 9) "bin5"
10) "5"
```
