import datetime

class QuinnLogger:
    ''' This class will handle creating the log file for each Catan game

    To Do:
        - None
    '''
    def __init__(self):
        ''' QuinnLogger.__init__() method

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.turn = 0
        self.player = -1
        current_time = datetime.datetime.now()
        filename = current_time.strftime('../Games/%y%m%d_%H%M%S')+'.txt'
##        print(filename)
        self.logfile = open(filename, 'w')

    def printHeader(self, playerlist):
        ''' adds necessary information to recreate the match

        Args:
            playerlist[str]: list of player script names

        Returns:
            {no return}
        '''
        self.logfile.write('Coders of Catan Game\n')
        line = 'Scripts list: '
        for i in range(len(playerlist)):
            line += playerlist[i] + ','
        line += '\n\n'
        self.logfile.write(line)


    def printMap(self, hexes):
        ''' writes map configuration used to text file

        Note:
            - GameTile may be changed to GameHex object
        
        Args:
            hexes(GameTile): 2d array of all hexes used for map

        Returns:
            {no return}
        '''
        #print(hexes.terrain)
        self.logfile.write('Resources\n')
        for i in range(len(hexes)):
            for j in range(len(hexes[i])):
##                print(hexes[i][j].terrain)
                self.logfile.write(str(hexes[i][j].terrain) + ',')
            self.logfile.write('\n')
        self.logfile.write('Numbers\n')
        for i in range(len(hexes)):
            for j in range(len(hexes[i])):
                self.logfile.write(str(hexes[i][j].number) + ',')
            self.logfile.write('\n')
        self.logfile.write('\n')

    def log(self, msg):
        ''' adds line to game log file with [turn, player] stamp

        Args:
            msg(str): message to be logged

        Returns:
            {no return}
        '''
        self.logfile.write('['+str(self.turn)+','+str(self.player)+']: ' + msg + '\n')


    def startGame(self):
        ''' denotes start of game in log file

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.logfile.write('\n\nStart Game:\n')
        self.nextTurn()


    def nextPlayer(self):
        ''' records player changes and increments turn if necessary

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.player += 1
        if self.player >=4:
            self.player = self.player%4
            self.nextTurn()
        self.logfile.write('Start player: ' + str(self.player) + '\n')


    def nextTurn(self):
        ''' records turn changes

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.turn += 1
        self.logfile.write('Start turn: ' + str(self.turn) + '\n')


    def endGame(self, playerVPs):
        ''' records end of game statistics

        Args:
            playerVPs[int]: array of victory points for each player

        Returns:
            {no return}
        '''
        self.logfile.write('\n Game Over:\n')
        line = 'Final Score: '
        for i in range(len(playerVPs)):
                line += str(playerVPs[i]) + ', '
        self.logfile.write('Final Score: ' + line.strip(', '))
        self.closeLogFile()


    def closeLogFile(self):
        ''' closes and saves log file

        Note:
            - game will not be saved unless log file is closed out. Not sure if mem leaks possible.

        Args:
            {no args}

        Returns:
            {no return}
        '''
        self.logfile.close()


##BuildTest = QuinnLogger()

'''
Function test
'''
##x = QuinnLogger()
##x.printHeader(['play 1','play 2','play 3','play 4'])
##x.startGame()
##x.nextPlayer()
##x.log('testing 1 2 3 bitches')
##x.log('same player new message')
##x.nextPlayer()
##x.log('new player same message')
##x.nextPlayer()
##x.nextPlayer()
##x.nextPlayer()
##x.nextPlayer()
##x.closeLogFile()
