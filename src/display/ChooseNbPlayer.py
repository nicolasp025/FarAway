import sys
import pygame

sys.path.append("./src/player/")
sys.path.append("./src/enum/")

from Player import Player
from Triangle import Triangle
from State import State

## The class which represent the display to choose the number of players
class ChooseNbPlayer:
        
    def __init__(self, screen, max:int, min:int):
        self.screen = screen
        self.screenW = screen.get_width()
        self.screenH = screen.get_height()
        self.maxJ = max
        self.minJ = min


    ## Display the screen to choose the number of players and 
    ## check if the user has clicked on the validate button
    def display(self, nbJoueur:int, clic:tuple[int, int]) -> tuple[bool, int]:
        midW = self.screen.get_width()/2   # screen's middle width
        midH = self.screen.get_height()/2  # screen's middle height
        ecart = self.screenW*0.1           # the offset between the middle and the triangles
        col = (255,255,255)

        # Triangle 1
        dec1 = self.screenH*0.16
        dec2 = self.screenH*0.08
        points_triangle1 = [(midW+ecart, midH), (midW+ecart, midH+dec1), (midW+dec1+ecart, midH+dec2)]
        tr1 = Triangle(points_triangle1)
        tr1.draw(self.screen, col)

        # Triangle 2
        points_triangle2 = [(midW-ecart, midH), (midW-ecart, midH+dec1), (midW-dec1-ecart, midH+dec2)]
        tr2 = Triangle(points_triangle2)
        tr2.draw(self.screen, col)
        
        # Size of polices
        sizePolNbPl = self.screenW//5
        sizePolTxt = self.screenW//21

        # Polices
        polNbPl = pygame.font.Font(None, sizePolNbPl)
        polTxt = pygame.font.Font(None, sizePolTxt)
        
        # Texts
        textT = "Choose the number of players :"
        textVal = "Validate"

        # Display the text
        textet_surface = polTxt.render(textT, True, col)  
        coor = (midW-textet_surface.get_width()/2, midH-self.screenH*0.12-textet_surface.get_height()/2)
        self.screen.blit(textet_surface, coor)

        # Display the button and the text within
        textev_surface = polTxt.render(textVal, True, col)  
        coor = (midW-textev_surface.get_width()/2, midH-textev_surface.get_height()/2 + self.screenH*0.25)
        self.screen.blit(textev_surface, coor)

        # Rectangle to create a button for the validation
        rect = textev_surface.get_rect()
        rect.topleft = coor
        pygame.draw.rect(self.screen, col, rect, 2)

        # Change the number of players depending of the clic
        nbJ = nbJoueur
        if clic==2:
            pos = pygame.mouse.get_pos()
            if tr1.clickIn(pos):
                nbJ = min(self.maxJ, nbJ+1)
            elif tr2.clickIn(pos):
                nbJ = max(self.minJ, nbJ-1)
            elif rect.collidepoint(pos[0], pos[1]):
                return True, nbJ

        text = str(nbJ)

        # Display the number of player
        texte_surface = polNbPl.render(text, True, col)  
        coor = (midW-texte_surface.get_width()/2, midH-texte_surface.get_height()/2+self.screenH*0.08)
        self.screen.blit(texte_surface, coor)

        return False, nbJ