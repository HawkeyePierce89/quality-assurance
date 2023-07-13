import pytest
from _03.src.Triangle import Triangle
from _03.src.Square import Square


@pytest.mark.parametrize('side_a, side_b, side_c, perimeter, area', [
    (5, 5, 8, 18, 12),
    (5, 12, 13, 30, 30),
])
def test_triangle_positive(side_a, side_b, side_c, perimeter, area):
    r = Triangle(side_a, side_b, side_c)
    assert r.name == 'Triangle'
    assert r.area() == area
    assert r.perimeter() == perimeter


@pytest.mark.parametrize('side_a, side_b, side_c', [
    (40, 10, 78),
    (1, 2, 3)
])
def test_triangle_negative(side_a, side_b, side_c):
    with pytest.raises(ValueError):
        Triangle(side_a, side_b, side_c)


@pytest.mark.parametrize('side_a, side_b, side_c, figure, area', [
    (5, 5, 8, Square(10), 112),
    (5, 12, 13, Square(1), 31),
])
def test_triangle_with_figure_positive(side_a, side_b, side_c, figure, area):
    r = Triangle(side_a, side_b, side_c)
    assert r.add_area(figure) == area


@pytest.mark.parametrize('side_a, side_b, side_c, figure', [
    (5, 12, 13, False),
])
def test_triangle_with_figure_negative(side_a, side_b, side_c, figure):
    r = Triangle(side_a, side_b, side_c)
    with pytest.raises(ValueError):
        r.add_area(figure)
