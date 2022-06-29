from rich import inspect
from connectors import coingecko
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import redis
from redis.commands.json.path import Path
from console import console

# constants
L_SYMBOLS = ['BTC', 'ETH', 'AVAX']

# init jop sched.
scheduler = BackgroundScheduler()
# init redis
rdb = redis.Redis(host='localhost', port=6379, password='foobared')
# rdb.set('someKey','someVal')


def job():
    """
    Fetch data from coingecko then stores in redis
    """
    dct_cg_price = coingecko.get_price(L_SYMBOLS)
    dct_cg_price = coingecko.conv_dict_key(dct_cg_price)

    if not rdb.json().set('someKey', Path.root_path(), dct_cg_price):
        console.print('Error: at ...')
    # store in redis


job = scheduler.add_job(job, 'interval', seconds=3)

scheduler.start()

while True:
    sleep(0.1)
