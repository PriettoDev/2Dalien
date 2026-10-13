import pygame
from src.ship import Ship
from src.settings import Settings

def test_ship():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    settings = Settings()

    ship = Ship(screen, settings)

    x_inicial = ship.x

    #ação da nave
    ship.moving_right = True
    ship.update()

    #verificação
    assert ship.x > x_inicial