import pytest
from _03.src.Square import Square
from _03.src.Rectangle import Rectangle


@pytest.mark.parametrize('side_a, perimeter, area', [
    (4, 16, 16),
    (10, 40, 100)
])
def test_square_positive(side_a, perimeter, area):
    r = Square(side_a)
    assert r.name == 'Square'
    assert r.area() == area
    assert r.perimeter() == perimeter


@pytest.mark.parametrize('side_a', [
    0,
    (-1)
])
def test_square_negative(side_a):
    with pytest.raises(ValueError):
        Square(side_a)

@pytest.mark.parametrize('side_a, figure, area', [
    (4, Rectangle(10, 25), 266),
    (10, Rectangle(1, 35), 135)
])
def test_square_with_figure_positive(side_a, figure, area):
    r = Square(side_a)
    assert r.add_area(figure) == area


@pytest.mark.parametrize('side_a, figure', [
    (4, False),
])
def test_square_with_figure_negative(side_a, figure):
    r = Square(side_a)
    with pytest.raises(ValueError):
        r.add_area(figure)