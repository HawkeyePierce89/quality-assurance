from abc import ABC, abstractmethod


class Figure(ABC):

    @abstractmethod
    def area(self):
        return 0

    @abstractmethod
    def perimeter(self):
        return 0

    def add_area(self, figure):
        if not isinstance(figure, Figure):
            raise ValueError('Figure must be an instance of Figure.')
        return self.area() + figure.area()
