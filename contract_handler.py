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
import copy

class SC_handler:

    def __init__(self, w3):
        self.w3 = w3

    def create_SC(self, abi, address):
        return self.w3.eth.contract(abi = abi, address = address)
    
    def load_abi(self, file_str):
        '''
        returns the ABI stored at location file_str 
        '''
        PCS_abi = None

        with open(file_str) as jsonF:
            PCS_abi = json.load(jsonF)
        return PCS_abi

    def create_SC_tup(self, file_str, address):
        '''
        Takes a file string and an address as argument
        file_str is the file address for the ABI object corresponding to the address given
        returns the contract created and the ABI loaded
        [SC, abi]
        '''
        # Loads the ABI interface for pancakeswap
        abi = self.load_abi(file_str)

        # Constructs the PCS contract from the given ABI
        return (self.w3.eth.contract(abi = abi, address = address), abi)
