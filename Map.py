from Models.Locations import Locations
from Models.Suspects import Suspects, SuspectColor
from colorama import Fore

class Map:
    def __init__(self):
        # init the Game Map with all characters in-place
        # the map data will be stored as a 2D dictionary
        self.GameMap = {
            Locations.Study:[], Locations.H1:[], Locations.Hall:[], Locations.H2:[Suspects.MissScarlet], Locations.Lounge:[],
            Locations.H3:[Suspects.Prof_Plum], Locations.H4:[], Locations.H5:[Suspects.Col_Mustard],
            Locations.Library:[], Locations.H6:[], Locations.BillardRoom:[], Locations.H7:[], Locations.DiningRoom:[],
            Locations.H8:[Suspects.Mrs_Peacock], Locations.H9:[], Locations.H10:[],
            Locations.Conservatory:[], Locations.H11: [Suspects.Mr_Green], Locations.Ballroom:[], Locations.H12:[Suspects.Mrs_White], Locations.Kitchen:[]
        }
    
    # 
    def IsBlocked(self, location):
        """
        Return the location availability of the next move.

        This function can be used when the map is synced, or it will produce incorrect local result.

        @type  location: Models.Locations
        @param location: The location value of the next move.
        @rtype: bool
        @return: If the passage is blocked or not
        """
        suspect = self.GameMap.get(location)
        return suspect != []

    def RecordPlayersMove(self, suspect = Suspects.EMPTY, oldLocation = Locations.Void, newLocation = Locations.Void):
        """
        This function record the all players' move to the map.

        @type suspect: Models.Suspects
        @param suspect: The moved suspect

        @type oldLocation: Models.Locations
        @param oldLocation: The suspect's old location

        @type newLocation: Models.Locations
        @param newLocation: The suspect's new location
        """
        # remove the suspect from old location
        if suspect in self.GameMap[oldLocation]:
            self.GameMap[oldLocation].remove(suspect)
        else:
            # the old location is invalid, coule caused by not saving the location in previous move
            # attempt to find the suspect location
            for key in self.GameMap:
                if suspect in self.GameMap[key]:
                    self.GameMap[key].remove(suspect)
                    break
        # assign value to the new location
        self.GameMap[newLocation].append(suspect)

    def ToGUI(self):
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
                _study = "Study" if self.GameMap[Locations.Study] == [] else SuspectColor[self.GameMap[Locations.Study][-1].name].value + "Study"
                _h1 = "H1" if self.GameMap[Locations.H1] == [] else SuspectColor[self.GameMap[Locations.H1][-1].name].value + "H1"
                _hall = "Hall" if self.GameMap[Locations.Hall] == [] else SuspectColor[self.GameMap[Locations.Hall][-1].name].value + "Hall"
                _h2 = "H2" if self.GameMap[Locations.H2] == [] else SuspectColor[self.GameMap[Locations.H2][-1].name].value + "H2"
                _Lounge = "Lounge" if self.GameMap[Locations.Lounge] == [] else SuspectColor[self.GameMap[Locations.Lounge][-1].name].value + "Lounge"
                mapString += Fore.WHITE + "1   | " + _study + Fore.WHITE + "  ___" + _h1 + Fore.WHITE + "___  " + _hall + Fore.WHITE + "   ___" + _h2 + Fore.WHITE + "___  " + _Lounge + Fore.WHITE + "  |\n"
            elif y_coord == 4:
                mapString += Fore.WHITE + "    |__   __|        |__   __|        |__    ___|\n"
            elif y_coord == 5:
                mapString += Fore.WHITE + "       | |              | |              |  |\n"
            elif y_coord == 6:
                _h3 = "H3" if self.GameMap[Locations.H3] == [] else SuspectColor[self.GameMap[Locations.H3][-1].name].value + "H3"
                _h4 = "H4" if self.GameMap[Locations.H4] == [] else SuspectColor[self.GameMap[Locations.H4][-1].name].value + "H4"
                _h5 = "H5" if self.GameMap[Locations.H5] == [] else SuspectColor[self.GameMap[Locations.H5][-1].name].value + "H5"
                mapString += Fore.WHITE + "2    " + _h3 + Fore.WHITE + "| |            " + _h4 + Fore.WHITE + "| |              |  |" + _h5 + "\n"
            elif y_coord == 7:
                mapString += Fore.WHITE + "     __| |__          __| |__          __|  |___\n"
            elif y_coord == 8:
                mapString += Fore.WHITE + "    |       |________|       |________|         |\n"
            elif y_coord == 9:
                _library = "Library" if self.GameMap[Locations.Library] == [] else SuspectColor[self.GameMap[Locations.Library][-1].name].value + "Library"
                _h6 = "H6" if self.GameMap[Locations.H6] == [] else SuspectColor[self.GameMap[Locations.H6][-1].name].value + "H6"
                _billiard = "Billiard" if self.GameMap[Locations.BillardRoom] == [] else SuspectColor[self.GameMap[Locations.BillardRoom][-1].name].value + "Billiard"
                _h7 = "H7" if self.GameMap[Locations.H7] == [] else SuspectColor[self.GameMap[Locations.H7][-1].name].value + "H7"
                _dining = "Dining" if self.GameMap[Locations.DiningRoom] == [] else SuspectColor[self.GameMap[Locations.DiningRoom][-1].name].value + "Dining"
                mapString += Fore.WHITE + "3   |" + _library + Fore.WHITE + " ___" + _h6 + Fore.WHITE + "___ "+ _billiard + Fore.WHITE + "___"+ _h7 + Fore.WHITE + "___  " +_dining + Fore.WHITE + "  |\n"
            elif y_coord == 10:
                mapString += Fore.WHITE + "    |__   __|        |__   __|        |__    ___|\n"
            elif y_coord == 11:
                mapString += Fore.WHITE + "       | |              | |              |  |\n"
            elif y_coord == 12:
                _h8 = "H8" if self.GameMap[Locations.H8] == [] else SuspectColor[self.GameMap[Locations.H8][-1].name].value + "H8"
                _h9 = "H9" if self.GameMap[Locations.H9] == [] else SuspectColor[self.GameMap[Locations.H9][-1].name].value + "H9"
                _h10 = "H10" if self.GameMap[Locations.H10] == [] else SuspectColor[self.GameMap[Locations.H10][-1].name].value + "H10"
                mapString += Fore.WHITE + "4    " + _h8 + Fore.WHITE + "| |            " + _h9 + Fore.WHITE + "| |              |  |" + _h10 + Fore.WHITE + "\n"
            elif y_coord == 13:
                mapString += Fore.WHITE + "     __| |__          __| |__          __|  |___\n"
            elif y_coord == 14:
                mapString += Fore.WHITE + "    |       |________|       |________|         |\n"
            elif y_coord == 15:
                _conserv = "Conserv" if self.GameMap[Locations.Conservatory] == [] else SuspectColor[self.GameMap[Locations.Conservatory][-1].name].value + "Conserv"
                _h11 = "H11" if self.GameMap[Locations.H11] == [] else SuspectColor[self.GameMap[Locations.H11][-1].name].value + "H11"
                _ballroom = "Ball Room" if self.GameMap[Locations.Ballroom] == [] else SuspectColor[self.GameMap[Locations.Ballroom][-1].name].value + "Ball Room"
                _h12 = "H12" if self.GameMap[Locations.H12] == [] else SuspectColor[self.GameMap[Locations.H12][-1].name].value + "H12"
                _kitchen = "Kitchen" if self.GameMap[Locations.Kitchen] == [] else SuspectColor[self.GameMap[Locations.Kitchen][-1].name].value + "Kitchen"
                mapString += Fore.WHITE + "5   |"+ _conserv + Fore.WHITE + "___" + _h11 + Fore.WHITE + "___"+ _ballroom + Fore.WHITE + "___" + _h12 + Fore.WHITE + "___ "+ _kitchen +" |\n"
            elif y_coord == 16:
                mapString += Fore.WHITE + "    |_______|        |_______|        |_________|"
        return mapString

def main():
    map = Map()
    #print(map.IsBlocked(Locations.Conservatory))
    print ("Output to CLI")
    print(map.ToGUI())

    print ("Move MrsWhite From H12 to Ball Room")
    map.RecordPlayersMove(Suspects.Mrs_White, Locations.H12, Locations.Ballroom)
    print ("Output new map to CLI")
    print(map.ToGUI())

    print("try faulty old location. Move MrsWhite From H1 to H12")
    map.RecordPlayersMove(Suspects.Mrs_White, Locations.H1, Locations.H12)
    print ("Output new map to CLI")
    print(map.ToGUI())


if __name__ == '__main__':
    main()