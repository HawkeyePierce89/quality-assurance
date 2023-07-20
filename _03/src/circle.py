import math
from .figure import Figure


class Circle(Figure):
    def __init__(self, radius=0):
        if radius <= 0:
            raise ValueError('Circle radius must be positive.')
        self.radius = radius
        self.name = 'Circle'

    def area(self):
        return math.pi * self.radius ** 2

    def perimeter(self):
        return 2 * math.pi * self.radius
