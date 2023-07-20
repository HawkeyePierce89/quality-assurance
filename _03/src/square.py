from .rectangle import Rectangle


class Square(Rectangle):
    def __init__(self, side_a=0):
        if side_a <= 0:
            raise ValueError('Square sides must be positive.')
        super().__init__(side_a, side_a)
        self.name = 'Square'
