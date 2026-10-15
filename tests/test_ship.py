import pygame
import pytest

from src.ship import Ship
from tests.doubles import StubSettings


@pytest.fixture
def mock_screen(mocker):
    screen = mocker.Mock()
    screen.get_rect.return_value = pygame.Rect(0, 0, 1200, 800)
    return screen


@pytest.fixture
def ship(mock_screen):
    return Ship(mock_screen, StubSettings())


def test_ship_move_direita_com_stub(ship):
    x_inicial = ship.x

    ship.moving_right = True
    ship.update()

    assert ship.x == x_inicial + StubSettings.ship_speed


def test_blitme_desenha_nave_na_tela(ship, mock_screen):
    ship.blitme()

    mock_screen.blit.assert_called_once_with(ship.image, ship.rect)