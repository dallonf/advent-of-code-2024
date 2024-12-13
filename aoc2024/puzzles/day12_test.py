from textwrap import dedent
from aoc2024.common.grid import IntVector2
import aoc2024.common.input as aoc_input
from .day12 import (
    EdgesSolver,
    Region,
    get_regions,
    parse,
    RegionSolver,
    part_one_answer,
    part_two_answer,
)

SIMPLE_INPUT = aoc_input.lines(
    dedent(
        """
        AAAA
        BBCD
        BBCC
        EEEC
        """
    )
)

NESTED_INPUT = aoc_input.lines(
    dedent(
        """
        OOOOO
        OXOXO
        OOOOO
        OXOXO
        OOOOO
        """
    )
)

LARGE_INPUT = aoc_input.lines(
    dedent(
        """
        RRRRIICCFF
        RRRRIICCCF
        VVRRRCCFFF
        VVRCCCJFFF
        VVVVCJJCFE
        VVIVCCJJEE
        VVIIICJJEE
        MIIIIIJJEE
        MIIISIJEEE
        MMMISSJEEE
        """
    )
)


def test_simple_plot():
    solver = RegionSolver(parse(SIMPLE_INPUT))
    regions = solver.get_regions()
    assert len(regions) == 5
    assert (
        Region(
            "A",
            frozenset(
                [IntVector2(0, 0), IntVector2(1, 0), IntVector2(2, 0), IntVector2(3, 0)]
            ),
        )
        in regions
    )
    assert (
        Region(
            "B",
            frozenset(
                [IntVector2(0, 1), IntVector2(1, 1), IntVector2(0, 2), IntVector2(1, 2)]
            ),
        )
        in regions
    )
    assert (
        Region(
            "C",
            frozenset(
                [IntVector2(2, 1), IntVector2(2, 2), IntVector2(3, 2), IntVector2(3, 3)]
            ),
        )
        in regions
    )

    regions_with_perimeters = {region.plant: region.perimeter for region in regions}
    assert regions_with_perimeters == {"A": 10, "B": 8, "C": 10, "D": 4, "E": 8}


def test_internal_regions():
    regions = get_regions(parse(NESTED_INPUT))
    assert len(regions) == 5


def test_pricing():
    regions = get_regions(parse(SIMPLE_INPUT))
    regions_with_prices = {region.plant: region.price_to_fence for region in regions}
    assert regions_with_prices == {"A": 40, "B": 32, "C": 40, "D": 4, "E": 24}


def test_part_one_answer():
    assert part_one_answer(SIMPLE_INPUT) == 140
    assert part_one_answer(NESTED_INPUT) == 772
    assert part_one_answer(LARGE_INPUT) == 1930


def test_sides():
    regions = get_regions(parse(SIMPLE_INPUT))
    regions_with_sides = {region.plant: region.sides for region in regions}
    assert regions_with_sides == {"A": 4, "B": 4, "C": 8, "D": 4, "E": 4}


def test_sides_detail():
    region = Region(
        "A",
        frozenset(
            [IntVector2(0, 0), IntVector2(1, 0), IntVector2(2, 0), IntVector2(3, 0)]
        ),
    )
    solver = EdgesSolver(region)
    edges = solver.get_edges()
    print(edges)
    assert len(edges) == 4


def test_part_two_answer():
    assert part_two_answer(SIMPLE_INPUT) == 80
    input_with_e = aoc_input.lines(
        dedent(
            """
            EEEEE
            EXXXX
            EEEEE
            EXXXX
            EEEEE
            """
        )
    )
    assert part_two_answer(input_with_e) == 236
    input_with_diagonal = aoc_input.lines(
        dedent(
            """
            AAAAAA
            AAABBA
            AAABBA
            ABBAAA
            ABBAAA
            AAAAAA
            """
        )
    )
    assert part_two_answer(input_with_diagonal) == 368
    assert part_two_answer(LARGE_INPUT) == 1206
