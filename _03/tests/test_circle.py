import pytest
import math
from _03.src.Circle import Circle
from _03.src.Square import Square


@pytest.mark.parametrize('radius, perimeter, area', [
    (10, 20 * math.pi, 100 * math.pi),
    (1, 2 * math.pi, 1 * math.pi),
])
def test_circle_positive(radius, perimeter, area):
    r = Circle(radius)
    assert r.name == 'Circle'
    assert r.area() == area
    assert r.perimeter() == perimeter

@pytest.mark.parametrize('radius', [
    0,
    (-1),
])
def test_circle_negative(radius):
    with pytest.raises(ValueError):
        Circle(radius)

@pytest.mark.parametrize('radius, figure, area', [
    (10, Square(10), 100 * math.pi + 100),
    (1, Square(1), 1 * math.pi + 1),
])
def test_circle_with_figure_positive(radius, figure, area):
    r = Circle(radius)
    assert r.add_area(figure) == area


@pytest.mark.parametrize('radius, figure', [
    (4, False),
])
def test_circle_with_figure_negative(radius, figure):
    r = Circle(radius)
    with pytest.raises(ValueError):
        r.add_area(figure)
