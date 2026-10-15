from alien import Alien

class FastAlien(Alien):
    """Alienígena mais rápido."""

    def update(self) -> None:
        self.x += (self.settings.alien_speed * 2) *self.settings.fleet_direction #provavelmente dará um erro no jogo mostrando duas naves uma em cima da outra com velocidades diferentes, eu não sei por que isso acontece, mas para consertar e uma se sobreescrever (ainda vai ter as duas naves mas uma sobre a outra na mesma velocidade), basta apagar o "* 2" ao lado de "self.settings.alien_speed"
        self.rect.x = self.x