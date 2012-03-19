#!/usr/bin/python

import pygame
import argparse
import sys
import socket
from select import select
import json
import random

#----------------------------------------
# Pygame Setup
#----------------------------------------
pygame.init()
pygame.display.set_mode((640, 480))
screen = pygame.display.get_surface()
clock = pygame.time.Clock()

#----------------------------------------
# Constants
#----------------------------------------
colors = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
    (255, 255,   0),
    (255,   0, 255),
    (  0, 255, 255),
]


#----------------------------------------
# Main Loop
#----------------------------------------

class Game():
    def __init__(self):
        self.server = None
        self.socket = None
        self.color = (255, 255, 255)


    def main(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('--server')
        parser.add_argument('--port', type=int, default=61452)
        args = parser.parse_args(argv[1:])

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("0.0.0.0", args.port))

        if args.server:
            self.server = args.server.split(":")

        self.main_loop()


    def main_loop(self):
        self.running = True
        self.lines = {"": []}
        while self.running:
            clock.tick(60)
            self.handle_inputs()
            self.render()
            self.handle_network()
        pygame.quit()


    def handle_inputs(self):
        # Inputs
        keys = {}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                self.socket.sendto(json.dumps([event.pos[0], event.pos[1], self.color]), (self.server[0], int(self.server[1])))
                self.add_point("", [event.pos[0], event.pos[1], self.color])

            self.color = random.choice(colors)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: self.running=False


    def render(self):
        screen.fill((0, 0, 0))

        for user in self.lines:
            for point in self.lines[user]:
                pygame.draw.circle(screen, point[2], (point[0], point[1]), 5)

        pygame.display.update()


    def handle_network(self):
        [readable, writable, errors] = select([self.socket, ], [], [], 0)
        for r in readable:
            if r == self.socket:
                data, addr = self.socket.recvfrom(1024)
                self.add_point(addr, json.loads(data))

    def add_point(self, client, point):
        if client not in self.lines:
            self.lines[client] = []
        self.lines[client].append(point)
        if len(self.lines[client]) > 30:
            self.lines[client].pop(0)


if __name__ == "__main__":
    sys.exit(Game().main(sys.argv))

