from web3 import Web3

class JoeV2Helper:
    #获得当前x兑换y的价格
    def get_price(_w3:Web3,_address_pair,_abi_pair,_decimal_x,_decimal_y):
        bin_step=_w3.eth.contract(address=_address_pair,abi=_abi_pair).functions.getBinStep().call()
        s=bin_step/10000
        id=_w3.eth.contract(address=_address_pair,abi=_abi_pair).functions.getActiveId().call()
        price=pow((1+s),id-pow(2,23))*pow(10,_decimal_x)/pow(10,_decimal_y)
        return price
