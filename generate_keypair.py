from algosdk import account, mnemonic


def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

# Write down the address, private key, and the passphrase for later usage
generate_algorand_keypair()

# My address: WTHK6QHZ4KFVCNQMKRZYOZS6DNHOTOMJ2SWMG5GALDM524GPX5I47PEWWA
# My private key: VedAn/NvJCX54mDaY64+0d2Apyz1JOTBELoINsyGkOe0zq9A+eKLUTYMVHOHZl4bTum5idSsw3TAWNndcM+/UQ==
# My passphrase: turkey adjust soul you emotion enable blind genius kitten ridge palm tackle accuse clarify practice ceiling develop drink fringe gauge observe canvas develop abstract company

# My address: XKA3XZZT5RVEJZQWXKUDUXAZUH4OB3BF4TBVPYOXSGTWZ3NVCPBPMGJOXY
# My private key: cKdZ8jdCrmlY6cxfvtHO+8xra+pIDPZaiIdcIiIlJhW6gbvnM+xqROYWuqg6XBmh+ODsJeTDV+HXkads7bUTwg==
# My passphrase: unlock grief weird casino frame bounce enlist smooth slogan eight trash soul stuff onion elder arrange gain cannon duck chair dust matter powder abandon fashion

# My address: WQHTQTJCCHU7BOYH2XAVQWISUYH2GUJTRWD4EIHPNWI3IAIH26BJ4W4F4U
# My private key: U3po4myq446xTOR6tFk1m3iBMsMFonWH2zIGmbaJDue0DzhNIhHp8LsH1cFYWRKmD6NRM42HwiDvbZG0AQfXgg==
# My passphrase: engine peanut illness plug shrug glove grain tone monster grocery one meadow actual smile come pear upgrade host bonus motor honey pen debris abstract spawn