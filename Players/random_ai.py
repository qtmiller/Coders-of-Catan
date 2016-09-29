import random

class BasePlayer:
    ''' This class contains all logic for a player.

    Note:
        - do not change the names of any existing methods
    
    To Do:
        - incomingTrade()
        - beginTurn() (eg. turn logic)
    '''
    def __init__(self, gamemaster, GBview, playerID):
        ''' BasePlayer.__init__() method

        Args:
            gamemaster:(GameMaster): gamemaster object to interact with
            GBview(GameBoardView): game board view to interact with
            playerID: this player's ID number

        Returns:
            {no return}
        '''
        self.GM = gamemaster
        self.GBview = GBview
        self.playerID = playerID
##        print('Player created')


    def initialPlacement(self):
        ''' determines initial settlement and road postions

        Args:
            {no args}

        Returns:
            true when done
        '''
        x,y = None, None
        ## pick random settlement location ##
        while(True):
            x = random.randint(0,len(self.GBview.vertices)-1)
            y = random.randint(0,len(self.GBview.vertices[x])-1)
            ## check if valid and empty ##
##            print(str(x) + ',' + str(y))
            if self.GBview.vertices[x][y].valid and self.GBview.vertices[x][y].playerID == None:
                if self.GM.buy('Settlement',[x,y]):
                    ## find adj edges ##
                    adj = self.GBview.vertEdges([x,y])
                    self.GM.buy('Road',adj[random.randint(0,len(adj)-1)])
                    break
        return True


    def incomingTrade(self, trade_offer):
        ''' decides whether to accept, modify, or reject incoming trade offer

        Args:
            trade_offer[variant]: details of trade [[offer to player], [want from player], opp player ID]

        Returns:
            counter trade offer [[offer to opp], [want from opp], self player ID], or false
        '''
##        print(trade_offer)
##        print(str(self.playerID) + ': incoming trade')
        ## if # of offer cards = # of want cards ##
##        if len(trade_offer[0]) != len(trade_offer[1]):
##            return False
        ## 50/50 chance of accepting ##
        if not random.randint(0,1):
##            print(str(self.playerID) + ': accepting trade')
            return [trade_offer[1],trade_offer[0],self.playerID]
        ## return trade or false ##
        return False


    def selectTrade(self, trade_offers):
        ''' selects between competing counter offers to trade

        Args:
            trade_offer[variant]: details of trade [[offer to player], [want from player], other player ID]

        Returns:
            int index of selected trade in offers list
        '''
##        print(str(self.playerID) + ': select trade')
        ## select random option if #offer == #want ##
##        for i in trade_offers[:]:
##            if i[0] != i[1]:
##                trade_offers.remove(i)
        return random.randint(0,len(trade_offers)-1)


    def moveRobber(self):
        ''' selects location to move robber and cards to steal

        Args:
            {no args}

        Returns:
            robber move [[location x,y], card seed, opp ID]
        '''
        ## pick random opponent settlement ##
        x,y,settle_player = None,None,None
        while(True):
            x = random.randint(0,len(self.GBview.vertices)-1)
            y = random.randint(0,len(self.GBview.vertices[x])-1)
            settle_player = self.GBview.vertices[x][y].playerID
            if (settle_player != None) and (settle_player != self.playerID):
                break
        ## place on random tile near opp settle ##
        tiles = self.GBview.vertTiles([x,y])
        location = tiles[random.randint(0,len(tiles)-1)]
        
        ## pick random card from player ##
        seed = random.randint(1,20)

        return [location, seed, settle_player]


    def over7Cards(self):
        ''' selects cards to throwaway

        Args:
            {no args}

        Returns:
            str array of cards to throwaway
        '''
        ## randomly select cards to throwaway ##
        hands = self.GM.playerHand(self.playerID)
        throwaway = []
        num_cards = len(hands[self.playerID])
        for j in range(int(num_cards/2)):
            throwaway.append(hands[self.playerID][random.randint(0,num_cards-1)])
##        print('Player ' + str(self.playerID))
##        print(hands)
##        print(throwaway)
        return throwaway


    def beginTurn(self):
        ''' main turn logic

        Args:
            {no args}

        Returns:
            return to end turn
        '''
        buildings = ['Settlement','City','Road','Dev']
        build_cost = [['Br','Wo','Wh','Sh'],['Wh','Wh','Or','Or','Or'],['Br','Wo'],['Or','Wh','Sh']]
        resCodes = ['Br','Wo','Or','Wh','Sh']
        ## randomly select build option ##
        hand = self.GM.playerHand(self.playerID)[self.playerID]
        for i in range(len(build_cost)):
            hand_c = list(hand)
            for j in range(len(build_cost[i])):
                card_check = False
                for k in range(len(hand_c)):
                    if hand_c[k] == build_cost[i][j]:
                        hand_c.pop(k)
                        card_check = True
                        break
                if not card_check:
                    break
                else:
                    if buildings[i] == 'Road':
                        if not random.randint(0,5):
                            self.build(buildings[i])
                    else:
                        self.build(buildings[i])

            
        ## if any res, rand chance to offer trade. offer 1 for 1 ##
        hand = self.GM.playerHand(self.playerID)[self.playerID]
        if len(hand):
            ## chance to offer trade ##
            if not random.randint(0,3):
                offer = hand[random.randint(0,len(hand)-1)]
                want = []
                while(True):
                    want = resCodes[random.randint(0,len(resCodes)-1)]
                    if want != offer:
                        break
##                print(str(self.playerID) + ': offering trade')
                self.GM.trade(offer, want)

        ## rand chance (~10%) to play any dev cards in hand ##
        if (True): # always plays for testing purposes
            dev_cards = self.GM.playerHandDev(self.playerID)[self.playerID]
##            print(dev_cards)
            if dev_cards:
                card = dev_cards[random.randint(0,len(dev_cards)-1)]
                if card == 'Kn':
                    self.GM.playDevCard(card) # No extras needed. positioning handled by player .moveRobber()
                elif card == 'Ye':
                    extras = []
                    for i in range(2):
                        extras.append(resCodes[random.randint(0,len(resCodes)-1)])
                    self.GM.playDevCard(card, extras) # The resources to take from pile
                elif card == 'Mo':
                    extras = resCodes[random.randint(0,len(resCodes)-1)]
                    self.GM.playDevCard(card, [extras]) # resource type to steal from all players
                elif card == 'Ro':
                    extras = []
                    for j in range(2):
                        for i in range(100): # limited to prevent lockup
                            x = random.randint(0,len(self.GBview.edges)-1)
                            y = random.randint(0,len(self.GBview.edges[x])-1)
                            if self.GBview.edges[x][y].playerID == self.playerID:
                                verts = self.GBview.edgeVerts([x,y])
                                edges = self.GBview.vertEdges(verts[random.randint(0,len(verts)-1)])
                                [x1,y1] = edges[random.randint(0,len(edges)-1)]
                                if x1 != x and y1 != y:
                                    if self.GBview.edges[x1][y1].playerID == None:
                                        extras.append([x1,y1])
                                        break
                    print(extras)
                    self.GM.playDevCard(card, extras) # two coordinates for roads to be built
                elif card == 'Vi':
                    self.GM.playDevCard(card) # no extras required. card is only played

        return


    def build(self, item):
        ''' this is just to separate the location selection logic form the main logic

        Args:
            building(str): type of building to buy

        Returns:
            {no return}
        '''
        if item == 'Settlement':
            for i in range(20):
                x = random.randint(0,len(self.GBview.edges)-1)
                y = random.randint(0,len(self.GBview.edges[x])-1)
                if self.GBview.edges[x][y].playerID == self.playerID:
                    verts = self.GBview.edgeVerts([x,y])
                    [x1,y1] = verts[random.randint(0,len(verts)-1)]
                    if self.GBview.vertices[x1][y1].playerID == None:
                        self.GM.buy(item,[x,y])
                        return
        elif item == 'City':
            for i in range(20):
                x = random.randint(0,len(self.GBview.vertices)-1)
                y = random.randint(0,len(self.GBview.vertices[x])-1)
                if self.GBview.vertices[x][y].playerID == self.playerID:
                    self.GM.buy(item,[x,y])
                    return
        elif item == 'Road':
            for i in range(20):
                x = random.randint(0,len(self.GBview.edges)-1)
                y = random.randint(0,len(self.GBview.edges[x])-1)
                if self.GBview.edges[x][y].playerID == self.playerID:
                    verts = self.GBview.edgeVerts([x,y])
                    edges = self.GBview.vertEdges(verts[random.randint(0,len(verts)-1)])
                    [x1,y1] = edges[random.randint(0,len(edges)-1)]
                    if x1 != x and y1 != y:
                        if self.GBview.edges[x1][y1].playerID == None:
                            self.GM.buy(item,[x1,y1])
                            return
        elif item == 'Dev':
            self.GM.buy(item)
            return


## BuildTest = BasePlayer()
