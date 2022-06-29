# oracle
API which periodically fetches price data from Coingeckco, and Binance, then conditionally stores in Redis.  

# Objectives
- []
- []
- [] ...

# Notice
This repo is a work in progress. A snapshot has been made to branch `snapshot`.  

# Rationale
## DB: Redis
Constrin: easy to dev  
RDBMS, too complex for this project.  
NOSQL, yes, two choice, Mongo, or Redis.  
Redis: Fast, easy, good for caching, fetching, storing JSON.  
Mongo: all of about just not as fast.
## API: FastAPI
Constrain: No need to write data  
FastAPI: Fast dev, Fast response, modular, defining schemas optional.  
## Scheduler: Python APS
Constrain: Background job scheduler, simple to implement  
Python APS: only one that fit the requirement  
ZeroMQ: also works, but requries more complex/ elaborate setup  
## Usage
### Local

Spin up redis
```
cd redis
docker compose up --build --force-recreate
```
Start fetcher
```
pipenv run python fetcher.py

```
Start apiserver
```
pipenv run uvicorn server:app --port 8888
```
