# Filename: A10_2D_baseline_client.py
# Written by: James D. Miller
# 6:42 PM Wed January 20, 2016

import sys, os, time
import pygame

# PyGame Constants
from pygame.locals import *
from pygame.color import THECOLORS

# Network stuff. Note "connection" is a single instantiation.
from PodSixNet.Connection import connection, ConnectionListener

# Argument parsing...
import argparse


# =======================================================================
# Classes
# =======================================================================


class NetworkListener(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))

        self.client_colors = {'C1': THECOLORS["orangered1"], 'C2': THECOLORS["tan"], 'C3': THECOLORS["cyan"],
                              'C4': THECOLORS["blue"],
                              'C5': THECOLORS["pink"], 'C6': THECOLORS["red"], 'C7': THECOLORS["coral"],
                              'C8': THECOLORS["green"],
                              'C9': THECOLORS["grey80"], 'C10': THECOLORS["rosybrown3"]}

        self.background_color = THECOLORS["white"]
        self.client_name = 'C0'
        self.client_color = THECOLORS["black"]

    def Network(self, data):
        # print 'network data:', data
        pass

    # def Network_connected(self, data):
    # print "connected to the server", data

    def Network_hello(self, data):
        global client_ID, client_state

        print("Network_hello:", data)

        client_ID = data['P_ID']

        if client_ID == 0:
            print("The server new-client count exceeds the limit. Restart the server.")
            signoff(client_state)

        self.client_name = 'C' + str(client_ID)

        self.background_color = THECOLORS["black"]
        self.client_color = self.client_colors[self.client_name]

        # Initialize user state dictionary.
        client_state = {'action': 'CN',
                        'ID': client_ID,
                        'mXY': (0, 0), 'mBd': False, 'mB': 1,
                        'a': 'U', 's': 'U', 'd': 'U', 'w': 'U',
                        'j': 'U', 'k': 'U', 'l': 'U', 'i': 'U', ' ': 'U',
                        'm': 'U',
                        'f': 'U',
                        't': 'U', 'ls': 'U'}

        pygame.display.set_caption("Air Table GamePad V.3:  Player C" + str(client_ID))

        # def Network_error(self, data):
        # print "error:", data['error'][1]

    # def Network_disconnected(self, data):
    # print "Disconnected from the server."

    def Network_badhealth(self, data):
        global start_shutdown

        start_shutdown = True
        print("The message I'm getting from the server is: " + data['message'] + ".")
        print("I'm really not feeling very well.")
        self.background_color = THECOLORS["white"]

        # signoff(client_state)

    # def Network_myaction(self, data):
    # print "myaction:", data


# =======================================================================
# Functions
# =======================================================================

def signoff(client_state):
    sys.exit()


def checkforUserInput(client_state):
    # Get all the events since the last call to get().
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            signoff(client_state)
        elif (event.type == pygame.KEYDOWN):
            if (event.key == K_ESCAPE):
                signoff(client_state)

            elif (event.key == K_c):
                mydisplay.fill(THECOLORS["yellow"])

            elif (event.key == K_1):
                return 1
            elif (event.key == K_2):
                return 2
            elif (event.key == K_3):
                return 3

            elif (event.key == K_a):
                client_state['a'] = 'D'
            elif (event.key == K_s):
                client_state['s'] = 'D'
            elif (event.key == K_d):
                client_state['d'] = 'D'
            elif (event.key == K_w):
                client_state['w'] = 'D'

            elif (event.key == K_j):
                client_state['j'] = 'D'
            elif (event.key == K_k):
                client_state['k'] = 'D'
            elif (event.key == K_l):
                client_state['l'] = 'D'
            elif (event.key == K_i):
                client_state['i'] = 'D'
            elif (event.key == K_SPACE):
                client_state[' '] = 'D'

            elif (event.key == K_LSHIFT):
                client_state['ls'] = 'D'
            elif (event.key == K_t):
                client_state['t'] = 'D'

            elif (event.key == K_BACKSLASH):
                print
                "Trying to start a new connection."
                connection.DoConnect((args.serverIP, 4330))
                # network_listener = NetworkListener((args.serverIP, 4330))

        elif (event.type == pygame.KEYUP):
            if (event.key == K_a):
                client_state['a'] = 'U'
            elif (event.key == K_s):
                client_state['s'] = 'U'
            elif (event.key == K_d):
                client_state['d'] = 'U'
            elif (event.key == K_w):
                client_state['w'] = 'U'

            elif (event.key == K_j):
                client_state['j'] = 'U'
            elif (event.key == K_k):
                client_state['k'] = 'U'
            elif (event.key == K_l):
                client_state['l'] = 'U'
            elif (event.key == K_i):
                client_state['i'] = 'U'
            elif (event.key == K_SPACE):
                client_state[' '] = 'U'

            elif (event.key == K_LSHIFT):
                client_state['ls'] = 'U'
            elif (event.key == K_t):
                client_state['t'] = 'U'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            client_state['mBd'] = True

            # Check the button status.
            (button1, button2, button3) = pygame.mouse.get_pressed()
            if button1:
                client_state['mB'] = 1
            elif button2:
                client_state['mB'] = 2
            elif button3:
                client_state['mB'] = 3
            else:
                client_state['mB'] = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            client_state['mBd'] = False
            client_state['mB'] = 0

    # cursor x,y
    client_state['mXY'] = pygame.mouse.get_pos()


# =======================================================================
# Main program statements
# =======================================================================

# Parse parameters provided in the command line.
# This description string (and parameter help) gets displayed if help is requested (-h added after the filename).
parser = argparse.ArgumentParser(
    description='Please add optional client parameters after the file name. For example: \n' +
                'A10_2D_baseline_client.py 111.222.22.22')
# A required positional argument.
parser.add_argument('serverIP', type=str, help='Use the IP address that is reported by the server when it starts.')
# An optional positional argument.
# parser.add_argument('someString', type=str, nargs='?', default='string1', help='Just enter a string value in the second position.')
# An optional argument.
# parser.add_argument('--test', '-t', type=str, help='Example: -t teststring OR --test teststring')

args = parser.parse_args()
print("Server IP Address:", args.serverIP)
# print "someString:", args.someString
# print "test:", args.test

pygame.init()

mydisplay = pygame.display.set_mode((800, 700))

# Instantiate clock to help control the framerate.
myclock = pygame.time.Clock()

# Font object for rendering text onto display surface.
fnt = pygame.font.SysFont("Arial", 14)

client_ID = 0

# Initialize the state dictionary
client_state = {}

# Note, the connection can take place in the NetworkListener or here.
# This "connection" is an instantiation of the EndPoint class that is done in the Connection.py file.
# Note, if you do this here, you have to call the "DoConnect" method, not the "Connect" method that
# is indicated on the web site.
# connection.DoConnect((args.serverIP, 4330))

network_listener = NetworkListener(args.serverIP, 4330)
print(args.serverIP)

framerate_limit = 120
flip_timer = 0.0

start_shutdown = False
shutdown_timer = 0.0

while True:

    dt_s = float(myclock.tick(framerate_limit) * 1e-3)
    # myclock.tick(framerate_limit)

    try:
        connection.Pump()
    except:
        signoff(client_state)
    network_listener.Pump()

    checkforUserInput(client_state)
    if client_ID != 0:
        # print "client_state", client_state
        connection.Send(client_state)

    if start_shutdown:
        shutdown_timer += dt_s
        if shutdown_timer > 0.5:
            network_listener.background_color = THECOLORS["red"]
        if shutdown_timer > 1.0:
            signoff(client_state)

    flip_timer += dt_s
    if (flip_timer > 0.2):
        # Background
        mydisplay.fill(network_listener.background_color)

        # Small rectangle to illustrate the client color that will appear on the server screen.
        pygame.draw.rect(mydisplay, network_listener.client_color, pygame.Rect(50, 50, 60, 20), 3)

        # Small background rectangle for text
        pygame.draw.rect(mydisplay, THECOLORS["white"], pygame.Rect(150, 50, 35, 20))
        # Text
        fps_string = "%.0f" % myclock.get_fps()
        txt_surface = fnt.render(fps_string, True, THECOLORS["black"])
        mydisplay.blit(txt_surface, [158, 51])

        pygame.display.flip()
        flip_timer = 0.0