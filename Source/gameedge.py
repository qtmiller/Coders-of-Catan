class GameEdge:
    ''' This class contains all attributes regarding game edges and methods for altering them

    To Do:
        - None
    '''
    def __init__(self,valid):
        ''' GameEdge.__init__() method

        Args:
            valid(bool): edge is valid if both adjacent vertices are valid

        Returns:
            {no return}
        '''
        self.valid = valid
        self.playerID = None

    def build(self, playerID):
        ''' builds a road if the edge is currently empty

        Args:
            player(int): playerID attempting to build road

        Returns:
            True if edge is empty and valid; False otherwise
        '''
        if self.valid == True and self.playerID == None:
            self.playerID = playerID
            return True
        else:
            return False
        

'''
debugging functions
'''
x = GameEdge(True)
##if x.buildRoad(0): print('Road Built')
##if not x.buildRoad(1): print('Road Blocked')
##y = GameEdge(False)
##y.buildRoad(3)
