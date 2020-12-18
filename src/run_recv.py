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

    # start input loop
    while True:
        # wait for recv'd data
        print("checking for rec'd data")
        msg_pick, addr = entity_socket.recvfrom(listenport)
        print("Recv'd payment data")
        msg = msg_pick.decode()
        pay_data = msg.split(',')
        print(pay_data)

        # send ACK to router
        ack = 'ACK,' + msg 
        dgram = ack.encode()
        entity_socket.sendto(dgram, (router_addr, router_port))

        # inc balance
        entity.balance += int(pay_data[3])
        print("new balance: " + str(entity.balance))
    
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