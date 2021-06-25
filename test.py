# idea is to test various stuff here
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
    from main import Bot
    from install import Install

class Test:
    def __init__(self):
        self.bot = Bot()
        self.fetch = self.bot.fetch
    
    def test_pair_price(self):
        tok1 = 'USDC'
        tok2 = 'wMATIC'
        print(str(self.fetch.get_dex('QS').get_pair_price(tok1, tok2 )) + ' ' + tok1 + ' per ' + tok2)

    def test_get_prices(self):
        tok1 = 'USDC'
        tok2 = 'wMATIC'
        list = self.fetch.get_prices(tok1, tok2)
        print(list[0][1]/list[1][1])
        for i in list:
            print(i[0] + ' has price: ' + str(i[1]) + ' '  + tok1 + ' per ' + tok2)

    def test_compare_prices(self):
        tok1 = 'USDC'
        tok2 = 'wMATIC'
        print(self.fetch.compare_prices(tok1, tok2))

    def test_price_loop(self):
        tok1 = 'USDC'
        tok2 = 'wMATIC'
        self.bot.price_loop(tok1, tok2)

    def test_get_all_prices(self):
        tok1 = 'USDC'
        tok2 = 'wMATIC'
        self.fetch.get_all_prices()

def fresh():
    ins = Install()
    ins.write_files()

def main():
    fresh()
    t = Test()
    t.test_get_all_prices()



if __name__ == "__main__":
    main()
