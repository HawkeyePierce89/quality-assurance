from .figure import Figure


class Rectangle(Figure):
    def __init__(self, side_a=0, side_b=0):
        if side_a <= 0 or side_b <= 0:
            raise ValueError('Rectangle sides must be positive.')
        self.side_a = side_a
        self.side_b = side_b
        self.name = 'Rectangle'

    def area(self):
        return self.side_a * self.side_b

    def perimeter(self):
        return 2 * (self.side_a + self.side_b)
