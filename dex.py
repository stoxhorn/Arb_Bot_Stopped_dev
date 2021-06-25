# this class is used to fetch data from Dexes and pools
import json
import web3
from time import time
from solc import compile_standard
from web3 import Web3
import threading
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes as hb
from datetime import datetime
from time import ctime
from copy import deepcopy

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from contract_handler import SC_handler
    


class Dex:
    
    def __init__(self, w3_object, dex_ticker, data, tokens):
        self.w3 = w3_object
        self.sc = SC_handler(w3_object)
        
        self.dex_ticker = dex_ticker

        router_data = data[0]
        factory_data = data[1]

        self.router_address = router_data[0]
        self.router_abi = router_data[1]


        self.factory_address = factory_data[0]
        self.factory_abi = factory_data[1]


        tup = self.sc.create_SC_tup(self.router_abi, self.router_address)
        self.router_sc = tup[0]
        self.router_abi = tup[1]

        tup = self.sc.create_SC_tup(self.factory_abi, self.factory_address)
        self.factory_sc = tup[0]
        self.factory_abi = tup[1]

        self.factory = {'address': self.factory_address, 'abi': self.factory_abi, 'sc': self.factory_sc}
        self.router = {'address': self.router_address, 'abi': self.router_abi, 'sc': self.router_sc}

        self.tokens = tokens
        
        self.pools = self.get_all_pools()
        

    def get_all_prices(self):
        prices = {}
        for pool in self.pools:
            token_tickers = pool.split('-')
            token1 = token_tickers[0]
            token2 = token_tickers[1]

            prices[pool] = self.get_pair_price(token1, token2)
        return prices

    def get_pair_price(self, token1, token2):
        '''
        Input is to be given as a string denoting the token ticker
        returns price of token1/token2
        '''
        print(token1)
        print(token2)
        token1 = self.tokens[token1]
        token2 = self.tokens[token2]

        pool_address = self.get_pool_address(token1.get_ticker(), token2.get_ticker())
        
        print(pool_address)
        balance1 = token1.get_sc().functions.balanceOf(pool_address).call()
        balance2 = token2.get_sc().functions.balanceOf(pool_address).call()
        
        balance1 = balance1/token1.get_deci_ratio()
        balance2 = balance2/token2.get_deci_ratio()

        return balance2/balance1

    def get_pool_address(self, token1, token2):
        '''
        Takes token ticker as arguments
        '''
        res = ''
        key1 = token1 + '-' + token2
        key2 = token2 + '-' + token1
        
        if key1 in self.pools:
            return self.pools[key1]
        elif key2 in self.pools:
            return self.pools[key2]
        else:
            return 'Errer'

# load
    def get_all_pools(self):
        '''
        Fetch and store addresses of all pools
        pools stored as token1-token2 in a dictionary
        '''
        pools = {}
        for token1 in self.tokens:
            token1_address = self.tokens[token1].get_address()
            for token2 in self.tokens:
                already_fetched = False
                if len(pools) > 0:
                    for i in pools:
                        if i == token1 + '-' + token2:
                            already_fetched = True
                            break
                        elif i == token2 + '-' + token1:
                            already_fetched = True
                            break
                        else:
                            pass
                else:
                    pass
                if not already_fetched:
                    token2_address = self.tokens[token2].get_address()
                    pool_address = self.factory_sc.functions.getPair(token1_address, token2_address).call()
                    pools[token1 + '-' + token2] = pool_address
                else:
                    pass
        pop_list = []
        for i in pools:
            if pools[i] == '0x0000000000000000000000000000000000000000':
                pop_list.append(i)
            else:
                pass
        for i in pop_list:
            pools.pop(i)
        return pools

# getters
    def get_ticker(self):
        return deepcopy(self.dex_ticker)

    def get_factory(self):
        return deepcopy(self.factory)
    
    def get_factory_address(self):
        return deepcopy(self.factory_address)
    
    def get_factory_abi(self):
        return deepcopy(self.factory_abi)

    def get_factory_sc(self):
        return deepcopy(self.factory_sc)
    
    def get_router(self):
        return deepcopy(self.router)
    
    def get_router_address(self):
        return deepcopy(self.router_address)
    
    def get_router_abi(self):
        return deepcopy(self.router_abi)

    def get_router_sc(self):
        return deepcopy(self.router_sc)
        