# This an example of how we can simulate game scenarios. We can programatically run through user I/O.
import time
import socket

def print_response(client):
    print(client.recv(3000).decode('utf-8'))
    time.sleep(0.25)

def create_client(host = '127.0.0.1'):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host,8080))
    time.sleep(0.25)
    return c

def client_tx(client, message):
    '''Transmit message from client to server'''
    client.send(str(message).encode('utf-8'))
    time.sleep(0.25)
    print_response(client)


def stub_1():
    '''Simulate Game Scenario'''

    # Open three client applications
    c1 = create_client()
    c2 = create_client()
    c3 = create_client()

    # Each user chooses a username
    client_tx(c1, 'Player1')
    client_tx(c2, 'Player2')
    client_tx(c3, 'Player3')

    # Each user selects a character
    client_tx(c1, '1')  # Miss Scarlet
    client_tx(c2, '2')  # Mrs. White
    client_tx(c3, '2')  # Mr. Green

    # Player 1
    client_tx(c1, '1') # Choose to move
    client_tx(c1, 'd1') # Move to D1
    client_tx(c1, '2') # End Turn
    #print_response(c1)

    #Player 2
    client_tx(c2, '1') # Choose to move
    client_tx(c2, 'd5') # Move to D5
    client_tx(c2, '2') # End Turn
    #print_response(c2)

    #Player 3
    client_tx(c3, '3') # End Turn
    #print_response(c3)

    # Player 1
    client_tx(c1, '1')  # Choose to move
    client_tx(c1, 'e1')  # Move to D1
    client_tx(c1, '3')  # End Turn
    # print_response(c1)

    # Player 2
    client_tx(c2, '1')  # Choose to move
    client_tx(c2, 'e5')  # Move to D5
    client_tx(c2, '3')  # End Turn
    # print_response(c2)

    # Player 3
    client_tx(c3, '3')  # End Turn
    # print_response(c3)

    # Player 1
    client_tx(c1, '1')  # Choose to move
    client_tx(c1, 'e2')  # Move to D1
    client_tx(c1, '2')  # End Turn
    # print_response(c1)

    # Player 2
    client_tx(c2, '1')  # Choose to move
    client_tx(c2, 'e4')  # Move to D5
    client_tx(c2, '2')  # End Turn
    # print_response(c2)

    # Player 3
    client_tx(c3, '3')  # End Turn
    # print_response(c3)

    # Player 1
    client_tx(c1, '3')  # End Turn
    # print_response(c1)

    # Player 2
    client_tx(c2, '1')  # Choose to move
    client_tx(c2, 'e3')  # Move to D5
    client_tx(c2, '3')  # End Turn
    # print_response(c2)

    # Player 3
    client_tx(c3, '3')  # End Turn
    # print_response(c3)

    # Player 1
    client_tx(c1, '3')  # End Turn
    # print_response(c1)

    # Player 2
    client_tx(c2, '1')  # Choose to move
    '''
    client_tx(c2, 'e1')  # Move to E1
    client_tx(c2, '1')  # Suggestion
    client_tx(c2, '1')  # Choose to Miss Scarlet
    client_tx(c2, '1')  # Choose Candlestick
    client_tx(c2, '2')  # End Turn
    '''
    # print_response(c2)

    # Player 3

    time.sleep(1000000)  # Prevents client connections from closing
    # Player 1
'''
    client_tx(c1, '2') # Make Accusation
    client_tx(c1, '2') # Suspect option 2
    client_tx(c1, '2') # Weapon option 2
    client_tx(c1, '2') # Room option 2

    #print_response(c1)

    client_tx(c1, '2') # Choose to play again
    #print_response(c1)
    client_tx(c2, '2') # Choose to play again
    #print_response(c2)
    client_tx(c3, '2') # Choose to play again
    #print_response(c3)
'''









if __name__ == '__main__':
    stub_1()

