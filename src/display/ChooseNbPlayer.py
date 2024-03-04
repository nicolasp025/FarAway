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
        self.maxJ = max
        self.minJ = min


    ## Display the screen to choose the number of players and 
    ## check if the user has clicked on the validate button
    def display(self, nbJoueur:int, clic:tuple[int, int]) -> tuple[bool, int]:
        midW = self.screen.get_width()/2   # screen's middle width
        midH = self.screen.get_height()/2  # screen's middle height
        ecart = 200                        # the offset between the middle and the triangles
        col = (255,255,255)

        # Triangle 1
        points_triangle1 = [(midW+ecart, midH), (midW+ecart, midH+180), (midW+180+ecart, midH+90)]
        tr1 = Triangle(points_triangle1)
        tr1.draw(self.screen, col)

        # Triangle 2
        points_triangle2 = [(midW-ecart, midH), (midW-ecart, midH+180), (midW-180-ecart, midH+90)]
        tr2 = Triangle(points_triangle2)
        tr2.draw(self.screen, col)
        
        # Size of polices
        sizePolNbPl = 400
        sizePolTxt = 100

        # Polices
        polNbPl = pygame.font.Font(None, sizePolNbPl)
        polTxt = pygame.font.Font(None, sizePolTxt)

        # Rectangle to create a button for the validation
        rect = pygame.Rect(midW-140, midH+300, 290, 70)
        
        # Texts
        textT = "Choose the number of players :"
        textVal = "Validate"

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
        self.screen.blit(texte_surface, (midW-75, midH-35))

        # Display the text
        textet_surface = polTxt.render(textT, True, col)  
        self.screen.blit(textet_surface, (midW-495, midH-195))

        # Display the button and the text within
        pygame.draw.rect(self.screen, col, rect, 2)
        textev_surface = polTxt.render(textVal, True, col)  
        self.screen.blit(textev_surface, (rect.x + 5, rect.y + 5))

        return False, nbJ