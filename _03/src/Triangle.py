import math
from .Figure import Figure


class Triangle(Figure):
    def __init__(self, side_a=0, side_b=0, side_c=0):
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError('Triangle sides must be positive')
        if side_a + side_b <= side_c or side_a + side_c <= side_b or side_b + side_c <= side_a:
            raise ValueError('Triangle inequality violated')

        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
        self.name = 'Triangle'

    def perimeter(self):
        return self.side_a + self.side_b + self.side_c

    def area(self):
        semiperimeter = self.perimeter() / 2

        return math.sqrt(semiperimeter * (semiperimeter - self.side_a) * (semiperimeter - self.side_b) * (
                    semiperimeter - self.side_c))
