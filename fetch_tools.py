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
from copy import copy

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from my_token import My_token
    from dex import Dex
    from contract_handler import SC_handler

class Fetch_tools:
        # address = Web3.toChecksumAddress('')
        
    def __init__(self, key, address, network):
        # Loads real or test network of BSC
        self.network = network + '_data'

        self.w3 = self.load_w3()
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.sc = SC_handler(self.w3)
        
        # value of own private metamask keyu
        self.key = key
        
        # address of own wallet
        self.address = Web3.toChecksumAddress(address)

        # load data for tokens and dexes
        self.dexes = self.load_dic(self.network + '/dexes.txt')
        
        # This also loads ABI from a token on test network
        self.test_token_abi = self.sc.load_abi('json/test_token_abi.json')
        
        # loads pool abi, assumed all pool abi is similar
        # atm i don't need pool ABI for anything
        self.pool_abi = self.sc.load_abi('json/pool_abi.json')
        self.tokens = self.create_token_contracts()
        
        self.dexes = self.load_dex_data()

        # creates the dictionary containing the tokens
        
    def compare_prices(self, token1, token2):
        return self.get_prices(token1, token2) 

    def get_all_prices(self):
        for dex in self.dexes:
            self.dexes[dex].get_all_prices()

    def get_prices(self, token1, token2):
        prices = []
        for dex in self.dexes:
            dex_obj = self.get_dex(dex)
            prices.append((dex, dex_obj.get_pair_price(token1, token2)))
        return prices

# getters and setters
    def get_dex_object(self, dex, object_type):
        return self.dex_dic[dex][object_type]

    def get_dex(self, dex):
        return copy(self.dexes[dex])

# Load functions

    def load_dex_data(self):
        '''
        instantiating a dex requires necessary data
        Data is formatted as:
        [router_data, factory_data]
        
        router_data and factory_data is formatted as:
        [address, abi_str]
        '''
        
        data = self.load_dic(self.network + '/dex_data.txt', False)
        for dex in data:
            list = []
            for entry in data[dex]:
                l = entry.split(',')
                address = self.dexes[dex + '_' + l[1]]
                abi_str = l[0]
                list.append((address, abi_str))
            data[dex] = list

        dexes = {}
        for dex in data:
            dexes[dex] = Dex(self.w3, dex, data[dex], self.tokens)
        
        return dexes
            

    def create_token_contracts(self):
        '''
        Function creating the contracts for all tokens tracked
        Thus i won't need to create them everytime i need to update price
        data is stored as tuples of 2 entires
        [address, SC]
        '''
        tokens = self.load_dic(self.network + '/tokens.txt')
        new_dic = {}
        for i in tokens:
            # Creates a new token object for each entry
            # tokens[i] is the address of token i
            new_dic[i] = My_token(i, tokens[i], self.test_token_abi, self.sc.create_SC(self.test_token_abi, tokens[i]))
        
        return new_dic
    
    def load_dic(self, file_str, check = True):
        '''
        Loads dic data stored in file_str
        Key and data seperated by a '-', one line per entry
        Stored as a dictionary, which is used as return data
        '''
        dic = {}
        with open(file_str) as f:
            for i in f:
                l = i.split('-')
                l[1] = l[1]
                if check:
                    dic[l[0]] = Web3.toChecksumAddress(l[1][:-1])
                else:
                    dic[l[0]] = (l[1], l[2][:-1])
        return dic
     
    def load_w3(self):
        '''
        initializes the web3 object
        will load testnetwork, if specified
        '''
        #Web3(Web3.WebsocketProvider())
        #polygon_quicknode_wss = 'wss://crimson-red-snowflake.matic.quiknode.pro/38b6e627d7236e2f4187ff9e385de21082177532/'
        polygon_quicknode_HTTP = 'https://crimson-red-snowflake.matic.quiknode.pro/38b6e627d7236e2f4187ff9e385de21082177532/'
        bsc_quicknode_HTTP = 'https://billowing-muddy-glade.bsc.quiknode.pro/0c1d1395d189ab42e9a03901bed0ff61a6b9e774/'
        bsc_quicknode_wss = 'wss://billowing-muddy-glade.bsc.quiknode.pro/0c1d1395d189ab42e9a03901bed0ff61a6b9e774/'
        if self.network == 'BSC_data':
            return Web3(Web3.HTTPProvider(bsc_quicknode_HTTP)) # Web3(Web3.WebsocketProvider(polygon_quicknode_wss)) #
        elif self.network == 'POLY_data':
            return Web3(Web3.HTTPProvider(polygon_quicknode_HTTP)) # Web3(Web3.WebsocketProvider(polygon_quicknode_wss)) #


