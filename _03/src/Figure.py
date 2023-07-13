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
            raise ValueError('figure must be a Figure instance')
        return self.area() + figure.area()
