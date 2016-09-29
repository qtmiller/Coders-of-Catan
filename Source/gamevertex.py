class GameVertex:
    ''' This class contains all attributes regarding game vertices and methods for altering them

    To Do:
        - Change building parameter from string to enum. Better practice
    '''
    def __init__(self, valid):
        ''' GameVertex.__init__() method

        Args:
            valid(bool): vertex is valid if at least one adjacent tile is land

        Returns:
            {no return}
        '''
        self.valid = valid
        self.building = None
        self.playerID = None

    def build(self, building, playerID):
        ''' Handles building of a settlement or city

        Args:
            building(str): the desired building to be built
            playerID(int): sets the terrain type of the game hex

        Returns:
            True if building meets requirements; False if any pre-requisite fails
        '''
##        print('Build call: ' + str(self.building) + ' to ' + building + ' play/own: ' + str(playerID) + '/' + str(self.playerID))
        if self.playerID == None and building == 'Settlement':
            self.building = building
            self.playerID = playerID
##            print('vertex settle')
            return True
        elif self.playerID == playerID and self.building == 'Settlement' and building == 'City':
            self.building = building
            return True
        else:
            return False


'''
Debugging code
'''
x=GameVertex(True)
