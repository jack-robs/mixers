import sys
import pickle
from socket import *
import time
from datetime import datetime
from Router import *

def run_router(listenaddr,listenport, router):

    # build socket
    router_socket = socket(AF_INET, SOCK_DGRAM)
    router_socket.bind(('', listenport))

    # listen on socket and react
    while True:
        print("router listening")
        msg_coded, sender_addr = router_socket.recvfrom(listenport)
        msg = msg_coded.decode()
        msg_data = msg.split(',')
        print("recv'd: " + msg)
        # incoming payment
        if msg_data[0] == 'pay':
            # check if payer is registered user

            if msg_data[2] in router.registered_users:
                payer_port = router.registered_users[msg_data[2]]
                print("sending to " + str(payer_port))

                payee_msg = ','.join(msg_data)
                print(payee_msg)
                print(sender_addr)
                dgram = payee_msg.encode()
                payto_addr = ('127.0.0.1', payer_port)
                router_socket.sendto(dgram, payto_addr)

                # send ack to sender at end of payment
                send_back = 'ACK'
                dgram = send_back.encode()
                router_socket.sendto(dgram, sender_addr)
                print("send to payer ACK")

            else: 
                # bad payment, user does not exist
                send_back = 'NACK'
                dgram = send_back.encode()
                router_socket.sendto(dgram, sender_addr)
                print("send to payer NACK")
                continue
        
                
        elif msg_data[0] == "ACK":
            print("write to ledger")
            # TODO write payment to ledger
            print("in ack:", msg_data)
            to_ledg = ','.join(msg_data)
            now = datetime.now()
            timestamp = now.strftime("%d%m%y_%H%M%S\n")
            to_ledg += ','
            to_ledg += timestamp
            print("to ledge:", to_ledg)
            fd = open("ledger.txt", "a+")
            fd.write(to_ledg)
            fd.close()
            continue

        elif msg_data[0] == "NACK":
            print("payment failed, don't write to ledger")
            continue



def main():

    # make router, register entities during instantiation
    router = Router('alice', 1026, 'bob', 1027)
    # python run_router 1025
    listenport = int(sys.argv[1])
    listenaddr = '127.0.0.1'
    run_router(listenaddr, listenport, router)


main()