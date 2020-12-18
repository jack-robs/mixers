import sys
from socket import *
import time
from Entity import *
from Packet import *

def register_to_router(router_addr, router_port, entity, pubk):
    print("registering publikey key with router")

def runEntity(router_addr, router_port, entity, listenport):

    # create connection w/ router
    entity_socket = socket(AF_INET, SOCK_DGRAM)
    entity_socket.bind(('', listenport))
    entity_socket.settimeout(1)
    name = entity.name

    # start input loop
    while True:
        
            
        uinput = input('`q`, `pay`, `bal`> ')

        # look for q signal
        if uinput == 'q':
            print("killing connection")
            return 
        
        elif uinput == "check":
            continue

        # look for pay signal
        elif uinput == 'pay':
            pay = int(input('pay how much: '))
            recv = input('send to who: ')
            if pay > entity.balance:
                print("insuff funds")
                continue

            # create payment packet: `<from>,<to>,<amount>`
            pay_packet = 'pay,' + entity.name + "," + recv + "," + str(pay)
            print("pay packet:", pay_packet)

            # send packet to router
            dgram = pay_packet.encode()
            entity_socket.sendto(dgram, (router_addr, router_port))

            # output result of sending payment (basic ++)
            ack_coded, ack_adr = entity_socket.recvfrom(2048)
            ack = ack_coded.decode()
            if ack == 'ACK':
                print("Recv'd confirmation: " + ack)
                
                # dec balance
                entity.balance -= pay
                print("new balance: " + str(entity.balance))
            else:
                print("failed payment " + ack)

        # look for msg received signal -> payment has arrived
        elif uinput == "bal":
            print("User: " + entity.name + " Bal: " + str(entity.balance))

        else:
            print("unk input")
            continue

    
def main():

    # init an entity, router addr and port
    # cli: python3 run_entity.py bob <router port>
    entity = Entity(sys.argv[2])
    addr = '127.0.0.1'
    router_port = int(sys.argv[1])
    entity_port = int(sys.argv[3])
    print("Router port: " + str(router_port) + " Entity name: " + sys.argv[2] + " Entity port: " + str(entity_port))
    runEntity(addr, router_port, entity, entity_port)
    print("Goodbye " + entity.name)


main()