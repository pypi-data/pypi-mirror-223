from web3 import Web3

class Synapse:

    chain_id_dfk=53935
    chain_id_klay=8217


    def depositETH(_web3:Web3,_contract_address,_contract_abi,_to_chain_id,_amount,_public_key,_private_key):
        l1_bridge_zap_contract=_web3.eth.contract(address=_contract_address, abi=_contract_abi)
        nonce=_web3.eth.get_transaction_count(_public_key)
        deposit_ETH_function=l1_bridge_zap_contract.functions.depositETH(_public_key,_to_chain_id,_amount)
        tx_params={
            'from': _public_key,
            'value': _amount,
            'nonce': nonce,
            'type': '0x2'
        }
        transaction=deposit_ETH_function.buildTransaction(tx_params)
        signed_transaction=_web3.eth.account.sign_transaction(transaction, private_key=_private_key)
        return _web3.toHex(_web3.eth.send_raw_transaction(signed_transaction.rawTransaction))
    
    def redeem(_web3:Web3,_contract_address,_contract_abi,_to_chain_id,_token,_amount,_public_key,_private_key):
        bridge_zap_contract=_web3.eth.contract(address=_contract_address, abi=_contract_abi)
        nonce=_web3.eth.get_transaction_count(_public_key)
        redeem_function=bridge_zap_contract.functions.redeem(_public_key,_to_chain_id,_token,_amount)
        tx_params={
            'from': _public_key,
            'value': 0,
            'nonce': nonce,
            'type': '0x2'
        }
        transaction=redeem_function.buildTransaction(tx_params)
        signed_transaction=_web3.eth.account.sign_transaction(transaction, private_key=_private_key)
        return _web3.toHex(_web3.eth.send_raw_transaction(signed_transaction.rawTransaction))