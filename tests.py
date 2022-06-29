from rich import inspect
import rich
from connectors import coingecko
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import redis
from redis.commands.json.path import Path


# constants
L_SYMBOLS = ['BTC', 'ETH', 'AVAX']

# init jop sched.
# scheduler = BackgroundScheduler()
# init redis
# rdb = redis.Redis(host='localhost', port=6379, password='foobared')
# rdb.set('someKey','someVal')


def job():
    """
    Fetch data from coingecko then stores in redis
    """
    dct_price = coingecko.get_price(L_SYMBOLS)
    rich.print(coingecko.conv_dict_key(dct_price))


    # rdb.json().set('someKey', Path.root_path(), dct_price)
    # store in redis


# job = scheduler.add_job(job, 'interval', seconds=3)

# scheduler.start()

# while True:
#     sleep(0.1)


job()
