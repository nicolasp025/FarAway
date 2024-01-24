import pygame
import sys

class Triangle:
    def __init__(self, points):
        self.points = points

    def dessiner(self, fenetre, couleur):
        pygame.draw.polygon(fenetre, couleur, self.points)

    def clickIn(self, coord_clic):
        x, y = coord_clic
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]

        detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / detT
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / detT
        gamma = 1 - alpha - beta

        return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1

