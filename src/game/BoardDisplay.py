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
        self.displayText(120, self.screen.get_width()/2-750, self.screen.get_height()/2-80, textr)

        # Display the actual player and the separator
        self.displayActualPlayer()

        i=0
        for card in self.actualPlayer.hand:
            # Display the card
            x = self.screen.get_width()/2 - 630 + i*(self.WIDTHREGION+100)
            y = self.screen.get_height()/2+260
            card.dcard.display(x, y)  

            pos = pygame.mouse.get_pos()
            # Check the mouse position
            if card.dcard.clickIn(pos):
                # Add a larger border when the mouse is over the card
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)

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
            self.displayText(120, self.screen.get_width()/2-780, self.screen.get_height()/2-80, texts)

            # Display the actual player and the separator
            self.displayActualPlayer()
            
            self.checkSanctuaryCards(nbToAdd)  # Check if there is enough sanctuary cards in the stack
            for i in range(nbToAdd):
                # Display the card
                card = self.sanctuaryCards[i]
                x = (i+1)*(self.WIDTHSANCTUARY+20)-70
                y = self.screen.get_height()/2+260
                card.dcard.display(x, y)

                pos = pygame.mouse.get_pos()
                # Check the mouse position
                if card.dcard.clickIn(pos):
                    # Add a larger border when the mouse is over
                    r = pygame.Rect(x, y, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
                    pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)

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
            # No sanctuary cards to add, go to next player or next state
            self.next(State.REGION) 


    ## Override
    def chooseRegionCard(self) -> None:
        # Display the text
        textr = "Choose the region card you want :"
        self.displayText(120, self.screen.get_width()/2-700, self.screen.get_height()/2-80, textr)

        # Display the actual player and the separator
        self.displayActualPlayer()

        for i in range(self.nbJoueur+1-self.cpt): # Display number of players plus one region cards
            # Display the card
            card = self.regionCards[i]
            x = i*(self.WIDTHREGION+5)
            y = self.screen.get_height()/2+260
            card.dcard.display(x, y)

            # Check the mouse position
            pos = pygame.mouse.get_pos()
            if card.dcard.clickIn(pos):
                # Add a larger border when the mouse is over
                r = pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION)
                pygame.draw.rect(self.screen, (255,255,255), r, 7, border_radius=30)

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
                    

    ## Override
    def displayEnd(self) -> None:
        # If there is a right clic go to the next player so he can see his revealed cards
        if self.clic == 2:
            self.next(State.END)

        # Texts
        textScore = " Scores :"
        textSep = "___________"

        # Display texts
        dec = 700 - 80*len(self.players) # Offset for the display in height (depending of the number of players)
        self.displayText(200, self.screen.get_width()/2-280, dec, textScore)
        self.displayText(200, self.screen.get_width()/2-390, dec+30, textSep)

        # Sort the results by points
        dict = self.countFinalPoints()
        dictSorted = {key: dict[key] for key in sorted(dict, key=dict.get, reverse=True)}

        # Display the scores
        i=0 
        for pId, res in dictSorted.items():
            textPts = "Player " + str(pId) + " : " + str(res) 
            self.displayText(180, self.screen.get_width()/2-330, dec+220 + i*140, textPts)
            i+=1


    ## Display the revealed cards for the actual player
    def displayRevealedCard(self) -> None:
        # Fill the screen to only show the revealed cards        
        background = pygame.image.load("./data/img/background.png")
        background = pygame.transform.scale(background, (self.screenW, self.screenH))
        self.screen.blit(background, (0, 0))

        # Size police
        sizePol = 60

        # Text sanctuary cards
        texts = "Sanctuary cards :"
        self.displayText(sizePol, 10, 85+self.HEIGHTSANCTUARY/2, texts)

        # Text region cards
        textr = "Region cards :"
        self.displayText(sizePol, 10, self.HEIGHTSANCTUARY + 105 + self.HEIGHTREGION/2, textr) 

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
            x = self.screen.get_width()/2 - (l*(self.WIDTHSANCTUARY+30))/2 + i*(self.WIDTHSANCTUARY+30)
            card.dcard.display(x, y)
            i+=1
        

    ## Display some informations for the players
    def infoPlayers(self) -> None:
        # Display the actual player and the turn number
        textPl = "Actual Player : " + str(self.actualPlayer.id) + " | Turn number : "+str(self.nbTurns+1) + " | "
        self.displayText(60, 5, 5, textPl) 

        # Display the key bind and what it does
        textKeybind = "Press 's' to show your revealed cards"
        self.displayText(60, self.screen.get_width()/3, 5, textKeybind) 



    ## Create a rectangle to permit the player to close the pygame window
    def forceExit(self) -> None:
        # Create and draw the rectangle
        rect = pygame.Rect(self.screen.get_width()-50, 0, 50, 50)
        pygame.draw.rect(self.screen, (255,0,0), rect)

        # Add a cross in the rectangle
        textCr = "x"
        self.displayText(60, self.screen.get_width()-35, 2, textCr, (0,0,0))

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
                self.state = State.END
        elif self.state == State.END:
            self.displayEnd()


    ## Display the text at the given coordonate
    def displayText(self, sizePol:int, x:int, y:int, text:str, colTxt:tuple[int, int, int]=(255,255,255), pol:str=None) -> None:
        police = pygame.font.Font(pol, sizePol)
        texte_surface = police.render(text, True, colTxt)
        self.screen.blit(texte_surface, (x, y))  
        
    
    ## Display actual player with a separator
    def displayActualPlayer(self):
        # Display the separator
        textSep = "__________________________"
        self.displayText(100, self.screen.get_width()/2-500, self.screen.get_height()/2-150, textSep)

        # Display the actual player
        textPl = "Actual player : " + str(self.actualPlayer.id)
        self.displayText(120, self.screen.get_width()/2-320, self.screen.get_height()/2-180, textPl)

    

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


            # Execute the right function corresponding to the state
            self.execute()

            # Check is exit is pressed
            self.forceExit()

            # Check if the key bind is pressed and it is not the start
            if pygame.key.get_pressed()[pygame.K_s] and self.state != State.START:
                self.displayRevealedCard()

            # Display some informations if it is not the start
            if self.state != State.START:
                self.infoPlayers()
            
            # Check is the left clic is up (This permits to only detect a clic when it up after being down)
            if self.clic == 2:
                self.clic = 0

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60) / 1000

        pygame.quit()
        
        return