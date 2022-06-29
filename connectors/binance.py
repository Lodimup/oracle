from binance import Client
import pandas as pd
import time

client = Client()

def get_price(l_symbols: list[str], l_vs_symbols: list[str] = ['USDC', 'USDT']) -> dict:
    """
    WARN: Binance does not have price against fiat, only against stable tokens.
    Returns price of token symbol against another token symbols.
    If a symbol against does not exist, fallback to
    """
    d = client.get_all_tickers()
    df = pd.DataFrame(d).set_index('symbol')  # against a large amount of data DataFrame is faster
    ret = {}
    for symbol in l_symbols: # TODO: optimization opportunity using df.transpose()[['pair2', 'pair2']]
        for vs_symbol in l_vs_symbols:
            try:
                ret[f'{symbol}'] = float(df.loc[f'{symbol}{vs_symbol}', 'price'])
                break
            except KeyError:
                continue

    ret['ts'] = time.time()

    return ret
