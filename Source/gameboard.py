import os

from gametile import GameTile
from gamevertex import GameVertex
from gameedge import GameEdge

##from gamecard import GameCard
##
##from quinnlogger import QuinnLogger


class GameBoardView:
    ''' This class isolates the players from the gameboard itself

    To Do:
        - Add input checks to all board utility functions
    '''

    def __init__(self, gameboard):
        ''' GameBoardView.__init__() method

        Note:
            this class just copies the data and useful util methods from the GameBoard supplied

        Args:
            gameboard(GameBoard): the GameBoard object to be copied

        Returns:
            {no return}
        '''
        self.__gameboard = gameboard
        self.tiles = self.__gameboard.tiles
        self.vertices = self.__gameboard.vertices
        self.edges = self.__gameboard.edges


    def update(self):
        ''' refreshes the map data from the gameboard

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.tiles = self.__gameboard.tiles
        self.vertices = self.__gameboard.vertices
        self.edges = self.__gameboard.edges


    def calcVPs(self):
        ''' calulates victory points for each player

        Args:
            {no args}

        Returns:
            array with number of victory points per player
        '''
        players = [0 for i in range(4)]

        for r in range(len(self.vertices)):
            for c in range(len(self.vertices)):
                if self.vertices[r][c].playerID!= None:
                    if self.vertices[r][c].building == 'Settlement':
                        players[self.vertices[r][c].player] += 1
                    elif self.vertices[r][c].building == 'City':
                        players[self.vertices[r][c].player] += 2
##        print(players)
        return players


    def maritimeTrade(self, cards, playerID):
        ''' verifies if a maritime trade is valid

        Args:
            cards[str]: list of cards being offered
            playerID(int): player attempting to make trade

        Returns:
            True if port available, False otherwise
        '''
        for i in cards:
            for j in cards:
                if i != j:
                    return False

        if len(cards) == 3:
            port_required = 'Z3'
        elif len(cards) == 2:
            port_required = 'Z' + cards[0][0]
        else:
            return False
        
        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i])):
                if j.playerID == playerID:
                    for [x,y] in self.vertTiles([i,j]):
                        if self.tiles[x][y].terrain == port_required:
                            return True
        return False


    def tileVerts(self, hexTile):
        ''' calulates adjacent vertices for a given tile

        Args:
            hexTile[[int,]]: coordinate pair of given tile

        Returns:
            array with coordinates of adjacent vertices
        '''
        ## add input check ##
        [r,c] = hexTile
        tileVert = []
        if (r%2) == 0:
            for x in range(r-1,r+1):
                for y in range((c-1)*2,2*c+1):
                    tileVert.append([x,y])
        elif (r%2) == 1:
            for x in range(r-1,r+1):
                for y in range(2*c-1,2*c+2):
                    tileVert.append([x,y])
##        print(tileVert)
        return tileVert


    def tileEdges(self, hexTile):
        ''' calulates adjacent edges for a given tile

        Args:
            hexTile[int]: coordinate pair of given tile

        Returns:
            array with coordinates of adjacent edges
        '''
        ## add input check ##
        tileEdge = []
        [r,c] = hextile
        if (r%2) == 0:
            for x in {(r-1)*2,r*2}:
                for y in {(c-1)*2,2*c-1}:
                    tileEdge.append([x,y])
            for y in range(c-1,c+1):
                tileEdge.append([2*r-1,y])
        elif (r%2) == 1:
            for x in {(r-1)*2,r*2}:
                for y in {c*2-1,2*c}:
                    tileEdge.append([x,y])
            for y in range(c-1,c+1):
                tileEdge.append([2*r-1,y])
        for [x,y] in tileEdge[:]:
                if (x < 0 or y < 0) or (x >= len(self.edges)) or (((x%2) == 0 and y >= len(self.edges[0])) or ((x%2) == 1 and (y >= 6))):
                    tileEdge.remove([x,y])
##        print(tileEdge)
        return tileEdge


    def vertTiles(self, vertex):
        ''' calulates adjacent tiles for a given vertex

        Args:
            vert[int]: coordinate pair of given vertex

        Returns:
            array with coordinates of adjacent tiles
        '''
        ## add input check ##
        vertTile = []
        [r,c] = vertex
        if ((r%2) == 0 and (c%2) == 0) or ((r%2) == 1 and (c%2) == 1):
            x = [r,r,r+1]
            y = [int(c/2),int(c/2)+1,int((c+1)/2)]
            for i in range(len(x)):
                vertTile.append([x[i],y[i]])
        else:
            x = [r,r+1,r+1]
            y = [int((c+1)/2),int(c/2),int(c/2)+1]
            for i in range(len(x)):
                vertTile.append([x[i],y[i]])
        for [x,y] in vertTile[:]:
                if (x < 0 or x >= len(self.tiles)) or (y < 0 or y >= len(self.tiles[0])):
                    vertTile.remove([x,y])
##        print(vertTile)
        return vertTile


    def vertEdges(self, vertex):
        ''' calulates adjacent edges for a given vertex

        Args:
            vertex[int]: coordinate pair of given vertex

        Returns:
            array with coordinates of adjacent edges
        '''
        ## add input check ##
        vertEdge = []
        [r,c] = vertex
        if ((r%2) == 0 and (c%2) == 0) or ((r%2) == 1 and (c%2) == 1):
            x = [2*r-1,2*r,2*r]
            y = [int(c/2),c-1,c]
            for i in range(len(x)):
                vertEdge.append([x[i],y[i]])
        else:
            x = [2*r,2*r,2*r+1]
            y = [c-1,c,int(c/2)]
            for i in range(len(x)):
                vertEdge.append([x[i],y[i]])
        for [x,y] in vertEdge[:]:
                if (x < 0 or y < 0) or (x >= len(self.edges)) or (((x%2) == 0 and y >= len(self.edges[0])) or ((x%2) == 1 and (y >= 6))):
                    vertEdge.remove([x,y])
##        print(vertEdge)
        return vertEdge


    def edgeTiles(self, edge):
        ''' calulates adjacent tiles for a given edge

        Args:
            edge[int]: coordinate pair of given edge

        Returns:
            array with coordinates of adjacent tiles
        '''
        ## add input check ##
        edgeTile = []
        x = []
        y = []
        [r,c] = edge
        if (r%2) == 0:
            x = [int(r/2),int(r/2+1)]
            if (r%4) == 0:
                if (c%2) == 0:
                    y = [int(c/2+1),int(c/2)]
                elif (c%2) == 1:
                    y = [int(c/2+1),int(c/2+1)]
            else:
                if (c%2) == 0:
                    y = [int(c/2),int(c/2+1)]
                elif (c%2) == 1:
                    y = [int(c/2+1),int(c/2+1)]
        elif (r%2) == 1:
            x = [int(r/2+1),int(r/2+1)]
            y = [c,c+1]
        for i in range(len(x)):
            edgeTile.append([x[i],y[i]])

##        print(edgeTile)
        return edgeTile


    def edgeVerts(self, edge):
        ''' calulates adjacent vertices for a given edge

        Args:
            edge[int]: coordinate pair of given edge

        Returns:
            array with coordinates of adjacent vertices
        '''
        ## add input check ##
        edgeVert = []
        x = []
        y = []
        [r,c] = edge
        if (r%2) == 0:
            x = [int(r/2),int(r/2)]
            y = [c,c+1]
        elif (r%2) == 1:
            x = [int(r/2),int(r/2+1)]
            y = [int(2*c),int(2*c)]
        for i in range(len(x)):
            edgeVert.append([x[i],y[i]])
##        print(edgeVert)        
        return edgeVert



class GameBoard:
    ''' This class holds all variables related to the game board and deck. Also verifies player actions related to the Game Board.

    Note:
        - It will be extendable for player scripts to add other board related matrices. (resource value, settlement priority, etc.)
        - could clean up the calculations by using tileVertex et al methods. And you might as well add input checks to tileVertex et al while you're at it.

    To Do:
        - add longest road calculator
        - add maritime trade verify function
        - add # of building check to build function (5 settle, 4 city, X roads)
    
    '''
    def __init__(self, logger):
        ''' GameBoardView.__init__() method

        Note:
            currently only reads the Settlers of Catan recommended starting map from memory

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.logger = logger
        
        # import resources tiles (class and values)
        self.tiles = [[0 for i in range(7)] for j in range(7)]
        self.vertices = [[None for i in range(12)] for j in range(6)]
        self.edges = [[None for i in range(11)] for j in range(11)]
        
        file_dir = os.path.dirname(os.path.realpath('__file__'))
        game_tile_file = os.path.join(file_dir,'..\Resources\gametiles.txt')

        with open(game_tile_file,'r') as f:
            tiles_terrain = [[None for i in range(len(self.tiles[0]))] for j in range(len(self.tiles))]
            tiles_numbers = [[None for i in range(len(self.tiles[0]))] for j in range(len(self.tiles))]

            while(True):
                line = f.readline()
                #print(line)
                
                if 'Terrain' in line:
                    for i in range(len(self.tiles)):
                        line = f.readline()
                        line = line.strip('\n')
                        tiles_terrain[i] = line.split(',')

                if 'Numbers' in line:
                    for i in range(len(self.tiles)):
                        line = f.readline()
                        line = line.strip('\n')
                        tiles_numbers[i] = line.split(',')

                if not line:
                    break

##            print('Resource map:')
##            print(tiles_terrain)
##            print('Numbers:')
##            print(tiles_numbers)

            for r in range(len(self.tiles)):
                for c in range(len(self.tiles[r])):
                    self.tiles[r][c] = GameTile(tiles_terrain[r][c],tiles_numbers[r][c])
                
        # calculate vertices
        for r in range(len(self.vertices)):
            for c in range(len(self.vertices[r])):
##                print(str(r) + ', ' + str(c))
                if (r%2) == 0:
                    if (c%2) == 0:
                        if self.tiles[r][int(c/2)].land or self.tiles[r][int(c/2)+1].land or self.tiles[r+1][int(c/2)].land:
                            self.vertices[r][c] = GameVertex(True)
                        else:
                            self.vertices[r][c] = GameVertex(False)
                    else:
                        if self.tiles[r][int((c+1)/2)].land or self.tiles[r+1][int((c-1)/2)].land or self.tiles[r+1][int((c+1)/2)].land:
                            self.vertices[r][c] = GameVertex(True)
                        else:
                            self.vertices[r][c] = GameVertex(False)
                elif (r%2) == 1:
                    if (c%2) == 0:
                        if self.tiles[r][int(c/2)].land or self.tiles[r+1][int(c/2)].land or self.tiles[r+1][int(c/2)+1].land:
                            self.vertices[r][c] = GameVertex(True)
                        else:
                            self.vertices[r][c] = GameVertex(False)
                    else:
                        if self.tiles[r][int((c-1)/2)].land or self.tiles[r][int((c+1)/2)].land or self.tiles[r+1][int((c+1)/2)].land:
                            self.vertices[r][c] = GameVertex(True)
                        else:
                            self.vertices[r][c] = GameVertex(False)
        ## Debug ##
##        for r in range(len(self.vertices)):
##            line = '['
##            for c in range(len(self.vertices[r])):
##                line += str(self.vertices[r][c].valid)
##                if c != range(len(self.vertices[r])):
##                    line += ','
##            line += ']'
##            print(line)

                            
        # calculate edges
        for r in range(len(self.edges)):
            for c in range(len(self.edges[r])):
##                print(str(r) + ', ' + str(c))
                if (r%2) == 0:
                    if self.vertices[int(r/2)][c].valid and self.vertices[int(r/2)][c+1]:
                        self.edges[r][c] = GameEdge(True)
                    else:
                        self.edges[r][c] = GameEdge(False)
                elif (r%2) == 1:
                    if (c < 6) and self.vertices[int((r-1)/2)][int(2*c+1)].valid and self.vertices[int((r+1)/2)][int(2*c+1)]:
                        self.edges[r][c] = GameEdge(True)
                    else:
                        self.edges[r][c] = GameEdge(False)

        self.logger.printHeader(['1','2','3','4'])
        self.logger.printMap(self.tiles)
        self.GBview = GameBoardView(self)


    def build(self, player, building, position, initial=False):
        ''' verifies build request and returns true if build successful

        Args:
            player(int): Id of player looking to build
            building(str): name of requested building
            position[int]: coordinates of requested building
            (opt) initial(bool): set true to ignore settlement road check

        Returns:
            true if build successful, false otherwise
        '''
        [r,c] = position
        if building == 'Settlement':
            road_check = False
            settle_check = True
            for [x,y] in self.GBview.vertEdges([r,c]):
                if self.edges[x][y].playerID == player:
                    road_check = True
                for [x1,y1] in self.GBview.edgeVerts([x,y]):
                    if self.vertices[x1][y1].playerID != None:
                        settle_check = False
            if settle_check and (road_check or initial):
                if (self.vertices[r][c].build('Settlement',player)):
                    self.logger.log('Player ' + str(player) + ' built a ' + building + ' at ' + str(position[0]) + ',' + str(position[1]))
                    print('Settlement Built')
                    self.GBview.update()
                    return True
                else:
                    return False
            else:
                return False
        elif building == 'City':
            if (self.vertices[r][c].build('City',player)):
                self.logger.log('Player ' + str(player) + ' built a ' + building + ' at ' + str(position[0]) + ',' + str(position[1]))
                print('City Built')
                self.GBview.update()
                return True
            else:
                return False
        elif building == 'Road':
            settle_check = False
            road_check = False
            for [x,y] in self.GBview.edgeVerts([r,c]):
                if self.vertices[x][y].playerID == player:
                    settle_check = True
                    break
                for [x1,y1] in self.GBview.vertEdges([x,y]):
                    if self.edges[x1][y1].playerID == player:
                        road_check = True
                        break
            if road_check or settle_check:
                if self.edges[r][c].build(player):
                    self.logger.log('Player ' + str(player) + ' built a ' + building + ' at ' + str(position[0]) + ',' + str(position[1]))
                    print('Road Built')
                    self.GBview.update()
                    return True
                else:
                    return False
        else:
            return False


    def getGBview(self):
        ''' returns GameBoardView for GameMaster

        Args:
            {no args}

        Returns:
            GameBoardView object
        '''
        return self.GBview


    def resourceRoll(self, roll):
        ''' calculates reqources to award each player for a given roll

        Args:
            roll(int): result of dice roll

        Returns:
            4 long list array with all resources to award
        '''
        player_resources = [[] for i in range(4)]

        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[r])):
##                print(str(r) + ',' + str(c) + ': ' + str(self.tiles[r][c].number) + ' v ' + str(roll))
                if self.tiles[r][c].number == roll:
##                    print(str(self.tiles[r][c].resource))
                    tileVert = self.GBview.tileVerts([r,c])
                    for [x,y] in tileVert:
                        if self.vertices[x][y].playerID != None:
                            if self.vertices[x][y].building == 'City':
                                player_resources[self.vertices[x][y].playerID].extend([self.tiles[r][c].resource])
##                                print('Bonus City Resource')
                            player_resources[self.vertices[x][y].playerID].extend([self.tiles[r][c].resource])
##        print(player_resources)
        return player_resources

    
    def calcVPs(self):
        ''' calculates victory points for each player on the board

        Args:
            {no args}

        Returns:
            4x1 array with points for each player
        '''
        playerVPs = [0 for i in range(4)]

        for r in range(len(self.vertices)):
            for c in range(len(self.vertices[r])):
                if self.vertices[r][c].playerID != None:
                    if self.vertices[r][c].building == 'Settlement':
                        playerVPs[self.vertices[r][c].playerID] += 1
                    elif self.vertices[r][c].building == 'City':
                        playerVPs[self.vertices[r][c].playerID] += 2
##        print(playerVPs)
        return playerVPs


    def moveRobber(self, location):
        ''' moves the robber from one space to hex to another

        Args:
            location[int]: new location to place the robber

        Returns:
            {no return}
        '''
        ## Add input check ##
        [x,y] = location
        ## remove robber ##
        for r in range(len(self.tiles)):
            for c in range(len(self.tiles[r])):
                if self.tiles[r][c].robber == True:
                    self.tiles[r][c].robber = False
                    break
        ## place robber ##
        self.tiles[x][y].robber == True
        return


'''
Build Test
'''
##testLogger = QuinnLogger()
##buildTest = GameBoard(testLogger)
##testLogger.closeLogFile()


'''
Test Resource Rolls
'''
##x = GameBoard()
##if(x.build(0,'Settlement',0,3)):print('success')
##else: print('failure')
##if(x.build(0,'Settlement',0,5,True)):print('success')
##else: print('failure')
##if(x.build(1,'Road',3,2)):print('success')
##else: print('failure')
##if(x.build(1,'Settlement',1,4,True)):print('success')
##else: print('failure')
##if(x.build(1,'Road',3,2)):print('success')
##else: print('failure')
##if(x.build(1,'Road',4,3)):print('success')
##else: print('failure')
##if(x.build(1,'City',1,4)):print('success')
##else: print('failure')
##if(x.build(2,'Settlement',1,8)):print('success')
##else: print('failure')
##if(x.build(3,'Settlement',2,8)):print('success')
##else: print('failure')
##print(x.resourceRoll(10)) ## 1,2 & 2,5
##x.buildingVictoryPoints()

'''
Test tileEdges function
'''
##y = GameBoard()
##y.tileEdges(2,3)
##y.tileEdges(2,6)
##y.tileEdges(1,3)
##y.tileEdges(1,6)

'''
Test vertTiles function
'''
##x = GameBoard()
##x.vertTiles(1,6)
##x.vertTiles(2,6)
##x.vertTiles(1,5)
##x.vertTiles(2,5)

'''
Test vertEdges function
'''
##x = GameBoard()
##x.vertEdges(1,5)
##x.vertEdges(2,6)
##x.vertEdges(1,6)
##x.vertEdges(2,5)
##x.vertEdges(2,11)
##x.vertEdges(2,0)

'''
Test edgeTiles function
'''
##x = GameBoard()
##x.edgeTiles(4,5)
##x.edgeTiles(4,6)
##x.edgeTiles(2,5)
##x.edgeTiles(2,6)
##x.edgeTiles(3,3)

'''
Test edgeVerts function
'''
##x = GameBoard()
##x.edgeVerts(2,3)
##x.edgeVerts(4,3)
##x.edgeVerts(3,3)





##BTgb = GameBoard()
##Buildtest = GameBoardView(BTgb)

##x = GameBoardView(BTgb)
##print(x.tiles)
##print(x.vertices)
##print(x.edges)


















