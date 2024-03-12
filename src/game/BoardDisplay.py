import sys
import json
import pygame
from random import shuffle
import time

sys.path.append("./src/player/")
sys.path.append("./src/card/")
sys.path.append("./src/enum/")
sys.path.append("./src/display/card/")
sys.path.append("./src/display/")

from Board import Board
from Triangle import Triangle
from State import State
from Colors import Colors
from Quest import Quest
from Stones import Stones
from Player import Player
from RegionCard import RegionCard
from SanctuaryCard import SanctuaryCard
from ConditionModes import ConditionModes
from RegionCardDisplay import RegionCardDisplay
from SanctuaryCardDisplay import SanctuaryCardDisplay
from CardDisplay import CardDisplay
from ChooseNbPlayer import ChooseNbPlayer

## The class which represents the display of the game
class BoardDisplay(Board):
    
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.screenW = info.current_w
        self.screenH = info.current_h

        self.screen = pygame.display.set_mode((self.screenW, self.screenH), pygame.FULLSCREEN)
        pygame.display.set_caption("Projet - Far Away")
        self.clock = pygame.time.Clock()
        super().__init__(self.screen, self.screenW, self.screenH)

        self.running = True

        self.nbJoueur = 2
    
        self.state = State.START

        self.clic = 0

        self.actualPlayer = None
        self.cpt = 0

        self.starting = []

        self.scores = {}

        self.sizePol = self.screenW//18

    ## Override
    def chooseNbPlayers(self) -> None:
        nbJ = ChooseNbPlayer(self.screen, super().MAXIMUMPLAYERS, super().MINIMUMPLAYERS).display(self.nbJoueur, self.clic)
        self.nbJoueur = nbJ[1]
        if nbJ[0]:
            for i in range(1,self.nbJoueur+1):
                self.players.append(Player(i))
                for j in range(3):
                    card = self.regionCards.pop(0)
                    self.players[i-1].addCardToHand(card)
            self.actualPlayer = self.players[self.cpt]
            self.state = State.REVEAL

    ## Change the actual player and, if it has to, to the next state
    def next(self, state) -> bool:
        self.cpt += 1
        # Check if the actual player is the last
        if self.cpt < self.nbJoueur:   
            self.actualPlayer = self.players[self.cpt]
            return False
        else:
            self.cpt = 0
            self.actualPlayer = self.players[self.cpt]
            self.state = state  # Go to the next state 
            return True

    ## Override
    def chooseCardToReveal(self) -> None:
        # Display the text
        textr = "Choose the card you want to reveal :"
        self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.4, textr)

        # Display the actual player and the separator
        self.displayActualPlayer()

        i=0
        for card in self.actualPlayer.hand:
            # Display the card
            cardAndEc = self.WIDTHREGION + self.WIDTHREGION*0.25
            x = self.screenW/2 - (1.5*cardAndEc)*0.94 + i*cardAndEc
            y = self.screenH - self.HEIGHTREGION*1.5
            card.dcard.display(x, y)  

            pos = pygame.mouse.get_pos()
            # Check the mouse position
            if card.dcard.clickIn(pos):
                # Add a larger border when the mouse is over the card
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=CardDisplay.border_radius)

                # Check the mouse clic
                if self.clic==2:
                    n = self.actualPlayer.revealCard(i+1)
                    self.starting.append((self.actualPlayer, n))

                    # Go to next player or next state and change the list of player with the right order for next state
                    if self.next(State.SANCTUARY):
                        self.starting.sort(key=lambda x : x[1])
                        self.players = [t[0] for t in self.starting]
                        self.starting = []
                        self.actualPlayer = self.players[0]
            i+=1
            

    ## Override
    def chooseSanctuaryCard(self) -> None:
        nbToAdd = self.actualPlayer.sanctuaryCardToAdd() # Number of sanctuary cards to choose between
    
        if nbToAdd > 0:
            # Display the text
            texts = "Choose the sanctuary card you want :"
            self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.4, texts)

            # Display the actual player and the separator
            self.displayActualPlayer()

            self.checkSanctuaryCards(nbToAdd)  # Check if there is enough sanctuary cards in the stack
            for i in range(nbToAdd):
                # Display the card
                card = self.sanctuaryCards[i]
                x = (i+1)*(self.WIDTHSANCTUARY+20)-70
                y = self.screenH - self.HEIGHTSANCTUARY*1.5
                card.dcard.display(x, y)

                pos = pygame.mouse.get_pos()
                # Check the mouse position
                if card.dcard.clickIn(pos):
                    # Add a larger border when the mouse is over
                    r = pygame.Rect(x, y, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
                    pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=CardDisplay.border_radius)

                    # Check the mouse clic
                    if self.clic==2:
                        # Add the selected card to the player's sanctuary cards
                        self.actualPlayer.addCardToSanctuaryCards(self.sanctuaryCards.pop(i))

                        # Add the other ones showed before to the stack for used ones
                        for j in range(nbToAdd-1):
                            self.sanctuaryCardsUsed.append(self.sanctuaryCards.pop(0))
                        self.next(State.REGION) # Go to next player or next state
                        break
        else:
            # No sanctuary cards to add for this player, go to next player or next state
            self.next(State.REGION) 


    ## Override
    def chooseRegionCard(self) -> None:
        # Display the text
        textr = "Choose the region card you want :"
        self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.4, textr)

        # Display the actual player and the separator
        self.displayActualPlayer()

        lgth = self.nbJoueur+1-self.cpt
        for i in range(lgth): # Display number of players plus one region cards
            # Display the card
            card = self.regionCards[i]

            nbCardOnRow = lgth # Number of cards to display on the row
            
            # If there is too much card display them in 2 rows
            if lgth > 4:
                y = 0
                if i < 4:
                    y = self.screenH - self.HEIGHTREGION*2.14
                    nbCardOnRow = 4
                else:
                    y = self.screenH - self.HEIGHTREGION*1.07
                    nbCardOnRow = lgth - 4
            else:
                y = self.screenH - self.HEIGHTREGION*1.5
            
            x = self.screenW/2 - (nbCardOnRow*(self.WIDTHREGION+30))/2 + (i%4)*(self.WIDTHREGION+30)
            card.dcard.display(x, y)

            # Check the mouse position
            pos = pygame.mouse.get_pos()
            if card.dcard.clickIn(pos):
                # Add a larger border when the mouse is over
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=CardDisplay.border_radius)

                # Check the click
                if self.clic==2:
                    # Add the card to the player hand
                    self.actualPlayer.addCardToHand(self.regionCards.pop(i))

                    # Go the next player or next state and put back the player in order of their id 
                    if self.next(State.REVEAL):
                        self.nbTurns += 1
                        self.regionCards.pop(0) # Delete the region that left 
                        self.players.sort(key=lambda p : p.id)
                        self.actualPlayer = self.players[0]
                        break # Stop the loop because the card has been chosen
                    

    ## Override
    def displayEnd(self) -> None:
        # If there is a right clic go to the next player so he can see his revealed cards
        if self.clic == 2:
            self.next(State.END)

        # Texts
        textScore = " Scores :"
        textSep = "___________"

        # Display texts
        dec = self.screenH*0.5 - self.screenH*0.05*len(self.players) # Offset for the display in height (depending of the number of players)
        sizePol = int(self.sizePol*1.6)
        self.displayText(sizePol, self.screenW*0.5, dec, textScore)
        self.displayText(sizePol, self.screenW*0.5, dec+self.screenH*0.04, textSep)

        # Sort the results by points
        self.scores = {key: self.scores[key] for key in sorted(self.scores, key=self.scores.get, reverse=True)}

        # Display the scores
        i=0 
        for pId, res in self.scores.items():
            textPts = "Player " + str(pId) + " : " + str(res) 
            self.displayText(sizePol, self.screenW/2, dec + self.screenH*0.15 + i*self.screenH*0.1, textPts)
            i+=1


    ## Display the revealed cards for the actual player
    def displayRevealedCard(self) -> None:
        # Fill the screen to only show the revealed cards        
        background = pygame.image.load("./data/img/background.png")
        background = pygame.transform.scale(background, (self.screenW, self.screenH))
        self.screen.blit(background, (0, 0))

        # Size police
        sizePol = self.sizePol//2

        # Text sanctuary cards
        texts = "Sanctuary cards :"
        self.displayText(sizePol, sizePol*3.2, self.HEIGHTSANCTUARY*0.7, texts)

        # Text region cards
        textr = "Region cards :"
        self.displayText(sizePol, sizePol*2.5, self.HEIGHTSANCTUARY + self.HEIGHTREGION*0.8, textr) 

        # Display region cards
        i=0
        for card in self.actualPlayer.revealedCards:
            y = 0
            # Display the cards in 2 different rows
            if i > 3:
                y = 140 + self.HEIGHTSANCTUARY + self.HEIGHTREGION
            else :
                y = self.HEIGHTSANCTUARY + 110
            x = (i%4)*(self.WIDTHREGION+30) + (self.WIDTHREGION*0.95)
            card.dcard.display(x, y)
            i+=1

        # Display sanctuary cards
        i=0
        l = len(self.actualPlayer.sanctuaryCards)
        for card in self.actualPlayer.sanctuaryCards:
            y = 70 
            x = self.screenW/2 - (l*(self.WIDTHSANCTUARY+30))/2 + i*(self.WIDTHSANCTUARY+30)
            card.dcard.display(x, y)
            i+=1
        

    ## Display some informations for the players
    def infoPlayers(self) -> None:
        # Display the actual player, the turn number and the key bind
        turn = " | "
        if self.state == State.END:
            turn += "Game is finished" 
        else:
            turn += "Turn number : "+str(self.nbTurns+1)

        textKeybind = "Press 's' to show your revealed cards"

        textPl = "Actual Player : " + str(self.actualPlayer.id) + turn + " | " + textKeybind

        sizePol = self.sizePol//2
        self.displayText(sizePol, sizePol*12.15, sizePol*0.4, textPl) 



    ## Create a rectangle to permit the player to close the pygame window
    def forceExit(self) -> None:
        # Create and draw the rectangle
        rect = pygame.Rect(self.screenW-50, 0, 50, 50)
        pygame.draw.rect(self.screen, (255,0,0), rect)

        # Check the mouse position and clic
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos[0], pos[1]) and self.clic == 1:
            self.running = False


    ## Call the function corresponding to the actual state
    def execute(self) -> None:
        if self.nbTurns == 8:
            self.state = State.END
        if self.state == State.START:
            self.chooseNbPlayers()
        elif self.state == State.REVEAL:
            self.chooseCardToReveal()
        elif self.state == State.SANCTUARY:
            self.chooseSanctuaryCard()
        elif self.state == State.REGION:
            # Players don't choose region card when it is the last turn
            if self.nbTurns < 7:
                self.chooseRegionCard()
            else:
                self.state = State.COMPUTE
        elif self.state == State.COMPUTE:
            self.computeScores()
        elif self.state == State.END:
            self.displayEnd()


    ## Compute the final scores for each player
    def computeScores(self) -> None:
        # Get the final points for each player
        self.scores = self.countFinalPoints()
        self.state = State.END


    ## Display the text at the given coordonate
    def displayText(self, sizePol:int, x:int, y:int, text:str, colTxt:tuple[int, int, int]=(255,255,255), pol:str=None) -> None:
        police = pygame.font.Font(pol, sizePol)
        texte_surface = police.render(text, True, colTxt)
        self.screen.blit(texte_surface, (x-texte_surface.get_width()/2, y-texte_surface.get_height()/2))  
        
    
    ## Display actual player with a separator
    def displayActualPlayer(self):
        # Display the separator
        textSep = "__________________________"
        self.displayText(self.sizePol-10, self.screenW/2, self.screenH - self.HEIGHTREGION*2.7, textSep)

        # Display the actual player
        textPl = "Actual player : " + str(self.actualPlayer.id)
        self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.8, textPl)

    

    ## Play the game
    def play(self) -> None:
        while self.running :

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Check is the left clic is donw
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.clic = 1

                # Check if the left clic is up
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clic == 1:
                    self.clic = 2

            # fill the screen with a color to wipe away anything from last frame
            background = pygame.image.load("./data/img/background.png")
            background = pygame.transform.scale(background, (self.screenW, self.screenH))
            self.screen.blit(background, (0, 0))
            

            # Check is exit is pressed
            self.forceExit()

            # Check if the key bind is pressed and it is not the start
            if pygame.key.get_pressed()[pygame.K_s] and self.state != State.START:
                self.displayRevealedCard()
            else:
                # Execute the right function corresponding to the state
                self.execute()

            # Display some informations if it is not the start
            if self.state != State.START:
                self.infoPlayers()
            
            # Check is the left clic is up (This permits to only detect a clic when it is up after being down)
            if self.clic == 2:
                self.clic = 0

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60) / 1000

        pygame.quit()
        
        return