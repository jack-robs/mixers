class Packet:

    def __init__(self, sender, recv, amount, addr=0, user=''):
        self.registeraddr = addr
        self.user = user
        self.sender = sender
        self.recv = recv
        self.amount = amount