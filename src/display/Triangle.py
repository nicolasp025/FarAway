import pygame

## Triangle class
class Triangle:
    def __init__(self, points:int):
        self.points = points

    ## Draw the triangle on the screen
    def draw(self, screen, color:tuple[int, int, int]) -> None:
        pygame.draw.polygon(screen, color, self.points)

    ## Get the state of the clic, true if it is within the triangle else false
    def clickIn(self, coord_clic) -> bool:
        x, y = coord_clic
        x1, y1 = self.points[0]
        x2, y2 = self.points[1]
        x3, y3 = self.points[2]

        detT = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
        alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / detT
        beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / detT
        gamma = 1 - alpha - beta

        return 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1

