import json
import web3
import time
from solc import compile_standard
from web3 import Web3
import threading
from web3.middleware import geth_poa_middleware
from hexbytes import HexBytes as hb
from datetime import datetime
from time import ctime
from copy import copy

class My_token:

    def __init__(self, ticker, address, abi, sc):
        self.ticker = ticker
        self.address = address
        self.abi = abi
        self.sc = sc
        self.decimals = self.calc_decimals()
        self.deci_ratio = 10 ** self.decimals

    def calc_decimals(self):
        return self.sc.functions.decimals().call()

    def get_deci_ratio(self):
        return copy(self.deci_ratio)

    def get_decimals(self):
        return copy(self.decimals)

    def get_ticker(self):
        return copy(self.ticker)
    
    def get_address(self):
        return copy(self.address)

    def get_abi(self):
        return copy(self.abi)

    def get_sc(self):
        return copy(self.sc)


    