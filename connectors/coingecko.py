from pycoingecko import CoinGeckoAPI
import time
from copy import deepcopy

cg = CoinGeckoAPI()

D_SYM_CONV = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'AVAX': 'avalanche-2',
}

D_SYM_CONV_CG = {
    'bitcoin': 'BTC',
    'ethereum': 'ETH',
    'avalanche-2': 'AVAX',
}

def conv_dict_key(d: dict) -> dict:
    ret = {}
    for k, v in d.items():
        if D_SYM_CONV_CG.get(k, None):
            ret[D_SYM_CONV_CG[k]] = v
    ret['ts'] = d['ts']

    return ret

def get_price(l_symbols: list[str], vs_currencies: str = 'usd') -> dict:
    d = cg.get_price(ids=[D_SYM_CONV[i] for i in l_symbols], vs_currencies=vs_currencies)
    ret = {}
    for k, v in d.items():
        ret[k] = float(v[vs_currencies])
    ret['ts'] = time.time()

    return ret
