# server_connection_handler.py

from http import server
import socket
import urllib.request
import time
import console_visuals as vi
import sys
from tqdm import tqdm
from colorama import init
from colorama import Fore, Back, Style

class ServerConnectionHandler():
    def __init__(self):
        self.n_players = 3#int(input('How many players are there?: '))
        self.n_bots = 0#2#int(input('How many bots to add?: '))
        self.clients = [] # Connection string of players that joined
        self.users = {} # Usernames of players that joined

        # self.server_type = int(input('''
        # How would you like to host the server?:
        # [1] Locally (LAN)
        # [2] Globally (WAN)
        # '''))
        self.server_type = 1

        total = self.n_players + self.n_bots
        if total > 6:
            print(Fore.RED + f'Error: The total number of players and bots is {total}. The maximum is 6!' + Style.RESET_ALL)
            sys.exit(1)
        if total < 3:
            print(Fore.RED + f'Error: The total number of players and bots is {total}. The minimum is 3!' + Style.RESET_ALL)
            sys.exit(1)


        # Select the IP to host from (Public or Private)
        if self.server_type == 1:
            host = '127.0.0.1'
        elif self.server_type == 2:
            try:
                host = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8') # Get public IP
            except Exception as network_error:
                print(Fore.RED + f'Error: Unable to resolve public IP address. Are you connected to the internet?' + Style.RESET_ALL)

        # Initialize Server
        print(f'Hosting server using IP: {host}')
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, 8080))
        self.server.listen(self.n_players)

    def broadcast(self, msg: str):
        '''Send a message to all clients'''
        print(f"[Broadcast Message] {msg}")
        for c in self.clients:
            c.send(f"BM_{msg}".encode('utf-8'))

    def message_client(client, msg: str):
        '''Send a message to a specific client'''
        client.send(msg.encode('utf-8')) # Message user

    def muster_clients(self):
        '''Server will accept incoming requests for clients to join until it reaches the number of players.'''
        pbar = tqdm(initial = 0, total = self.n_players, desc = 'Waiting for players to join.')
        while len(self.clients) < self.n_players:
            client, ip = self.server.accept()
            self.clients.append(client) # Add client to roster
            username = self.assign_username(client) # Prompt client for their username
            self.broadcast(Fore.BLUE + f'{username} has joined the game!' + Style.RESET_ALL)
            pbar.update(1)
        pbar.close()

    def assign_username(self, client: socket.socket):
        '''Request that the client provide a username'''
        client.send('AssignUserName'.encode('utf-8'))
        username = client.recv(3000).decode('utf-8')

        # TODO implement username validation and checking for duplicates

        self.users[username] = client # Save the username to client association
        client.send(f'Welcome, {username}!\n'.encode('utf-8'))
        return username

    def choose_character(self, client: socket.socket, available_characters: list):
        '''Prompt the user to choose an available character'''
        options = available_characters

        client.send(f'AssignCharacter@{options}'.encode('utf-8'))
        selection = int(client.recv(3000).decode('utf-8')) # Get the players selection number
        selected_character = available_characters[selection-1]
        available_characters.remove(selected_character) # Player has chosen character, remove it from list
        client.send(f'You have selected {selected_character}!\n'.encode('utf-8'))

        return selected_character

    def play_again_vote(self):
        '''Handle player voting to determine if another game should be played.
        
        Returns:
            boolean: Whether or not to play again
        '''
        play_again_tally = 0

        for client in self.clients:
            client.send('Would you like to play again?\n [1] Yes [2] No'.encode('utf-8'))
            selection = int(client.recv(3000).decode('utf-8')) # Get the player's vote
            if selection == 1:
                play_again_tally += 1

        vote = play_again_tally/len(self.clients)
        if vote > 0.5:
            # Majority voted to play again
            self.broadcast('The majority vote is to play again!')
            return True
        elif vote == 0.5:
            # Equal vote on both sides
            self.broadcast('The vote was 50-50. Please make up your minds and vote again!')
            self.play_again_vote(self)
        else:
            # Majority voted to stop playing
            self.broadcast("The majority voted to stop playing. Goodbye!")
            return False

    def kick_players(self):
        '''Kick all of the players in the game. Close the connection socket gracefully.'''
        # Send message client app to signal disconnection
        for client in self.clients:
            client.send('kick'.encode('utf-8'))
        self.clients = [] # Wipe clients from SCH
        


        


