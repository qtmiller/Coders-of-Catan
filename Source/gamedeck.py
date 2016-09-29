import random

from gamecard import GameCard

class GameDeck:
    '''This class holds all values and player data related to the card deck

    To Do:
        - devCardPlayed()
        - add cardSteal()
        - improve road building devCard execution
    '''
    def __init__(self, gamemaster, logger):
        ''' GameDeck.__init__() method

        Args:
            gamemaster(GameMaster): the gamemaster object to interact with
            logger(QuinnLogger): logging object to record to

        Returns:
            {no return}
        '''
        self.GM = gamemaster
        self.logger = logger
        self.resCards = [] # 19 for each resources
        self.resCodes = ['Br','Wo','Or','Wh','Sh']
        self.devCards = [] # knights, bountiful, monopoly, victory
        self.devCodes = ['Kn','Ye','Mo','Ro','Vi']
        self.largest_army = None

        for i in range(len(self.resCodes)):
            for j in range(19): #number of cards per resource
                self.resCards.append(GameCard(self.resCodes[i]))
        num = [14,2,2,2,5]
        for i in range(len(self.devCodes)):
            for j in range(num[i]):
                self.devCards.append(GameCard(self.devCodes[i]))
        

    def giveResources(self, resources):
        ''' assigns resource cards to players

        Args:
            resources[string]: 4x(1+) array with resources to give each player

        Returns:
            {no return}
        '''
        for i in range(len(resources)):
            line = 'Resources: '
            for j in range(len(resources[i])):
                if resources[i][j] in self.resCodes:
                    line += str(resources[i][j]) + ','
                    self.cardToPlayer(resources[i],i)
            line += ' to player ' + str(i)
##            self.logger.log(line)
    

    def playerHand(self, player = None):
        ''' returns resource cards in each players hand

        Args:
            (opt) player(int): player ID to not hide. other players' cards qill be replaced with a card count

        Returns:
            4x(1+) array with resCards of selected player and card counts for the others
        '''
        players = [[] for i in range(4)]
        for i in range(len(self.resCards)):
            if self.resCards[i].player != None:
                x = players[self.resCards[i].player].append(self.resCards[i].value)

        if player != None:
            for i in range(len(players)):
                if i != player:
                    players[i] = [len(players[i])]
                    
        return players


    def playerHandDev(self, player = None):
        ''' returns development cards in each players hand

        Args:
            (opt) player(int): player ID to not hide. other players' cards qill be replaced with a card count

        Returns:
            4x(1+) array with resCards of selected player and card counts for the others
        '''
        players = [[] for i in range(4)]
        for i in range(len(self.devCards)):
            if self.devCards[i].player != None and self.devCards[i].played == False: # need to rework this when time permits
                x = players[self.devCards[i].player].append(self.devCards[i].value)

        if player != None:
            for i in range(len(players)):
                if i != player:
                    players[i] = [len(players[i])]

        print(players)
        return players


    def trade(self, cards_a, cards_b, player_a, player_b):
        ''' transfers cards between two players hands

        Args:
            cards_a[str]: list of cars to take from player_a
            cards_b[str]: list of cards to take from player_b
            player_a: first player in transaction
            player_b: second playerin transaction (if neg trade with bank)

        Returns:
            True if trade successful, False otherwise
        '''
        ## player to player ##
        if player_b >=0:
            self.logger.log('Trade between ' + str(player_a) + ' and ' + str(player_b))
            if not self.cardCheck([cards_a], player_a):
                return False
            if not self.cardCheck([cards_b], player_b):
                return False
            self.cardFromPlayer([cards_a], player_a)
            self.cardToPlayer([cards_a], player_b)
            self.cardFromPlayer([cards_b], player_b)
            self.cardToPlayer([cards_b], player_a)
            return True
        ## player to bank ##
        elif player_b < 0:
            if not self.cardCheck([cards_a], player_a):
                return False
            self.cardFromPlayer([cards_a], player_a)
            self.cardToPlayer([cards_b], player_a)
            return True
        else:
            return False
        


    def cardToPlayer(self, cards, player):
        ''' assigns cards to a given player

        Note:
            - awards a random dev card

        Args:
            cards[str]: array of cards to assign a player
            player(int): player ID to assign cards to

        Returns:
            false if any errors occur
        '''
        for x in range(len(cards)):
            if cards[x] in self.resCodes:
                for i in range(len(self.resCards)):
                    if self.resCards[i].value == cards[x] and self.resCards[i].player == None:
                        self.resCards[i].player = player
                        self.logger.log('Giving ' + str(self.resCards[i].value) + ' to ' + str(player))
                        break
            elif cards[x] == 'Dev':
                drawIndex = random.randint(0,(len(self.devCards)-1))
                for i in range(len(self.devCards)):
                    if self.devCards[(drawIndex+i)%len(self.devCards)].player == None:
                        self.devCards[(drawIndex+i)%len(self.devCards)].player = player
                        self.logger.log('Giving ' + str(player) + ' ' + str(self.devCards[(drawIndex+i)%len(self.devCards)].value))
                        break
##        print(cards)
        return


    def cardFromPlayer(self, cards, player):
        ''' retracts resource cards from player

        Args:
            cards[str]: array of cards to retract from a player
            player(int): player ID to retract cards from

        Returns:
            false if player does not have cards
        '''
        for x in cards:
            if x in self.resCodes:
                for i in range(len(self.resCards)):
                    if self.resCards[i].value == x and self.resCards[i].player == player:
                        self.resCards[i].player = None
                        self.logger.log('Taking ' + str(self.resCards[i].value) + ' from ' + str(player))
                        break
            else:
                return False


    def cardCheck(self, cards, player):
        ''' verifies player has necessary cards to purchase an asset

        Args:
            cards[str]: array of cards required
            player(int): player ID to check

        Returns:
            true if player has necessary resources, false otherwise
        '''
        cards_c = list(cards)
        hand = self.playerHand(player)[player]
        for i in range(len(hand)):
            for j in range(len(cards_c)):
                if hand[i] == cards_c[j]:
                    cards_c.pop(j)
                    break
        if not cards_c:
            return True
        else:
            return False


    def countResCards(self): # for debugging
        ''' just used for debugging. remove from final version

        Args:
            {no args}

        Returns:
            {no return}
        '''
        cardCount = [0 for i in range(len(self.resCodes))]
        for i in range(len(self.resCodes)):
            for j in range(len(self.resCards)):
                if self.resCards[j].value == self.resCodes[i] and self.resCards[j].player == None:
                    cardCount[i] += 1
        return cardCount


    def stealCard(self, seed, from_player, to_player): 
        ''' takes a random resource card from one player and gives it to another

        Args:
            seed(int): the card selection from stealing player
            from_player(int): the player being stolen from
            to_player(int): the player being rewarded

        Returns:
            True if successful, else False
        '''
        ## determine card ##
        from_cards = []
        for i in self.resCards:
            if i.player == from_player:
                from_cards.append(i)
        if not len(from_cards):
            return False
        card = from_cards[int((len(from_cards)-1)%seed)]
        ## transfer card ##
        self.logger.log(str(to_player) + ' stole from ' + str(from_player))
        self.cardFromPlayer([card.value], from_player)
        self.cardToPlayer([card.value], to_player)
        return True


    def playDevCard(self, card, player, extras=None):
        ''' executes actions relevant to a player dev card

        Args:
            card[str]: dev card to be played
            player(int): player ID to check if card available
            extras[variant]: varies depending on dev card see inline comments for each type

        Returns:
            true if player card played successfully, false otherwise
        '''
        ## Card check ##
        for i in range(len(self.devCards)):
##            print(str(self.devCards[i].value == card) + ',' + str(self.devCards[i].player == player) + ',' + str(self.devCards[i].played == False) + ',')
            if self.devCards[i].value == card and self.devCards[i].player == player and self.devCards[i].played == False:
                self.logger.log(str(player) + ' played a ' + card)
                print('dev card played ' + card)
                if card == 'Kn': # extras = None. postion selection handled by usual player method
                    self.GM.moveRobber(player)
                elif card == 'Ye': # extras = [res,res]. 2 resources to add to player hand
                    self.cardToPlayer(extras, player)
                elif card == 'Mo': # extras = res. all active cards of res given to player
                    for i in range(4):
                        if i != player:
                            while self.cardFromPlayer(extras, i):
                                  self.cardToPlayer(extras, player)
                elif card == 'Ro': # extras = [[x,y],[x1,y1]]. positions for new road
                    return self.GM.devCardRoad(player, extras)
                elif card == 'Vi': # extras = None. not applicable
                    # only needs to be marked played. no action required
                    pass
                else:
                    return False
                self.devCards[i].played = True
##                self.logger.log(str(player) + ' played ' + card)
##                z += 1
                return True
        return False


    def calcVPs(self):
        ''' returns victory points from cards 

        Args:
            {no args}

        Returns:
            4x1 array of victory points per player
        '''
        ## count victory point and knight cards ##
        playerVPs = [0 for i in range(4)]
        knights = [0 for i in range(4)]
        for i in range(len(self.devCards)):
            current_card = self.devCards[i]
            if (self.devCards[i].value == 'Vi') and (self.devCards[i].player != None) and (self.devCards[i].played == True):
                playerVPs[self.devCards[i].player] += 1
            elif self.devCards[i].value == 'Kn' and self.devCards[i].player != None and self.devCards[i].played == True:
                knights[self.devCards[i].player] += 1
        ## determine largest army ##
        most, most2nd = 0,0
        most_i, most2nd_i = None,None
        for i in range(len(knights)):
            if knights[i] >= most:
                most2nd = most
                most2nd_i = most_i
                most = knights[i]
                most_i = i
        if most > most2nd and most >= 3:
            self.largest_army = most_i
        ## award largest army ##
        if self.largest_army != None:
            playerVPs[self.largest_army] += 2
        
        return playerVPs
    

##from gamemaster import GameMaster
##from quinnlogger import QuinnLogger
##testGM = GameMaster()
##testLogger = QuinnLogger()
##BuildTest = GameDeck(testGM, testLogger)


'''
Testing Deck add/subtract functions
'''
##x = GameDeck(testLogger)
##x.cardToPlayer(['Sh'],0)
##x.cardToPlayer(['Wh'],0)
##x.cardToPlayer(['Sh','Or','Wh'],1)
##print(x.countResCards())
##x.giveResources([['Wh'],['Or','Sh','Fo'],['Br'],[]])
##print(x.playerHands())
##print(x.countResCards())
##x.cardFromPlayer(['Wh'],0)
##print(x.playerHands(1))
##print(x.countResCards())
##print(x.buyRequest(['Sh','Or'],1))
##print(x.buyRequest(['Or','Br'],1))


##BuildTest.logger.closeLogFile()




