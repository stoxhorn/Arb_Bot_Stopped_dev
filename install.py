
class Install:

    def __init__(self):
        self.started = True
        self.BSC_data_location = 'BSC_data/'
        self.POLY_data_location = 'POLY_data/'
        self.write_BSC()
        self.write_POLY()

    def write_BSC(self):
        self.BSC_usr_data_str = (self.BSC_data_location + 'user_data.txt', 
'''# Any lines with # in front will be ignored
# Be 100% sure there's at least one space between the = and the data behind it
# be 100% sure there's no spaces or any other characters after the data.
# an example for valid address data:
# address = 0x12345678912345678989
# nothing after the last 9
# your wallet's address
address = 

# your API key of your address, DON'T share this with anyone,
# or EVER type it into a machine you suspect could have a keylogger on it
key = 

# gas price is measured in gwei, same unit as left side in gas management in metamask
# please keep in mind this won't be the gas price paid to approve a token to sell
BSC gas price = 40
POLY gas price = 100

BSC wss node API =
BSC HTTP node API =

POLY wss node API =
POLY HTTP node API =
''')
        self.BSC_tokens_str = (self.BSC_data_location + 'tokens.txt',
'''wBNB-0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c
cake-0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82
bUSDC-0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d
BUSD-0xe9e7cea3dedca5984780bafc599bd69add087d56
MEE-0xe20a11175ee2392c9e2838221b2488d0f6a9680f
''')
        self.BSC_dex_str  = (self.BSC_data_location + 'dexes.txt', 
'''PCS_Router-0x10ED43C718714eb63d5aA57B78B54704E256024E
PCS_Factory-0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73
Sushi_Router-0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506
Sushi_Factory-0xc35dadb65012ec5796536bd9864ed8773abc74c4
''')

        self.BSC_dex_data_str = (self.BSC_data_location + 'dex_data.txt', 
'''PCS-json/PCS_abi.json,Router-json/PCS_factory_abi.json,Factory
Sushi-json/PCS_abi.json,Router-json/PCS_factory_abi.json,Factory
''')


    def write_POLY(self):
        self.POLY_usr_data_str = (self.POLY_data_location + 'user_data.txt', 
'''# Any lines with # in front will be ignored
# Be 100% sure there's at least one space between the = and the data behind it
# be 100% sure there's no spaces or any other characters after the data.
# an example for valid address data:
# address = 0x12345678912345678989
# nothing after the last 9
# your wallet's address
address = 

# your API key of your address, DON'T share this with anyone,
# or EVER type it into a machine you suspect could have a keylogger on it
key = 

# gas price is measured in gwei, same unit as left side in gas management in metamask
# please keep in mind this won't be the gas price paid to approve a token to sell
BSC gas price = 40
POLY gas price = 100

BSC wss node API =
BSC HTTP node API =

POLY wss node API =
POLY HTTP node API =
''')
        self.POLY_tokens_str = (self.POLY_data_location + 'tokens.txt',
'''wMATIC-0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270
USDC-0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
DAI-0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063
QUICK-0x831753DD7087CaC61aB5644b308642cc1c33Dc13
''')
        self.POLY_dex_str  = (self.POLY_data_location + 'dexes.txt', 
'''QS_Router-0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff
QS_Factory-0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32
Sushi_Router-0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506
Sushi_Factory-0xc35dadb65012ec5796536bd9864ed8773abc74c4
''')

        self.POLY_dex_data_str = (self.POLY_data_location + 'dex_data.txt', 
'''QS-json/QS_abi.json,Router-json/QS_factory_abi.json,Factory
Sushi-json/PCS_abi.json,Router-json/PCS_factory_abi.json,Factory
''')


    def write_file(self, tuple):
        file_name = tuple[0]
        data = tuple[1]
        file = open(file_name, 'w')
        file.write(data)
        file.close()
    
    def write_files(self):
        self.write_file(self.BSC_dex_str)
        self.write_file(self.BSC_tokens_str)
        self.write_file(self.BSC_usr_data_str)
        self.write_file(self.BSC_dex_data_str)

        self.write_file(self.POLY_dex_str)
        self.write_file(self.POLY_tokens_str)
        self.write_file(self.POLY_usr_data_str)
        self.write_file(self.POLY_dex_data_str)


def main():
    ins = Install()
    ins.write_files()

if __name__ == "__main__":
    main()