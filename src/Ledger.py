# Class Ledger, created and controled by Class: Router (non-networked), if JackPay is not a mixer
# controls reading/writing to ledger.csv

class Ledger:

    def __init__(self):
        self.ledger_name = 'jackpay_ledger.csv'

    def decode_tx(self, Transaction):
        
        builder = []
        last4_hash = Transaction.hash
        builder.append(last4_hash)
        amount = Transaction.amount
        builder.append(amount)
        dtg = Transaction.dtg
        builder.append(dtg)

        to_csv = ','.join(builder)

        return to_csv

    # read last entry to ledger
    def read_last(self):
        pass

    # write to ledger
    def write_ledger(self, Transaction):
        # decode obj: Transaction and write to jackpay_ledger.csv
        # r: boolean, good/bad write
        status = False

        # string in form of 'tx_hash_last_4, amount, dtg' (no \n on it)
        to_csv = self.decode_tx(Transaction)

        try: 
            fd = open(self.ledger_name, "a+")
            fd.write(to_csv + "\n")
            fd.close()
            status = True
            return status
        except:
            return status
