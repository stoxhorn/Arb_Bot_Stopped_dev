# Idea is to run the bot from this file
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
import copy

if __package__ is None or __package__ == '':
    # uses current directory visibility
    from fetch_tools import Fetch_tools

class Bot:
    def __init__(self):
        data = self.read_user()
        self.address = Web3.toChecksumAddress(data[0])
        self.key = data[1]
        self.fetch = Fetch_tools(self.key, self.address, 'BSC')

    def get_all_ratios(self):
        '''
        Fetches all prices and calculates the ratios between all tokens
        '''
        prices = self.fetch.get_all_prices()
        


    def price_loop(self, token1, token2):
        loop_bool = True
        prices = None
        dex = ''
        while(loop_bool):
            prices = self.fetch.compare_prices(token1,token2)
            ratio = (abs(1 - prices[0][1]/prices[1][1]))
            ratio = ratio * 100
            if ratio > 0.3:
                # Find the exchange with the cheapest price
                min = 0
                for i in prices:
                    if min == 0:
                        min = i[1]
                        dex = i[0]
                    elif i[1] < min:
                        min = i[1]
                        dex = i[0]
                    else:
                        pass
                break
            else:
                pass
        

# ----- functions reading txt file for user-data
    '''
    Reads user_data.txt for key, address and gas price
    returns a list of different data
    [address, key, BSC gas price, POLY gas price]
    '''
    def read_user(self):
        data = [None, None, None, None]
        with open('POLY_data/user_data.txt') as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == '#':
                    pass
                else:
                    if line[:7] == 'address':
                        data[0] = line[10:-1]
                    elif line[:3] == 'key':
                        data[1] = line[6:-1]
                    elif line[:13] == 'BSC gas price':
                        data[2] = line[16:-1]
                    elif line[:14] == 'POLY gas price':
                        data[3] = line[17:-1]
                    else:
                        pass
        return data

def main():
    pass


if __name__ == "__main__":
    main()
