from src.desconto import IDesconto


class StubSemDesconto(IDesconto):
    def calcular(self, valor):
        return 0

class StubSettings:
    ship_speed = 1.5