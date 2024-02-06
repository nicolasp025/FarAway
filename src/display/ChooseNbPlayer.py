import sys
import pygame

sys.path.append("./src/player/")
sys.path.append("./src/enum/")

from Player import Player
from Triangle import Triangle
from State import State


class ChooseNbPlayer:
        
    def __init__(self, screen, max, min):
        self.screen = screen
        self.maxJ = max
        self.minJ = min


    def display(self, nbJoueur, clic):

        midW = self.screen.get_width()/2
        midH = self.screen.get_height()/2
        ecart = 200
        col = (255,255,255)
        points_triangle1 = [(midW+ecart, midH), (midW+ecart, midH+180), (midW+180+ecart, midH+90)]
        tr1 = Triangle(points_triangle1)
        tr1.dessiner(self.screen, col)
        points_triangle2 = [(midW-ecart, midH), (midW-ecart, midH+180), (midW-180-ecart, midH+90)]
        tr2 = Triangle(points_triangle2)
        tr2.dessiner(self.screen, col)
        
        sizeP = 400
        police = pygame.font.Font(None, sizeP)
        text_nbJ = pygame.Rect(midW-80, midH-40, 100, 50)
        
        policet = pygame.font.Font(None, 100)
        text_title = pygame.Rect(midW-500, midH-200, 400, 50)
        textt = "Choose the number of players :"

        text_val = pygame.Rect(midW-140, midH+300, 290, 70)
        textv = "Validate"

        nbJ = nbJoueur
        if clic==2:
            pos = pygame.mouse.get_pos()
            if tr1.clickIn(pos):
                nbJ = min(self.maxJ, nbJ+1)
            elif tr2.clickIn(pos):
                nbJ = max(self.minJ, nbJ-1)
            elif text_val.collidepoint(pos[0], pos[1]):
                return True, nbJ

        text = str(nbJ)
        pygame.draw.rect(self.screen, (0,0,0), text_nbJ)
        texte_surface = police.render(text, True, col)  
        self.screen.blit(texte_surface, (text_nbJ.x + 5, text_nbJ.y + 5))

        pygame.draw.rect(self.screen, (0,0,0), text_title)
        textet_surface = policet.render(textt, True, col)  
        self.screen.blit(textet_surface, (text_title.x + 5, text_title.y + 5))

        pygame.draw.rect(self.screen, col, text_val, 2)
        textev_surface = policet.render(textv, True, col)  
        self.screen.blit(textev_surface, (text_val.x + 5, text_val.y + 5))

        return False, nbJ