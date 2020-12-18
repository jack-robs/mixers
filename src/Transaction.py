# Transaction class
# used whenever a TX has to be made

import datetime, hashlib

class Transaction:

    def __init__(self):
        self.dtg = datetime.datetime
    
    def build_tx(self, sender, recv, amount):
        self.sent_from = sender
        self.sent_to = recv
        self.amount = amount
        sha = hashlib.sha256(sent_from + sent_to + val_str)
        self.last4_hash = sha[:-4]


    # TODO: logic in here to show it's been mixed
    # or other status codes?