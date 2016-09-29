class GameTile:
    ''' This class contains all attributes regarding game hexes and methods for altering them

    To Do:
        - change all instances of tile to hex. Better terminology
        - modify string parameters to enum types. Better practice
    '''
    def __init__(self, terrain, number):
        ''' GameTile.__init__() method

        Args:
            terrain(str): sets the terrain type of the game hex
            number(int): sets the resource roll number of the tile

        Returns:
            {no return}
        '''
        self.terrain = terrain
        self.number = int(number)

        ## Match the resource reward to the tiles terrain ##
        terrain_to_resource = {
            'Hi': 'Br',
            'Fo': 'Wo',
            'Mo': 'Or',
            'Fi': 'Wh',
            'Pa': 'Sh'}
        self.resource = terrain_to_resource.get(self.terrain, None)

        ## Check if terrain tile is land or sea ##
        if self.terrain in ['Hi','Fo','Mo','Fi','Pa','De']:
            self.land = True
        else:
            self.land = False

        ## Place initial robber. could be moved to gameboard for instances with 2 desserts ##
        if self.terrain == 'De':
            self.robber = True
        else:
            self.robber = False

    def addRobber(self):
        ''' Sets robber value True

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.robber = True

    def removeRobber(self):
        ''' Sets robber value False

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.robber = False

'''
debugging functions
'''
##x = GameTile('Fo',5)
##print('Terrain: ' + x.terrain)
##print('Number: ' + str(x.number))
##print('Is land: ' + str(x.land))
##print('Robber: ' + str(x.robber))
##print('Adding robber')
##x.addRobber()
##print('Robber: ' + str(x.robber))
##x.removeRobber()
##print('Robber: ' + str(x.robber))
##print()
##
##y = GameTile('De',0)
##print('Terrain: ' + y.terrain)
##print('Number: ' + str(y.number))
##print('Is land: ' + str(y.land))
##print('Robber: ' + str(y.robber))
##print()
##
##z = GameTile('Se',0)
##print('Terrain: ' + z.terrain)
##print('Number: ' + str(z.number))
##print('Is land: ' + str(z.land))
##print('Robber: ' + str(z.robber))
##    
##    
##
