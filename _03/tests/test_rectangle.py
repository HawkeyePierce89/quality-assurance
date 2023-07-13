import pytest
from _03.src.Rectangle import Rectangle
from _03.src.Square import Square


@pytest.mark.parametrize('side_a, side_b, perimeter, area', [
    (4, 5, 18, 20),
    (10, 20, 60, 200)
])
def test_rectangle_positive(side_a, side_b, perimeter, area):
    r = Rectangle(side_a, side_b)
    assert r.name == 'Rectangle'
    assert r.area() == area
    assert r.perimeter() == perimeter


@pytest.mark.parametrize('side_a, side_b', [
    (-1, 10),
    (2, 0)
])
def test_rectangle_negative(side_a, side_b):
    with pytest.raises(ValueError):
        Rectangle(side_a, side_b)


@pytest.mark.parametrize('side_a, side_b, figure, area', [
    (4, 5, Square(10), 120),
    (10, 20, Square(1), 201)
])
def test_rectangle_with_figure_positive(side_a, side_b, figure, area):
    r = Rectangle(side_a, side_b)
    assert r.add_area(figure) == area


@pytest.mark.parametrize('side_a, side_b, figure', [
    (4, 5, False),
])
def test_rectangle_with_figure_negative(side_a, side_b, figure):
    r = Rectangle(side_a, side_b)
    with pytest.raises(ValueError):
        r.add_area(figure)
