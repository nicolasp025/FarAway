import sys
import json
import pygame
import pygame_textinput
from random import shuffle
import time
import math

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
    
    # The size max for the pseudo
    MAXPSEUDO = 16

    # The speed for the animation
    SPEED = 50

    # Number of frames max for the animation
    NBFRAMESMAX = 4

    # The default number of players
    default_number_of_players = 2

    def __init__(self):
        pygame.init()

        # Get the screen's informations
        info = pygame.display.Info()
        self.screenW = info.current_w
        self.screenH = info.current_h

        # Set the screen
        self.screen = pygame.display.set_mode((self.screenW, self.screenH), pygame.FULLSCREEN)
        pygame.display.set_caption("Projet - Far Away")
        self.clock = pygame.time.Clock()

        super().__init__(self.screen, self.screenW, self.screenH)

        # Set the running variable to True for the play method
        self.running = True 

        # Number of players (default 2)
        self.nbJoueur = self.default_number_of_players
    
        # State of the game (set to start for the beginning)
        self.state = State.START

        # State of the clic (0 for nothing, 1 for down, 2 for up)
        self.clic = 0

        # Actual player
        self.actualPlayer = None

        # Counter for the players
        self.cpt = 0

        # List that will be used to sort the players for the next state
        self.starting = []

        # Scores of the players
        self.scores = {}

        # Size of the police 
        self.sizePol = self.screenW//18

        # Pseudo of the player
        self.pseudo = ""

        # Animation for the cards (true when the cards are moving)
        self.animation = True

        # Coordinates for the animation (actual x and y for each card)
        self.x_anim = []
        self.y_anim = []

        # Temporary score
        self.tmpScore = 0

        # The number of the player that have their scores displayed
        self.nbPlScores = 0

        # Number of frames passed for the next animation frame
        self.nbFramesPassed = 0


    ## Override
    def chooseNbPlayers(self) -> None:
        nbJ = ChooseNbPlayer(self.screen, super().MAXIMUMPLAYERS, super().MINIMUMPLAYERS).display(self.nbJoueur, self.clic)
        self.nbJoueur = nbJ[1]
        if nbJ[0]:
            for i in range(1,self.nbJoueur+1):
                self.players.append(Player(i))
                # Add 3 cards to the hand of each player
                for j in range(3):
                    card = self.regionCards.pop(0)
                    self.players[i-1].addCardToHand(card)
            self.actualPlayer = self.players[self.cpt]
            self.state = State.PSEUDO
            # setup the coordinates for the animation 
            self.setupAnimationCoordinates(True, len(self.actualPlayer.hand))

    ## Setup the coordinates for the animation
    def setupAnimationCoordinates(self, reveal:bool=False, len:int=0) -> None:
        # Set the coordinates for the animation depending of the state
        if reveal:
            self.x_anim = [[self.screenW//2 - self.WIDTHREGION//2, self.screenW//2 - self.WIDTHSANCTUARY//2] for i in range(len)]
            self.y_anim = [[self.screenH - self.HEIGHTREGION//2, self.screenH - self.HEIGHTSANCTUARY//2] for i in range(len)]
        else:
            self.x_anim = [[self.screenW*0.26, self.screenW*0.55] for i in range(max(len, self.nbJoueur+1))]
            self.y_anim = [[-self.HEIGHTREGION*0.5, -self.HEIGHTSANCTUARY*0.5] for i in range(max(len, self.nbJoueur+1))]
 
    ## Choose the pseudo of the player
    def enterPseudo(self) -> str:
        police = pygame.font.Font(None, self.sizePol)
        texte_saisie = police.render("Player "+str(self.actualPlayer.id)+", Choose your pseudo : " + self.pseudo, True, (255,255,255))
        rect_texte = texte_saisie.get_rect()
        rect_texte.center = (self.screenW // 2, self.screenH // 2)
        self.screen.blit(texte_saisie, rect_texte)
        
        ## Get the key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Check if the pseudo is not empty
                    if (self.pseudo != ""):
                        self.actualPlayer.addPseudo(self.pseudo)
                        self.pseudo = ""
                        self.next(State.REVEAL)
                elif event.key == pygame.K_BACKSPACE:
                    # Delete the last character
                    self.pseudo = self.pseudo[:-1]
                else:
                    # Add the character to the pseudo
                    if len(self.pseudo) < self.MAXPSEUDO:
                        if event.unicode.isalpha() or event.unicode.isdigit():
                            self.pseudo += event.unicode


    ## Change the actual player and, if it has to, the next state
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

        if self.animation:
            self.animateCard(len(self.actualPlayer.hand), 0)
            # Display the actual player and the separator
            self.displayActualPlayer()
        else:
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

                        # Add the player and the number of the card revealed
                        self.starting.append((self.actualPlayer, n))

                        self.animation = True # Activate the animation
                        # Go to next player or next state and change the list of player with the right order for next state
                        if self.next(State.SANCTUARY):
                            # Sort the players by the card revealed's number
                            self.starting.sort(key=lambda x : x[1])
                            self.players = [t[0] for t in self.starting]
                            self.starting = []
                            self.actualPlayer = self.players[0]
                            self.setupAnimationCoordinates()
                i+=1
            

    ## Override
    def chooseSanctuaryCard(self) -> None:
        nbToAdd = self.actualPlayer.sanctuaryCardToAdd() # Number of sanctuary cards to choose between

        if nbToAdd > 0:
            # Display the text
            texts = "Choose the sanctuary card you want :"
            self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.4, texts)

            self.checkSanctuaryCards(nbToAdd)  # Check if there is enough sanctuary cards in the stack

            if self.animation:
                self.animateCard(nbToAdd, 1)
                # Display the actual player and the separator
                self.displayActualPlayer()
            else:
                # Display the actual player and the separator
                self.displayActualPlayer()
                for i in range(nbToAdd):
                    # Display the card
                    card = self.sanctuaryCards[i]
                    x, y = self.calculateCoordinateSanctuary(i, nbToAdd)
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
                            self.animation = True # Activate the animation
                            break
        else:
            # No sanctuary cards to add for this player, go to next player or next state
            self.next(State.REGION) 


    ## Calculate the coordinate for the sanctuary cards
    def calculateCoordinateSanctuary(self, i:int, nbToAdd:int) -> tuple[int, int]:
        x = self.screenW/2 - (nbToAdd*(self.WIDTHSANCTUARY+self.WIDTHSANCTUARY*0.25))/2 + i*(self.WIDTHSANCTUARY+self.WIDTHSANCTUARY*0.25)
        y = self.screenH - self.HEIGHTSANCTUARY*1.5
        return (x, y)
    
    ## Animation for the type of cards given (0 for region cards, 1 for sanctuary cards)
    def animateCard(self, lgth:int, type_card:int) -> None:
        # Check if there is enough coordinates for the size lgth
        if lgth > len(self.x_anim):
            self.setupAnimationCoordinates(False, lgth)

        # Get the initial position of the cards
        pos_init = [(self.x_anim[i][type_card], self.y_anim[i][type_card]) for i in range(lgth)]

        pos_final = []

        # Get the final position of the cards
        if type_card == 0:
            pos_final = [self.calculateCoordinateRegion(i, lgth) for i in range(lgth)]
        else:
            pos_final = [self.calculateCoordinateSanctuary(i, lgth) for i in range(lgth)]

        # Get the maximum distance between the initial and final position
        dist_max = [math.sqrt((x1 - x2)**2 + (y1 - y2)**2) for (x1, y1), (x2, y2) in zip(pos_init, pos_final)]

        tmp_max = max(dist_max) / self.SPEED

        # Get the speed for each card (all this calculation is to have the cards to arrive at the same time)
        speed_x = [(x2 - x1) / tmp_max for (x1, _), (x2, _) in zip(pos_init, pos_final)]
        speed_y = [(y2 - y1) / tmp_max for (_, y1), (_, y2) in zip(pos_init, pos_final)]

        gray = (200,200,200)
        white = (255,255,255)
        rectangle = []

        # Get all the rectangles (which represents the cards)
        if type_card == 0:
            rectangle = [pygame.Rect(x, y, self.WIDTHREGION, self.HEIGHTREGION) for x, y in pos_init]
        else:
            rectangle = [pygame.Rect(x, y, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY) for x, y in pos_init]

        # Draw the rectangles
        for rect in rectangle:
            pygame.draw.rect(self.screen, gray, rect, border_radius=CardDisplay.border_radius)
            pygame.draw.rect(self.screen, white, rect, 1, border_radius=CardDisplay.border_radius)
           
        # Move the cards for next frame
        for i in range(lgth):
            self.x_anim[i][type_card] += speed_x[i]
            self.y_anim[i][type_card] += speed_y[i]

        # Check if the cards are arrived
        if self.state != State.REVEAL:
            # The cards should getting down (0, 0 is a the top left corner of the screen)
            if min(speed_y) <= 0:
                self.animation = False
                self.setupAnimationCoordinates()
        else:
            # The cards should getting up (0, 0 is a the top left corner of the screen)
            if min(speed_y) >= 0:
                self.animation = False
                self.setupAnimationCoordinates(True, len(self.actualPlayer.hand))

    ## Calculate the coordinate for the region cards
    def calculateCoordinateRegion(self, i:int, lgth:int) -> tuple[int, int]:
        nbCardOnRow = lgth # Number of cards to display on the row
        
        # If there is too much card display them in 2 rows
        if lgth > 4:
            y = 0
            if i < 4:
                y = self.screenH - self.HEIGHTREGION*2.25
                nbCardOnRow = 4
            else:
                y = self.screenH - self.HEIGHTREGION*1.2
                nbCardOnRow = lgth - 4
        else:
            y = self.screenH - self.HEIGHTREGION*1.5
        
        x = self.screenW/2 - (nbCardOnRow*(self.WIDTHREGION+self.WIDTHREGION*0.25))/2*0.95 + (i%4)*(self.WIDTHREGION+self.WIDTHREGION*0.25)
        return (x, y)


    ## Override
    def chooseRegionCard(self) -> None:
        # Display the text
        textr = "Choose the region card you want :"
        self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.4, textr)

        lgth = self.nbJoueur+1-self.cpt

        if self.animation:
            self.animateCard(lgth, 0)
            # Display the actual player and the separator
            self.displayActualPlayer()
        else: 
            # Display the actual player and the separator
            self.displayActualPlayer()
            for i in range(lgth): # Display number of players plus one region cards
                # Display the card
                card = self.regionCards[i]

                x, y = self.calculateCoordinateRegion(i, lgth)
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
                            self.animation = True # Activate the animation
                            self.setupAnimationCoordinates(True, len(self.actualPlayer.hand))
                            break # Stop the loop because the card has been chosen
                    
    ## Override
    def displayEnd(self) -> None:
        # Texts
        textScore = " Scores :"
        textSep = "___________"

        # Display texts
        dec = self.screenH*0.5 - self.screenH*0.05*len(self.players) # Offset for the display in height (depending of the number of players)
        sizePol = int(self.sizePol*1.2)
        self.displayText(sizePol, self.screenW*0.5, dec, textScore)
        self.displayText(sizePol, self.screenW*0.5, dec+self.screenH*0.04, textSep)

        # Display the scores one by one with an animation
        if self.animation == True:

            # Display the scores
            self.nbPlScores
            for i in range(self.nbPlScores+1):

                # Get the id and the res of the player
                pId, res = list(self.scores.items())[self.nbJoueur - (i+1)]


                tmp_res = 0
                if i == self.nbPlScores:
                    # Animation for the scores (increase the score by 1 each NBFRAMESMAX frame)
                    self.nbFramesPassed += 1
                    tmp_res = self.tmpScore
                    if self.nbFramesPassed == self.NBFRAMESMAX:
                        self.tmpScore += 1
                        self.nbFramesPassed = 0

                    # Do the animation for the next player in scores
                    if self.tmpScore == res:
                        self.tmpScore = 0
                        self.nbPlScores += 1
                else:
                    tmp_res = res

                # Display the score of the player
                textPts = [player for player in self.players if player.id == pId][0].pseudo + " : " + str(tmp_res) + " points"
                self.displayText(sizePol, self.screenW/2, dec + self.screenH*0.18 + (self.nbJoueur - (i+1))*self.screenH*0.08, textPts)
            
            # The animation for each player is finished
            if self.nbPlScores == self.nbJoueur:
                self.animation = False

        else:
            # Display the scores normally
            i=0 
            for pId, res in self.scores.items():
                textPts = [player for player in self.players if player.id == pId][0].pseudo + " : " + str(res) + " points"
                self.displayText(sizePol, self.screenW/2, dec + self.screenH*0.18 + i*self.screenH*0.08, textPts)
                i+=1

            # If there is a right clic go to the next player so he can see his revealed cards
            if self.clic == 2:
                self.next(State.END)


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
        rect_reg = self.displayText(sizePol, sizePol*2.5, self.HEIGHTSANCTUARY + self.HEIGHTREGION*0.8, textr) 

        # Display region cards
        i=0
        for card in self.actualPlayer.revealedCards:
            y = 0
            # Display the cards in 2 different rows
            if i > 3:
                y = self.HEIGHTSANCTUARY*1.2 + self.HEIGHTREGION
            else :
                y = self.HEIGHTSANCTUARY*1.1
            x = (i%4)*(self.WIDTHREGION*1.1) + rect_reg.width*1.05
            card.dcard.display(x, y)
            i+=1

        # Display sanctuary cards
        i=0
        l = len(self.actualPlayer.sanctuaryCards)
        for card in self.actualPlayer.sanctuaryCards:
            y = self.HEIGHTSANCTUARY*0.05
            x = self.screenW/2 - (l*(self.WIDTHSANCTUARY*1.1))/2 + i*(self.WIDTHSANCTUARY*1.1)
            card.dcard.display(x, y)
            i+=1


    ## Display the revealed cards for the actual player
    def displayCardToChooseLater(self) -> None:
        # Fill the screen to only show the revealed cards        
        background = pygame.image.load("./data/img/background.png")
        background = pygame.transform.scale(background, (self.screenW, self.screenH))
        self.screen.blit(background, (0, 0))

        # Size police
        sizePol = self.sizePol

        # Text sanctuary cards
        texts = "The region cards to choose in the next round :"
        self.displayText(sizePol, self.screenW//2, self.screenH//4, texts)

        lgth = self.nbJoueur+1
        for i in range(lgth): # Display number of players plus one region cards
            # Display the card
            card = self.regionCards[i]

            x, y = self.calculateCoordinateRegion(i, lgth)
            card.dcard.display(x, y)
        

    ## Display some informations for the players
    def infoPlayers(self) -> None:
        # Display the actual player, the turn number and the key bind
        turn = " | "
        if self.state == State.END:
            turn += "Game is finished" 
        else:
            turn += "Turn number : "+str(self.nbTurns+1)

        # Text for the keybinds
        textKeybindd = ""
        if self.state == State.REVEAL: # keybind only needed for the reveal state
            textKeybindd = " | Press 'd' to show the cards you will have to choose"
        textKeybinds = "Press 's' to show your revealed cards"
        textKeyBind_all = textKeybinds + textKeybindd

        textPl = "Actual Player : " + str(self.actualPlayer.pseudo) + turn 

        sizePol = self.sizePol//2
        # Display on two different lines
        self.displayText(sizePol, self.screenW//2, self.screenH - sizePol*1.1, textPl) 
        self.displayText(sizePol, self.screenW//2, self.screenH - sizePol*0.3, textKeyBind_all)



    ## Create a rectangle to permit the player to close the pygame window
    def forceExit(self) -> None:
        # Create and draw the rectangle
        rect = pygame.Rect(self.screenW-50, 0, 50, 50)
        pygame.draw.rect(self.screen, (255,0,0), rect)

        # Check the mouse position and clic
        pos = pygame.mouse.get_pos()
        if rect.collidepoint(pos[0], pos[1]) and self.clic == 2:
            self.running = False


    ## Call the function corresponding to the actual state
    def execute(self) -> None:
        if self.nbTurns == 8:
            self.state = State.END
        if self.state == State.START:
            self.chooseNbPlayers()
        elif self.state == State.PSEUDO:
            self.enterPseudo()
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
        # Sort the results by points
        self.scores = {key: self.scores[key] for key in sorted(self.scores, key=self.scores.get, reverse=True)}
        self.animation = True
        self.state = State.END


    ## Display the text at the given coordonate and return the rectangle where the text is 
    def displayText(self, sizePol:int, x:int, y:int, text:str, colTxt:tuple[int, int, int]=(255,255,255), pol:str=None) -> pygame.Rect:
        police = pygame.font.Font(pol, sizePol)
        texte_surface = police.render(text, True, colTxt)
        self.screen.blit(texte_surface, (x-texte_surface.get_width()/2, y-texte_surface.get_height()/2))  
        return texte_surface.get_rect()
        
    
    ## Display actual player with a separator
    def displayActualPlayer(self):
        # Display the separator
        textSep = "__________________________"
        self.displayText(self.sizePol-10, self.screenW/2, self.screenH - self.HEIGHTREGION*2.6, textSep)

        # Display the actual player
        textPl = "Actual player : " + str(self.actualPlayer.pseudo)
        self.displayText(self.sizePol, self.screenW/2, self.screenH - self.HEIGHTREGION*2.64, textPl)


    ## Display the stack of the regions cards and the sanctuary cards
    def displayStacks(self) -> None:
        coef_dec_card = 0.001
        x_stack_reg = self.screenW*0.26
        x_stack_sanc = self.screenW*0.55
        mid = 0.5
        gray = (200,200,200)
        white = (255,255,255)

        # Display the stack of the region cards
        for i in range(len(self.regionCards)):
            r_reg = pygame.Rect(x_stack_reg + i*self.WIDTHREGION*coef_dec_card, -self.HEIGHTREGION*mid - i*self.HEIGHTREGION*coef_dec_card, self.WIDTHREGION, self.HEIGHTREGION)
            # Draw two rectangles, one inside the other to have a border
            pygame.draw.rect(self.screen, gray, r_reg, border_radius=CardDisplay.border_radius)
            pygame.draw.rect(self.screen, white, r_reg, 1, border_radius=CardDisplay.border_radius)

        # Display the stack of the sanctuary cards
        for i in range(len(self.sanctuaryCards)):
            r_sanc = pygame.Rect(x_stack_sanc + i*self.WIDTHREGION*coef_dec_card, -self.HEIGHTSANCTUARY*mid - i*self.HEIGHTREGION*coef_dec_card, self.WIDTHSANCTUARY, self.HEIGHTSANCTUARY)
            # Draw two rectangles, one inside the other to have a border
            pygame.draw.rect(self.screen, gray, r_sanc, border_radius=CardDisplay.border_radius)
            pygame.draw.rect(self.screen, white, r_sanc, 1, border_radius=CardDisplay.border_radius)

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

            # fill the screen with the background to wipe away anything from last frame
            background = pygame.image.load("./data/img/background.png")
            background = pygame.transform.scale(background, (self.screenW, self.screenH))
            self.screen.blit(background, (0, 0))
            
            # Check is exit is pressed
            self.forceExit()

            if self.state != State.START and self.state != State.END and self.state != State.PSEUDO:
                # Display the stacks
                self.displayStacks()

            # Check if the key bind is pressed and it is not the start
            if pygame.key.get_pressed()[pygame.K_s] and self.state != State.START and self.state != State.PSEUDO:
                self.displayRevealedCard()
            elif pygame.key.get_pressed()[pygame.K_d] and self.state == State.REVEAL:
                self.displayCardToChooseLater()
            else:
                # Execute the right function corresponding to the state
                self.execute()

            # Display some informations if it is not the start
            if self.state != State.START and self.state != State.PSEUDO:
                self.infoPlayers()
            
            # Check is the left clic is up (This permits to only detect a clic when it is up after being down)
            if self.clic == 2:
                self.clic = 0

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60) / 1000

        pygame.quit()
        
        return