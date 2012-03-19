#!/usr/bin/python

import socket
from select import select

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 61453))

while True:
    [readable, writable, errors] = select([s, ], [], [], 0)
    for r in readable:
        if r == s:
            data, addr = s.recvfrom(1024)
            if addr not in clients:
                print "new client:", addr
                clients.append(addr)
            for client in clients:
                if client != addr:
                    s.sendto(data, client)

