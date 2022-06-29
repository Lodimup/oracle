from rich import inspect
from connectors import (
    coingecko,
    binance
)
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import time
import redis
from redis.commands.json.path import Path
from console import console

# constants
DEBUG = True
DELAY_CHK = 5  # minutes
JOB_INTERVAL = 30 # seconds
L_SYMBOLS = ['BTC', 'ETH', 'AVAX']

console.log('Oracle started...')

scheduler = BackgroundScheduler() # init jop sched.
# should be loaded from .env, import os, os.getenv etc...
rdb = redis.Redis(host='localhost', port=6379, password='foobared') # init redis

def fetch_median_price() -> dict:
    """
    Fetch price from connectors, it is only done
    Could be made to fetch in parallel using threading,
    in this case only two API calls are made so it does not really matter
    """
    if DEBUG: console.log('Fetching Coingecko')
    dct_cg_price = coingecko.get_price(L_SYMBOLS)
    dct_cg_price = coingecko.conv_dict_key(dct_cg_price) # convert price to standard dict keys
    if DEBUG: console.log(dct_cg_price)

    if DEBUG: console.log('Fetching Binance')
    dct_bn_price = binance.get_price(L_SYMBOLS)
    if DEBUG: console.log(dct_bn_price)

    # Create dict with median price
    dct_median_price = {}
    for symbol in L_SYMBOLS:
        dct_median_price[symbol] = (dct_cg_price[symbol] + dct_bn_price[symbol]) / 2
    dct_median_price['ts'] = time.time()
    if DEBUG:
        console.log('median price')
        console.log(dct_median_price)

    return dct_median_price

def job() -> bool:
    """
    Fetch data from coingecko/binance then stores in redis.
    Returns: True if successful, False otherwise.
    """
    console.print('-'*20, 'job started', '-'*20)

    # Fetch price from db
    db_price = rdb.json().get('price:agg', Path.root_path())
    if DEBUG: console.log('db_price:', db_price)

    # Check if price in the db is delayed by more than 5 minutes, or does not exist
    # Only continue is data is delayed by 5 minutes, or does not exist, because fetching data from coingecko/binance is slow
    if not db_price:
        if DEBUG: console.log('db_price does not exist.')
        rdb.json().set('price:agg', Path.root_path(), fetch_median_price())
        db_price = rdb.json().get('price:agg', Path.root_path())
        return True

    if not (time.time() - db_price['ts']) > DELAY_CHK * 60:
        if DEBUG:
            retry_in = DELAY_CHK * 60 - (time.time() - db_price['ts'])
            console.log(f'db_price is still considered fresh, {DELAY_CHK} minutes, skipping job.\nTry again in {retry_in:.0f}s.')
        return False

    # Create dict with median price
    dct_median_price = fetch_median_price()

    # Check if median price differs from val in db for more than 0.1%
    for symbol in L_SYMBOLS:
        diff = abs(1 - dct_median_price[symbol] / db_price[symbol])
        if diff > 0.1 / 100:
            if DEBUG:
                console.log(f'{symbol=} {diff=}, will commence transaction.')
            break
        if DEBUG: console.log(f'All entries no diff > 0.1% , will skip transaction.')
        return False

    # Store price in db
    if not rdb.json().set('price:agg', Path.root_path(), dct_median_price):
        console.log('ERR: price transaction failed')
        return False
    console.log(f'Price transaction success.\n{dct_median_price}')

    return True


def main():
    job()  # start one job immediately
    j = scheduler.add_job(job, 'interval', seconds=JOB_INTERVAL)
    scheduler.start()

    while True:
        sleep(0.1)


if __name__ == '__main__':
    main()
