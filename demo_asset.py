from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, wait_for_confirmation
from algosdk.mnemonic import to_private_key
import json

algod_address = "https://testnet-api.algonode.cloud"
algod_client = algod.AlgodClient("", algod_address)

def create_asset(asset_creator_address, private_key):
    
    params = algod_client.suggested_params()

    txn = AssetConfigTxn(
    sender=asset_creator_address,
    sp=params,
    total=1000,
    default_frozen=False,
    unit_name="ENALGO",
    asset_name="enalgo",
    manager=asset_creator_address,
    reserve=asset_creator_address,
    freeze=asset_creator_address,
    clawback=asset_creator_address,
    url="https://path/to/my/asset/details", 
    decimals=0)

    # Sign with secret key of creator
    stxn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)
        # Retrieve the asset ID of the newly created asset by first
        # ensuring that the creation transaction was confirmed,
        # then grabbing the asset id from the transaction.
    
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))

# asset_creator_address = "WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA"
# passphrase = "turkey adjust soul you emotion enable blind genius kitten ridge palm tackle accuse clarify practice ceiling develop drink fringe gauge observe canvas develop abstract company"
# private_key = to_private_key(passphrase)
#create_asset(asset_creator_address, private_key) # "asset-index": 149398609

def update_asset(asset_id, asset_creator_address, asset_new_manager_address, private_key):
    # CHANGE MANAGER
    # The current manager(Account 2) issues an asset configuration transaction that assigns Account 1 as the new manager.
    # Keep reserve, freeze, and clawback address same as before, i.e. account 2
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetConfigTxn(
        sender=asset_creator_address,
        sp=params,
        index=asset_id, 
        manager=asset_creator_address,
        reserve=asset_new_manager_address,
        freeze=asset_new_manager_address,
        clawback=asset_new_manager_address)
    # sign by the current manager - Account 2
    stxn = txn.sign(private_key)
    # txid = algod_client.send_transaction(stxn)
    # print(txid)
    # Wait for the transaction to be confirmed
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)
    # Check asset info to view change in management. manager should now be account 1
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

# asset_creator_address = "WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA"
# passphrase = "turkey adjust soul you emotion enable blind genius kitten ridge palm tackle accuse clarify practice ceiling develop drink fringe gauge observe canvas develop abstract company"
# private_key = to_private_key(passphrase)
# asset_new_manager_address = "XKA3XZZT5RVEJZQWXKUDUXAZUH4OB3BF4TBVPYOXSGTWZ3NVCPBPMGJOXY"
# asset_id = 149398609
# # passphrase = "unlock grief weird casino frame bounce enlist smooth slogan eight trash soul stuff onion elder arrange gain cannon duck chair dust matter powder abandon fashion"
# # new_manager_private_key = to_private_key(passphrase)
# update_asset(asset_id, asset_creator_address, asset_new_manager_address, private_key)

def opt_in(asset_id, account_address, private_key):
    # OPT-IN
    # Check if asset_id is in account 3's asset holdings prior
    # to opt-in
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    account_info = algod_client.account_info(account_address)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1    
        if (scrutinized_asset['asset-id'] == asset_id):
            holding = True
            break
    if not holding:
        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = AssetTransferTxn(
            sender=account_address,
            sp=params,
            receiver=account_address,
            amt=0,
            index=asset_id)

        stxn = txn.sign(private_key)
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
        except Exception as err:
            print(err)
        # Now check the asset holding for that account.
        # This should now show a holding with a balance of 0.
        print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

# account_address = "WQHTQTJCCHU7BOYH2XAVQWISUYH2GUJTRWD4EIHPNWI3IAIH26BJ4W4F4U"
# passphrase = "engine peanut illness plug shrug glove grain tone monster grocery one meadow actual smile come pear upgrade host bonus motor honey pen debris abstract spawn"
# private_key = to_private_key(passphrase)
# asset_id = 149398609
# opt_in(asset_id, account_address, private_key)

def transferring_asset(asset_id, from_address, from_address_private_key, to_address):
    # TRANSFER ASSET
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=from_address,
        sp=params,
        receiver=to_address,
        amt=10,
        index=asset_id)
    stxn = txn.sign(from_address_private_key)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)
    # The balance should now be 10.
    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))

# asset_id = 149398609
# from_address = "WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA"
# passphrase = "turkey adjust soul you emotion enable blind genius kitten ridge palm tackle accuse clarify practice ceiling develop drink fringe gauge observe canvas develop abstract company"
# from_address_private_key = to_private_key(passphrase)
# to_address = "WQHTQTJCCHU7BOYH2XAVQWISUYH2GUJTRWD4EIHPNWI3IAIH26BJ4W4F4U"
# transferring_asset(asset_id, from_address, from_address_private_key, to_address)

def retrive_created_assest_info(account, assetid):
    account_info = algod_client.account_info(account)
    idx = 0
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

def retrive_assest_info(account, assetid):
    account_info = algod_client.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

# asset_id = 149398609
# account_address = "WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA"
# retrive_assest_info(account_address, asset_id)

def destroy_asset(asset_id, account_address, private_key):
        # DESTROY ASSET
    # With all assets back in the creator's account,
    # the manager (Account 1) destroys the asset.
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    # Asset destroy transaction
    txn = AssetConfigTxn(
        sender=account_address,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
        )
    # Sign with secret key of creator
    stxn = txn.sign(private_key)
    # Send the transaction to the network and retrieve the txid.
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))     
    except Exception as err:
        print(err)
    # Asset was deleted.
    try:
        print("Account 3 must do a transaction for an amount of 0, " )
        print("with a close_assets_to to the creator account, to clear it from its accountholdings")
        print("For Account 1, nothing should print after this as the asset is destroyed on the creator account")    
        retrive_created_assest_info(account_address, asset_id)
        retrive_assest_info(account_address, asset_id)
        # asset_info = algod_client.asset_info(asset_id)
    except Exception as e:
        print(e)    


# asset_id = 149398609
# account_address = "WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA"
# passphrase = "turkey adjust soul you emotion enable blind genius kitten ridge palm tackle accuse clarify practice ceiling develop drink fringe gauge observe canvas develop abstract company"
# private_key = to_private_key(passphrase)
# destroy_asset(asset_id, account_address, private_key)