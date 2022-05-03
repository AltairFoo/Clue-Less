from card import Card
from player import Player
from location import Location
from turn import Turn
import console_visuals as vi


class GameManager:
    def __init__(self, players, extra_cards, case_file_cards):
        self.players = players
        # All Card objects are referencable through the players besides extra cards and case file cards
        self.extra_cards = extra_cards
        self.case_file_cards = case_file_cards
        self.game_over = False
        self.player_num_going = 0 # To track where in the players list we are for turns

    def move_to_next_turn(self):
        # Find the next un-eliminated player
        found_player = False

        while not found_player:
            self.player_num_going = (self.player_num_going + 1) % len(self.players)

            if not self.players[self.player_num_going].eliminated:
                found_player = True

        # Check how many players are left
        players_left = 0

        for p in self.players:
            if not p.eliminated:
                players_left = players_left + 1

        # End the game if only 1 player remains
        if players_left == 1:
            self.game_over = True

    def run_turn(self, player):
        self.broadcast(f"It is {player.username}'s turn.")

        # At the start of a turn, add the following console visuals:
        self.message_player(player,vi.game_map()) # Print the static game map
        self.message_player(player, vi.ToGUI(self.players)) # colored game map
        self.message_player(player, vi.player_cards(player))# Print a list of the player's cards
        self.message_player(player, vi.extra_cards(self.extra_cards))# Print the extra cards

        your_cards = [c.name for c in player.cards]
        your_cards = ', '.join(your_cards)
        self.message_player(player, f"Your cards: {your_cards}")

        turn = Turn(player)
        player_options = turn.generate_player_options(player)

        player_choice = self.receive_player_choice(player, player_options)

        # While the player has not ended their turn or made an accusation:
        # 1. Execute player's choice,
        # 2. Generate player's options,
        # 3. Receive player's next choice
        while player_choice != "End Turn" and player_choice != "Accuse":
            # Execute player's choice
            if player_choice == "Move":
                # Get the movement options available to the player
                player_move_options = turn.generate_player_move_options(player)
                # Receive player's move choice
                player_move_choice = self.receive_player_move_choice(player, player_move_options)
                # Move the player
                self.move_player(player, player_move_choice)
                turn.moved = True # Player has moved their location this turn. They can't move locations again until the next turn.
            if player_choice == "Suggest":
                # Get string names of character, weapon, and room for suggestion, in that order
                suggestion_values = self.get_suggestion_values(player)

                # Inform all players of the suggestion
                suggest_msg = player.username + " is making a suggestion: It was " + \
                              suggestion_values[0] + " in the " + suggestion_values[2] + " with the " + \
                              suggestion_values[1] + "!"
                self.broadcast(suggest_msg)

                # Find if any player is playing as the suggested character
                player_to_move = None
                for p in self.players:
                    if p.character == suggestion_values[0]:
                        player_to_move = p

                # If the player exists, move them
                if player_to_move is not None:
                    self.move_player(player_to_move, player.location)
                    player_to_move.was_suggested = True # To help determine game options next turn

                # Run the suggestion
                self.make_suggestion(player, suggestion_values)

                # Update Turn so player's options are accurate
                turn.suggested = True

            player_options = turn.generate_player_options(player)

            player_choice = self.receive_player_choice(player, player_options)

        player.was_suggested = False # Reset in case they started out suggested

        # Return player choice because it could end on End Turn or Accuse
        # GameManager will act differently, depending on the result of the turn
        return player_choice

    def receive_player_choice(self, player, player_options):
        options = ''
        for i in enumerate(player_options):
            options += f'[{i[0]+1}] {i[1]}\n'

        #options_prompt = "What would you like to do?: " + player_options[0]
        options_prompt = f'What would you like to do? \n{options}'

        '''for option in player_options[1:]:
            options_prompt = options_prompt + option'''

        # Send options prompt to user and receive their choice as numeric input
        self.message_player(player, options_prompt)
        player_choice = int(player.client_id.recv(3000).decode('utf-8'))
        player_choice = player_options[player_choice-1]
        # Error handling for incorrect user input
        while player_choice not in player_options:#['1','2','3']: #player_options:
            error_options_prompt = "Invalid choice entered. " + options_prompt

            self.message_player(player, error_options_prompt)
            player_choice = player.client_id.recv(3000).decode('utf-8')

        return player_choice

    def receive_player_move_choice(self, player, move_options):
        # move_options will be a list of Location objects (length at least 1, up to 4)
        options_prompt = f"Your current location is {player.location.name}. Where would you like to move? Your options are: "
        options = [o.name for o in move_options]
        options_prompt = options_prompt + ', '.join(options)

        # Send options prompt to user and receive their choice as numeric input
        self.message_player(player,options_prompt)
        player_choice_name = str(player.client_id.recv(3000).decode('utf-8')).upper()

        # Error handling for incorrect user input
        # ...

        # Find the Location object with the name selected by the player
        player_choice = list(filter(lambda option: option.name == player_choice_name, move_options))[0]

        return player_choice # Return the location object

    def move_player(self, player, new_location):
        # Update values of Location object for player's current location
        player.location.players_present.remove(player)
        if player.location.max_players > len(player.location.players_present):
            if player.location.name[0] != 'H':
                player.location.moveable = True # Mark players previous location as moveable (Unless it was a home square)

        # Update player's location
        player.location = new_location

        # Update values of Location object for player's new location
        player.location.players_present.append(player)
        if player.location.max_players <= len(player.location.players_present):
            player.location.moveable = False

        self.broadcast(player.username + " moved to " + new_location.name)

    # For the UI, we will have to change this to a pop-up or something
    def get_suggestion_values(self, player):
        suggest_char_prompt = 'Which character committed the crime?:' + vi.suspects()

        self.message_player(player,suggest_char_prompt)
        suggest_char_choice = int(player.client_id.recv(3000).decode('utf-8'))
        suggest_char_choice = self.character_name_list()[suggest_char_choice-1]

        # Error handling for incorrect suggestion player input
        while suggest_char_choice not in self.character_name_list():
            self.message_player(player, "Invalid character selection.")
            self.message_player(player,suggest_char_prompt)
            suggest_char_choice = int(player.client_id.recv(3000).decode('utf-8'))

        suggest_weapon_prompt = 'Which weapon was used for the crime?:' + vi.weapons()

        self.message_player(player,suggest_weapon_prompt)
        suggest_weapon_choice = int(player.client_id.recv(3000).decode('utf-8'))
        suggest_weapon_choice = self.weapon_name_list()[suggest_weapon_choice-1]

        while suggest_weapon_choice not in self.weapon_name_list():
            self.message_player(player, "Invalid weapon name entered.")
            self.message_player(player,suggest_weapon_prompt)
            suggest_weapon_choice = player.client_id.recv(3000).decode('utf-8')

        # Return the names of the character, weapon, and room (3 strings)
        # Change to returning the cards? Or the names of the first 2 but then the Location object?
        suggestion_values = [suggest_char_choice, suggest_weapon_choice, player.location.room_name]

        return suggestion_values

    def make_suggestion(self, player, suggestion_values):
        # Get list of players from which to request a card
        players_to_request = self.players[:self.player_num_going] + self.players[self.player_num_going + 1:]

        request_ind = 0
        card_to_show = None

        while card_to_show is None and request_ind < len(players_to_request):
            showing_player = players_to_request[request_ind]
            showable_cards = []

            # Check if the player has a showable card
            for card in showing_player.cards:
                # suggestion_values is a list of card names
                if card.name in suggestion_values:
                    showable_cards.append(card.name)

            if len(showable_cards) == 0:
                # If 0 showable cards, message all players and move to next player
                suggest_msg = showing_player.username + " was unable to show a card!"
                self.broadcast(suggest_msg)
                request_ind = request_ind + 1
            else:
                # If 1 showable card, that's the card. Otherwise, prompt for card selection
                if len(showable_cards) == 1:
                    card_to_show = showable_cards[0]
                else:
                    # Create prompt for card to show
                    # Use offset index for better UX. Should -1 when sending the actual card.
                    card_show_prompt = "Which card would you like to show? " + showable_cards[0] + "[1]"
                    showable_cards_index = 1
                    for card_name in showable_cards[1:]:
                        showable_cards_index += 1
                        card_show_prompt = card_show_prompt + card_name + "[" + showable_cards_index + "] " 

                    self.message_player(showing_player,card_show_prompt)
                    card_to_show = showing_player.client_id.recv(3000).decode('utf-8')

                    # Error handling if player enters incorrect value
                    while card_to_show not in showable_cards:
                        error_card_show_prompt = "That's not a showable card. " + card_show_prompt

                        self.message_player(showing_player,error_card_show_prompt)
                        card_to_show = showing_player.client_id.recv(3000).decode('utf-8')

                # Finally, show the card to the suggesting player and tell all players a card was shown
                card_showing_prompt = showing_player.username + " shows you " + card_to_show

                self.message_player(player,card_showing_prompt)

                self.broadcast(showing_player.username + " showed a card to " + player.username + "!")

                # Update player's checklist?
        return

    # Keep run_accusation separate from run_turn since run_turn either returns 'Accuse' or 'End Turn'
    # We will call run_turn and run_accusation separately in the main script
    def run_accusation(self, player):
        # Get accusation values
        accusation_values = self.get_accusation_values(player)

        # Broadcast to all players the accusation
        accuse_msg = player.username + " is making an ACCUSATION: It was " + \
                      accusation_values[0] + " in the " + accusation_values[2] + " with the " + \
                      accusation_values[1] + "!"
        self.broadcast(accuse_msg)

        # Check accusation values against answer
        correct_accuse = self.check_accusation_values(accusation_values)

        # If accusation is correct, set self.game_over to True
        if correct_accuse:
            self.broadcast(player.username + "'s accusation was correct!")
            self.game_over = True
        else: # If accusation is wrong, remove player from the players list
            self.broadcast(player.username + "'s accusation was wrong! " +
                           player.username + " has been eliminated!")

            player.eliminated = True

        return # Nothing is returned. Moving to next turn will check the number of players left.

    # For the UI, we will have to change this to a pop-up or something
    def get_accusation_values(self, player):
        accuse_char_prompt = 'Which character committed the crime?:' + vi.suspects()
        self.message_player(player,accuse_char_prompt)
        accuse_char_choice = int(player.client_id.recv(3000).decode('utf-8'))
        accuse_char_choice = self.character_name_list()[accuse_char_choice-1]

        # Error handling for incorrect suggestion player input
        while accuse_char_choice not in self.character_name_list():
            self.message_player(player, "Invalid character selection.")
            self.message_player(player,accuse_char_prompt)
            accuse_char_choice = int(player.client_id.recv(3000).decode('utf-8'))

        accuse_weapon_prompt = 'Which weapon was used for the crime?:' + vi.weapons()
        self.message_player(player, accuse_weapon_prompt)
        accuse_weapon_choice = int(player.client_id.recv(3000).decode('utf-8'))
        accuse_weapon_choice = self.weapon_name_list()[accuse_weapon_choice-1]

        while accuse_weapon_choice not in self.weapon_name_list():
            self.message_player(player, "Invalid weapon selection")
            self.message_player(player, accuse_weapon_prompt)
            accuse_weapon_choice = int(player.client_id.recv(3000).decode('utf-8'))

        accuse_location_prompt = """Where did the crime happen:
        Study, Hall, Lounge, Library, Billiard Room, Dining Room, Conservatory, Ballroom, or Kitchen?"""
        
        accuse_location_prompt = 'Where did the crime happen?: ' + vi.rooms()
        self.message_player(player,accuse_location_prompt)
        accuse_location_choice = int(player.client_id.recv(3000).decode('utf-8'))
        accuse_location_choice = self.room_name_list()[accuse_location_choice-1]

        while accuse_location_choice not in self.room_name_list():
            self.message_player(player, 'Invalid room selection.')
            self.message_player(player,accuse_location_prompt)
            accuse_location_choice = int(player.client_id.recv(3000).decode('utf-8'))

        # Return the names of the character, weapon, and room (3 strings)
        # Change to returning the cards? Or the names of the first 2 but then the Location object?
        accusation_values = [accuse_char_choice, accuse_weapon_choice, accuse_location_choice]

        return accusation_values

    def check_accusation_values(self, accusation_values):
        correct_count = 0
        for acc_val in accusation_values:
            if acc_val in ["Col. Mustard", "Hall", "revolver"]:
                correct_count = correct_count + 1
            #for c in self.case_file_cards:
            #    if acc_val == c.name:
            #        correct_count = correct_count + 1

        if correct_count == 3:
            correct_accuse = True
        else:
            correct_accuse = False

        return correct_accuse

    def end_game(self):
        # The player currently 'going' is the winner
        player_going = self.players[self.player_num_going]

        # Check for the type of game end
        players_left = 0
        for p in self.players:
            if not p.eliminated:
                players_left = players_left + 1
        # If there is only 1 un-eliminated player, then they won by survival.
        if players_left == 1:
            self.broadcast(player_going.username + " is the last player remaining. They win!")
        # Otherwise, they won with a successful accusation
        else:
            self.broadcast(player_going.username + " has won!")

        # Find the case file card for the correct type for the answer broadcast
        cf_char = None
        cf_weap = None
        cf_loc = None
        for cfc in self.case_file_cards:
            if cfc.type == "suspect":
                cf_char = cfc
            if cfc.type == "weapon":
                cf_weap = cfc
            if cfc.type == "room":
                cf_loc = cfc

        # Broadcast the answer to everyone
        self.broadcast("It was " + cf_char.name + " with the " + cf_weap.name + " in the " + cf_loc.name)

        return

    def character_name_list(self):
        return ["Miss Scarlet", "Col. Mustard", "Mrs. White", "Mr. Green", "Mrs. Peacock", "Prof. Plum"]

    def weapon_name_list(self):
        return ["candlestick", "revolver", "dagger", "lead pipe", "rope", "wrench"]

    def room_name_list(self):
        return ["Study", "Hall", "Lounge", "Library", "Billiard Room", "Dining Room", "Conservatory",
                "Ballroom", "Kitchen"]

    def broadcast(self, msg):
        '''Send a message to all clients'''
        print(f"[Broadcast Message] {msg}")
        for c in self.players:
            c.client_id.send(f"[Broadcast Message] {msg}\n".encode('utf-8'))

    def message_player(self, player, msg):
        '''Send a specific to a specific player'''
        #print(f"[Message to {player.username}] {msg}")
        player.client_id.send(str(msg+'\n').encode('utf-8'))
