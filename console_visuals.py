from colorama import init
from colorama import Fore, Back, Style
from enum import Enum

def game_logo():
    game_logo = Fore.RED + '''
    ░█████╗░██╗░░░░░██╗░░░██╗███████╗░░░░░░██╗░░░░░███████╗░██████╗░██████╗
    ██╔══██╗██║░░░░░██║░░░██║██╔════╝░░░░░░██║░░░░░██╔════╝██╔════╝██╔════╝
    ██║░░╚═╝██║░░░░░██║░░░██║█████╗░░█████╗██║░░░░░█████╗░░╚█████╗░╚█████╗░
    ██║░░██╗██║░░░░░██║░░░██║██╔══╝░░╚════╝██║░░░░░██╔══╝░░░╚═══██╗░╚═══██╗
    ╚█████╔╝███████╗╚██████╔╝███████╗░░░░░░███████╗███████╗██████╔╝██████╔╝
    ░╚════╝░╚══════╝░╚═════╝░╚══════╝░░░░░░╚══════╝╚══════╝╚═════╝░╚═════╝░
    ''' + Style.RESET_ALL
    return(game_logo)

def suspects():
    '''Print the suspect options'''
    suspects = '''
    +----------------------+
    |      Suspects        |
    +----------------------+
    | [1] Miss Scarlet     |
    | [2] Col. Mustard     |
    | [3] Mrs. White       |
    | [4] Mr. Green        |
    | [5] Mrs. Peacock     |
    | [6] Prof. Plum       |
    +----------------------+
    '''
    return(suspects)

def weapons():
    '''Print the weapons options'''
    weapons = '''
    +----------------------+
    |       Weapons        |
    +----------------------+
    | [1] Candlestick      |
    | [2] Revolver         |
    | [3] Dagger           |
    | [4] Lead Pipe        |
    | [5] Rope             |
    | [6] Wrench           |
    +----------------------+
    '''
    return(weapons)

def options():
    '''Print the options for suspect and weapon'''
    options = '''
    +----------------------+-----------------+
    |      Suspects        |     Weapons     |
    +----------------------+-----------------+
    | [1] Miss Scarlet     | [1] Candlestick |
    | [2] Col. Mustard     | [2] Revolver    |
    | [3] Mrs. White       | [3] Dagger      |
    | [4] Mr. Green        | [4] Lead Pipe   |
    | [5] Mrs. Peacock     | [5] Rope        |
    | [6] Prof. Plum       | [6] Wrench      |
    +----------------------+-----------------+
    '''
    return(options)

def rooms():
    '''Print all the room options'''
    rooms = '''
    +-------------------+
    |      Rooms        |
    +-------------------+
    | [1] Study         |
    | [2] Hall          |
    | [3] Lounge        |
    | [4] Library       |
    | [5] Billiard Room |
    | [6] Dining Room   |
    | [7] Conservatory  |
    | [8] Ballroom      |
    | [9] Kitchen       |
    +-------------------+
    '''
    return(rooms)

def player_suggestion(murderer, weapon, room):
    suggestion = Fore.YELLOW + f'''
    +----------------------+
           SUGGESTION     
    +----------------------+
    * Murderer: {murderer} 
    * Weapon: {weapon}     
    * Room: {room}         
    +----------------------+
    ''' + Style.RESET_ALL
    return(suggestion)

def player_accusation(murderer, weapon, room):
    accusation = Fore.RED + f'''
    +----------------------+
           ACCUSATION      
    +----------------------+
    * Murderer: {murderer} 
    * Weapon: {weapon}     
    * Room: {room}         
    +----------------------+
    ''' + Style.RESET_ALL

def game_map():
    '''Print the game map'''
    map = f'''
            A       B        C       D         E
         _______          _______          _________
        |       |________|       |___H1___|         |
    1   | Study  ________  Hall   ________  Lounge  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    2    H6| |              | |              |  |H2
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    3   |Library _________Billiard________  Dining  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    4    H5| |              | |              |  |
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    5   |Conserv ________Ball Room_________ Kitchen |
        |_______|   H4   |_______|   H3   |_________|
    '''
    return(map)

def extra_cards(extra_cards):
    '''Print the extra cards on the board'''
    cards_names = [ card.name for card in extra_cards]
    cards_string = ', '.join(cards_names)
    extra_cards = f'Extra Cards: {cards_names}'
    return extra_cards

def player_cards(player):
    '''Print the cards a specific player has'''
    cards_names = [ card.name for card in player.cards]
    cards_string = ', '.join(cards_names)
    player_cards = f'Your Cards: {cards_names}'
    return player_cards

def case_file_envelope(end_accusation):
    '''Print the contents of the case file envelope'''
    case_file = f'''
    Here are the contents of the case file:   
    +----------------------+
       Case File Envelope    
    +----------------------+
    * Murderer: {end_accusation['murderer']} 
    * Weapon: {end_accusation['weapon']}     
    * Room: {end_accusation['room']}         
    +----------------------+
    '''
    return case_file

def ToGUI(players):
    # port player to enum
    GameMap = {
            Locations.Study:[], Locations.H1:[], Locations.Hall:[], Locations.H2:[], Locations.Lounge:[],
            Locations.H3:[], Locations.H4:[], Locations.H5:[],
            Locations.Library:[], Locations.H6:[], Locations.BillardRoom:[], Locations.H7:[], Locations.DiningRoom:[],
            Locations.H8:[], Locations.H9:[], Locations.H10:[],
            Locations.Conservatory:[], Locations.H11: [], Locations.Ballroom:[], Locations.H12:[], Locations.Kitchen:[]
        }
    '''
            A       B        C       D         E
         _______          _______          _________
        |       |________|       |___H1___|         |
    1   | Study  ________  Hall   ________  Lounge  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    2    H6| |              | |              |  |H2
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    3   |Library _________Billiard________  Dining  |
        |__   __|        |__   __|        |__    ___|
           | |              | |              |  |
    4    H5| |              | |              |  |
         __| |__          __| |__          __|  |___
        |       |________|       |________|         |
    5   |Conserv ________Ball Room_________ Kitchen |
        |_______|   H4   |_______|   H3   |_________|
    '''
    for player in players:
        if player.location == "A1":
            GameMap[Locations.Study].append(convertToReference(player.character))
        elif player.location == "A2":
            GameMap[Locations.H3].append(convertToReference(player.character))
        elif player.location == "A3":
            GameMap[Locations.Library].append(convertToReference(player.character))
        elif player.location == "A4":
            GameMap[Locations.H8].append(convertToReference(player.character))
        elif player.location == "A5":
            GameMap[Locations.Conservatory].append(convertToReference(player.character))
        elif player.location == "B1":
            GameMap[Locations.H1].append(convertToReference(player.character))
        elif player.location == "B3":
            GameMap[Locations.H6].append(convertToReference(player.character))
        elif player.location == "B5":
            GameMap[Locations.H11].append(convertToReference(player.character))
        elif player.location == "C1":
            GameMap[Locations.Hall].append(convertToReference(player.character))
        elif player.location == "C2":
            GameMap[Locations.H4].append(convertToReference(player.character))
        elif player.location == "C3":
            GameMap[Locations.BillardRoom].append(convertToReference(player.character))
        elif player.location == "C4":
            GameMap[Locations.H9].append(convertToReference(player.character))
        elif player.location == "C5":
            GameMap[Locations.Ballroom].append(convertToReference(player.character))
        elif player.location == "D1":
            GameMap[Locations.H2].append(convertToReference(player.character))
        elif player.location == "D3":
            GameMap[Locations.H7].append(convertToReference(player.character))
        elif player.location == "D5":
            GameMap[Locations.H12].append(convertToReference(player.character))
        elif player.location == "E1":
            GameMap[Locations.Lounge].append(convertToReference(player.character))
        elif player.location == "E2":
            GameMap[Locations.H5].append(convertToReference(player.character))
        elif player.location == "E3":
            GameMap[Locations.DiningRoom].append(convertToReference(player.character))
        elif player.location == "E4":
            GameMap[Locations.H10].append(convertToReference(player.character))
        elif player.location == "E5":
            GameMap[Locations.Kitchen].append(convertToReference(player.character))
        
    mapString = ""
    # generate console output line by line
    for y_coord in range(17):
        if y_coord == 0:
            mapString += Fore.WHITE + "        A       B        C       D         E\n"
        elif y_coord == 1:
            mapString += Fore.WHITE + "     _______          _______          _________\n"
        elif y_coord == 2:
            mapString += Fore.WHITE + "    |       |________|       |________|         |\n"
        elif y_coord == 3:
            _study = "Study" if GameMap[Locations.Study] == [] else SuspectColor[GameMap[Locations.Study][-1].name].value + "Study"
            _h1 = "H1" if GameMap[Locations.H1] == [] else SuspectColor[GameMap[Locations.H1][-1].name].value + "H1"
            _hall = "Hall" if GameMap[Locations.Hall] == [] else SuspectColor[GameMap[Locations.Hall][-1].name].value + "Hall"
            _h2 = "H2" if GameMap[Locations.H2] == [] else SuspectColor[GameMap[Locations.H2][-1].name].value + "H2"
            _Lounge = "Lounge" if GameMap[Locations.Lounge] == [] else SuspectColor[GameMap[Locations.Lounge][-1].name].value + "Lounge"
            mapString += Fore.WHITE + "1   | " + _study + Fore.WHITE + "  ___" + _h1 + Fore.WHITE + "___  " + _hall + Fore.WHITE + "   ___" + _h2 + Fore.WHITE + "___  " + _Lounge + Fore.WHITE + "  |\n"
        elif y_coord == 4:
            mapString += Fore.WHITE + "    |__   __|        |__   __|        |__    ___|\n"
        elif y_coord == 5:
            mapString += Fore.WHITE + "       | |              | |              |  |\n"
        elif y_coord == 6:
            _h3 = "H3" if GameMap[Locations.H3] == [] else SuspectColor[GameMap[Locations.H3][-1].name].value + "H3"
            _h4 = "H4" if GameMap[Locations.H4] == [] else SuspectColor[GameMap[Locations.H4][-1].name].value + "H4"
            _h5 = "H5" if GameMap[Locations.H5] == [] else SuspectColor[GameMap[Locations.H5][-1].name].value + "H5"
            mapString += Fore.WHITE + "2    " + _h3 + Fore.WHITE + "| |            " + _h4 + Fore.WHITE + "| |              |  |" + _h5 + "\n"
        elif y_coord == 7:
            mapString += Fore.WHITE + "     __| |__          __| |__          __|  |___\n"
        elif y_coord == 8:
            mapString += Fore.WHITE + "    |       |________|       |________|         |\n"
        elif y_coord == 9:
            _library = "Library" if GameMap[Locations.Library] == [] else SuspectColor[GameMap[Locations.Library][-1].name].value + "Library"
            _h6 = "H6" if GameMap[Locations.H6] == [] else SuspectColor[GameMap[Locations.H6][-1].name].value + "H6"
            _billiard = "Billiard" if GameMap[Locations.BillardRoom] == [] else SuspectColor[GameMap[Locations.BillardRoom][-1].name].value + "Billiard"
            _h7 = "H7" if GameMap[Locations.H7] == [] else SuspectColor[GameMap[Locations.H7][-1].name].value + "H7"
            _dining = "Dining" if GameMap[Locations.DiningRoom] == [] else SuspectColor[GameMap[Locations.DiningRoom][-1].name].value + "Dining"
            mapString += Fore.WHITE + "3   |" + _library + Fore.WHITE + " ___" + _h6 + Fore.WHITE + "___ "+ _billiard + Fore.WHITE + "___"+ _h7 + Fore.WHITE + "___  " +_dining + Fore.WHITE + "  |\n"
        elif y_coord == 10:
            mapString += Fore.WHITE + "    |__   __|        |__   __|        |__    ___|\n"
        elif y_coord == 11:
            mapString += Fore.WHITE + "       | |              | |              |  |\n"
        elif y_coord == 12:
            _h8 = "H8" if GameMap[Locations.H8] == [] else SuspectColor[GameMap[Locations.H8][-1].name].value + "H8"
            _h9 = "H9" if GameMap[Locations.H9] == [] else SuspectColor[GameMap[Locations.H9][-1].name].value + "H9"
            _h10 = "H10" if GameMap[Locations.H10] == [] else SuspectColor[GameMap[Locations.H10][-1].name].value + "H10"
            mapString += Fore.WHITE + "4    " + _h8 + Fore.WHITE + "| |            " + _h9 + Fore.WHITE + "| |              |  |" + _h10 + Fore.WHITE + "\n"
        elif y_coord == 13:
            mapString += Fore.WHITE + "     __| |__          __| |__          __|  |___\n"
        elif y_coord == 14:
            mapString += Fore.WHITE + "    |       |________|       |________|         |\n"
        elif y_coord == 15:
            _conserv = "Conserv" if GameMap[Locations.Conservatory] == [] else SuspectColor[GameMap[Locations.Conservatory][-1].name].value + "Conserv"
            _h11 = "H11" if GameMap[Locations.H11] == [] else SuspectColor[GameMap[Locations.H11][-1].name].value + "H11"
            _ballroom = "Ball Room" if GameMap[Locations.Ballroom] == [] else SuspectColor[GameMap[Locations.Ballroom][-1].name].value + "Ball Room"
            _h12 = "H12" if GameMap[Locations.H12] == [] else SuspectColor[GameMap[Locations.H12][-1].name].value + "H12"
            _kitchen = "Kitchen" if GameMap[Locations.Kitchen] == [] else SuspectColor[GameMap[Locations.Kitchen][-1].name].value + "Kitchen"
            mapString += Fore.WHITE + "5   |"+ _conserv + Fore.WHITE + "___" + _h11 + Fore.WHITE + "___"+ _ballroom + Fore.WHITE + "___" + _h12 + Fore.WHITE + "___ "+ _kitchen +" |\n"
        elif y_coord == 16:
            mapString += Fore.WHITE + "    |_______|        |_______|        |_________|"
    return mapString

def convertToReference(self, playerName):
    if playerName == "Miss Scarlet":
        return ("Miss Scarlet")
    elif playerName == "Col. Mustard":
        return ("Colonel Mustard")
    elif playerName == "Mrs. White":
        return ("Mrs. White")
    elif playerName == "Mr. Green":
        return ("Mr. Green")
    elif playerName == "Mrs. Peacock":
        return ("Mrs. Peacock")
    elif playerName == "Prof. Plum":
        return ("Professor Plum")

class Suspects(Enum):
    MissScarlet = "Miss Scarlet"
    Col_Mustard = "Colonel Mustard"
    Mrs_White = "Mrs. White"
    Mr_Green = "Mr. Green"
    Mrs_Peacock = "Mrs. Peacock"
    Prof_Plum = "Professor Plum"
    EMPTY = "EMPTY"

class SuspectColor(Enum):
    MissScarlet = Fore.RED
    Col_Mustard = Fore.YELLOW
    Mrs_White = Fore.CYAN   # replace default white color
    Mr_Green = Fore.GREEN
    Mrs_Peacock = Fore.BLUE
    Prof_Plum = Fore.MAGENTA    # closest match to purple

class Locations(Enum):
    Study = 0,
    H1 = 1,
    Hall = 2,
    H2 = 3,
    Lounge = 4,
    H3 = 5,
    H4 = 6,
    H5 = 7,
    Library = 8,
    H6 = 9,
    BillardRoom = 10,
    H7 = 11,
    DiningRoom = 12,
    H8 = 13,
    H9 = 14,
    H10 = 15,
    Conservatory = 16,
    H11 = 17,
    Ballroom = 18,
    H12 = 19,
    Kitchen = 20
