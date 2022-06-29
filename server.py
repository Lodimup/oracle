from fastapi import FastAPI
import redis
from redis.commands.json.path import Path

app = FastAPI()

@app.get("/latest")
async def root():
    # should be loaded from .env, import os, os.getenv etc...
    rdb = redis.Redis(host='localhost', port=6379, password='foobared')
    db_price = rdb.json().get('price:agg', Path.root_path())
    rdb.close()
    del db_price['ts']
    
    dct_resp = {}
    for k, v in db_price.items():
        dct_resp[k] = str(v)
    
    return {"prices": dct_resp}
