# oracle
API which periodically fetches price data from Coingeckco, and Binance, then conditionally stores in Redis.  

The program is separated into two services:  
fetcher.py for fetching and storing data
server.py for serving API /latest

# Objectives
- [x] fetch binance price
- [x] fetch coingeco price
- [x] calc median
- [x] do not transact if data stale cond. not met
- [x] do not transact if any calc'd data diff cond. not met
- [x] endpoint exposed

# Notice
A snapshot has been made to branch `snapshot`.  
I normally do not log debug this much, it is for your ease of debugging  
server addr, password, should be loaded using
```
import os
from dotenv import load_dotenv

load_dotenv()
... = os.getenv('...')
```
but opted out for the sake of simplicity in testing.
Sane options can be configured in fetcher.py constants.  
Function pattern:
```
def func():
  guard
  body
  default
```
# Rationale
## Separating server.py, fetcher.py
Simply micro-service pattern. Each service should only do one thing.
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
Use env manager of your choice
```
pipenv install
```
Start fetcher
```
pipenv run python fetcher.py

```
Start apiserver
```
pipenv run uvicorn server:app --port 8888
```
Access at:
http://127.0.0.1:8888/latest
