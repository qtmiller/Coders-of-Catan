##
##  This script will control a game of 4 player settlers
##
##
##
##

import importlib.util
import os
import random
import datetime

from quinnlogger import QuinnLogger
from gameboard import GameBoard
from gamedeck import GameDeck


class GameMaster:
    ''' This class controls the flow of a game and is responsible for verifying player actions

    Note:
        - once the class is called it will run through a whole game without further input
    
    To Do:
        - GameLoop()
        - trade()
        - calcVPs()
    '''
    def __init__(self):
        ''' GameMaster.__init__() method

        Args:
            {no args}

        Returns:
            {no return}
        '''
        ## create log file ##
        self.logger = QuinnLogger()
        
        ## load player list ##
        playerScriptNames = []
        with open('../Resources/playerlist.txt','r') as f:
            while(True):
                line = f.readline()
                if not line: break
                line = line.strip('\n')
                playerScriptNames.append(line+'.py')
##        print(playerScriptNames)
        random.shuffle(playerScriptNames)
        self.logger.printHeader(playerScriptNames)
        
        ## generate board ##
        self.gameBoard = GameBoard(self.logger)
        ## generate boardView ##
        self.GBview = self.gameBoard.getGBview()
        ## generate deck ##
        self.gameDeck = GameDeck(self, self.logger)

        ## initiate players ##
        self.players = []
        self.player = 0
        playersPath = os.path.join(os.getcwd(),'../Players/')
        for i in range(4):
            playerFilePath = playersPath + playerScriptNames[i]
            spec = importlib.util.spec_from_file_location('Players.'+playerScriptNames[i].strip('.py'),playerFilePath)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            self.players.append(mod.BasePlayer(self, self.GBview, i))
##        print(self.players)

        self.player_turns = 0
        random.seed(datetime.datetime.timestamp(datetime.datetime.now()))
        ## call loop function ##
        self.gameLoop()
        pass


    def gameLoop(self):
        ''' Manages flow of game until 10 victory points are earned by a player

        Args:
            {no args}

        Returns:
            {no return}
        '''
        ## initial placement ##
        self.initial_setup = True
        for i in range(len(self.players)):
            self.player = i
            while(True):
                if self.players[self.player].initialPlacement():
                    break
        for i in range(len(self.players)):
            self.player = 3-i
            while(True):
                if self.players[self.player].initialPlacement():
                    break
        self.initial_setup = False
        ## start loop ##
        self.logger.startGame()
        print('Start Game')
        playerVPs = self.calcVPs()
        while (max(playerVPs)<10 and (self.player_turns < (4*300))):
            self.logger.nextPlayer()
            ## resource roll ##
            die_1 = random.randint(1,6)
            die_2 = random.randint(1,6)
            res_roll = die_1 + die_2
            self.logger.log('Resource Roll: ' + str(die_1) + '+' + str(die_2) + '=' + str(res_roll))
            ## handle robber rolls ##
            if res_roll == 7:
                ## count/discard player cards ##
##                print('robber roll')
                hands = self.gameDeck.playerHand()
                for i in range(len(hands)):
                    if len(hands[i]) > 7:
                        discard = self.players[i].over7Cards()
##                        print(discard)
                        self.gameDeck.cardFromPlayer(discard, i)
                ## have player move robber ##
                robber_move = self.players[self.player].moveRobber()
                self.gameBoard.moveRobber(robber_move[0])
                ## player draws card from adjacent players ##
                self.gameDeck.stealCard(robber_move[1],robber_move[2], self.player)
            else:
                self.gameDeck.giveResources(self.gameBoard.resourceRoll(res_roll))
            ## call player turnFunc ##
            self.players[self.player].beginTurn()
            ## wait for player to return func ##
            
            ## calc VP and log ##
            playerVPs = self.calcVPs()
##            playerVPs_string = [(str(playerVPs[i]) + ', ') for i in range(len(playerVPs))]
            line = 'Victory Points: '
            for i in range(len(playerVPs)):
                line += str(playerVPs[i]) + ', '
            self.logger.log(line.strip(', '))
            ## increment player ##
            self.player += 1
            self.player = self.player % 4
            self.player_turns += 1
            if not (self.player_turns % (4*10)): print(int(self.player_turns/4)) # for debugging

        ## log final state ##
        self.logger.endGame(playerVPs)


    def moveRobber(self, player=None):
        ''' requests desired robber location from player

        Args:
            player(int): player that gets to choose robber location

        Returns:
            {no return}
        '''
        choice = [] # format [[x,y],card_select_seed,opponentID]
        if player == None:
            player = self.player
        choice = self.players[self.player].moveRobber()
        self.gameBoard.moveRobber(choice[0])
##        print(choice)
        self.gameDeck.stealCard(choice[1], choice[2], player)
        return

    def trade(self, offer, want, wantPlayer=[]):
        ''' broadcasts trade offer to all players unless certain player specified

        Args:
            offer[str]: list of resources player is offering
            want[str]: list of resources player wants in return
            (opt) wantPlayer[int]: list of players to offer trade to. if blank, all players receive offer

        Returns:
            True if trade successful, False otherwise
        '''
        ## determine if broadcast or specific ##
##        print('GM.trade called')
        counter_offers = []
        if wantPlayer == []:
            wantPlayer = [i for i in range(4)]
            wantPlayer.remove(self.player)
        ## trade with bank ##
        elif wantPlayer[0] < 0:
            return self.gameDeck.trade(offer, want, self.player, wantPlayer[0])
        ## loop through other players with offer if they have the cards ##
        for i in wantPlayer:
            if self.gameDeck.cardCheck([want], i):
                counterOffer = self.players[i].incomingTrade([offer, want, self.player])
                if counterOffer:
                    counter_offers.append(counterOffer)
        ## if no one accepts return false, if one accepts make trade and return true, if multiple accept return all offers to initial player ##
##        print(counter_offers)
        if len(counter_offers):
            trade_choice = self.players[self.player].selectTrade(counter_offers)
##            print(trade_choice)
            if trade_choice < 0:
##                print('trade declined')
                return False
            else:
##                print('trade accepted')
                return self.gameDeck.trade(counter_offers[trade_choice][0], counter_offers[trade_choice][1], counter_offers[trade_choice][2], self.player)
        else:
            return False


    def buy(self, item, location=None):
        ''' handles plurchase requests by player.

        Args:
            item[str]: item player wishes to purchase. options are ['Road','Settlement','City','Dev']
            (opt) location[int]: location to build item. Not necessary for dev cards

        Returns:
            True if build successful, False otherwise
        '''
        ## verify player has resources ##
        ## give dev card or attempt build ##
            ## remove res cards ##
        ## Breakdown request ##
##        print(location)
        buildCost = [['Br','Wo','Wh','Sh'],['Wh','Wh','Or','Or','Or'],['Br','Wo'],['Or','Wh','Sh']]
        if item == 'Road':
            if self.initial_setup:
                return self.gameBoard.build(self.player,item,location,self.initial_setup)
            else:
                if self.gameDeck.cardCheck(buildCost[2],self.player):
                    if self.gameBoard.build(self.player, item, location):
                        self.gameDeck.cardFromPlayer(buildCost[2],self.player)
                        return True
                return False
        elif item == 'Settlement':
            if self.initial_setup:
                return self.gameBoard.build(self.player,item,location,self.initial_setup)
            else:
                if self.gameDeck.cardCheck(buildCost[0],self.player):
                    if self.gameBoard.build(self.player,item, location):
                        self.gameDeck.cardFromPlayer(buildCost[0],self.player)
                        return True
                return False
        elif item == 'City':
            if self.gameDeck.cardCheck(buildCost[1],self.player):
                if self.gameBoard.build(self.player,item, location):
                    self.gameDeck.cardFromPlayer(buildCost[1],self.player)
        elif item == 'Dev':
            if self.gameDeck.cardCheck(buildCost[3],self.player):
                self.logger.log('Trying to buy dev card')
                self.gameDeck.cardToPlayer([item], self.player)
                self.gameDeck.cardFromPlayer(buildCost[3],self.player)
                return True
        else:
            return False


    def playerHand(self, playerID):
        ''' returns player hand

        Args:
            playerID(int): player ID to lookup
            
        Returns:
            4x(1+) array of player resCards. card count for other player cards
        '''
        return self.gameDeck.playerHand(playerID)


    def playerHandDev(self, playerID):
        ''' returns player dev cards

        Args:
            playerID(int): player ID to lookup
            
        Returns:
            4x(1+) array of player resCards. card count for other player cards
        '''
        return self.gameDeck.playerHandDev(playerID)


    def playDevCard(self, card_value, extras=None):
        ''' passes dev card play request to gameDeck

        Args:
            card[str]: dev card to be played
            extras[variant]: varies depending on dev card see gamedeck.py for inline comments for each type

        Returns:
            true if player card played successfully, false otherwise
        '''
        return self.gameDeck.playDevCard(card_value, self.player, extras)


    def devCardRoad(self, player, locations):
        ''' attempts to build 2 roads

        Note:
            only to be called by gameDeck. I should really find a better way to implement this.

        Args:
            location[[int,int]]: pair of edge coordinates to build roads at

        Returns:
            true if both roads built successfully, false otherwise
        '''
        try:
            self.gameBoard.build(player, 'Road', locations[0])
            self.gameBoard.build(player, 'Road', locations[1])
        except:
            self.logger.log('Error in devCardRoad function')
            return False
    

    def calcVPs(self):
        ''' calculate total victory points for all players

        Args:
            {no args}
            
        Returns:
            4x1 array with victory points per player
        '''
        ## get GameBoard VPs ##
        GB = self.gameBoard.calcVPs()
        ## get Deck VPs ##
        deck = self.gameDeck.calcVPs()
        ## Sum ##
        playerVPs = [(GB[i] + deck[i]) for i in range(len(GB))]
        return playerVPs
    

BuildTest = GameMaster()
BuildTest.logger.closeLogFile()




































        
    
