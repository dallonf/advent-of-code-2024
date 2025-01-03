from textwrap import dedent


from aoc2024.common.grid import Direction
import aoc2024.common.input as aoc_input
from .day15 import PuzzleInput, Warehouse, part_one_answer

TINY_EXAMPLE_JUST_GRID = aoc_input.lines(
    dedent(
        """
        ########
        #..O.O.#
        ##@.O..#
        #...O..#
        #.#.O..#
        #...O..#
        #......#
        ########

        """
    )
)
SAMPLE_INPUT = aoc_input.load_lines("day15sample")


def test_parse():
    warehouse = Warehouse.parse(TINY_EXAMPLE_JUST_GRID)
    assert warehouse.format() == "\n".join(TINY_EXAMPLE_JUST_GRID)


def test_move():
    warehouse = Warehouse.parse(TINY_EXAMPLE_JUST_GRID)

    warehouse.move(Direction.LEFT)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #..O.O.#
            ##@.O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.UP)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #.@O.O.#
            ##..O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.UP)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #.@O.O.#
            ##..O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.RIGHT)
    print(warehouse.format())
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #..@OO.#
            ##..O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.RIGHT)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #...@OO#
            ##..O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.RIGHT)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #...@OO#
            ##..O..#
            #...O..#
            #.#.O..#
            #...O..#
            #......#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.DOWN)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #....OO#
            ##..@..#
            #...O..#
            #.#.O..#
            #...O..#
            #...O..#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.DOWN)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #....OO#
            ##..@..#
            #...O..#
            #.#.O..#
            #...O..#
            #...O..#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.LEFT)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #....OO#
            ##.@...#
            #...O..#
            #.#.O..#
            #...O..#
            #...O..#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.DOWN)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #....OO#
            ##.....#
            #..@O..#
            #.#.O..#
            #...O..#
            #...O..#
            ########
            """
        ).strip()
    )

    warehouse.move(Direction.RIGHT)
    assert (
        warehouse.format()
        == dedent(
            """
            ########
            #....OO#
            ##.....#
            #...@O.#
            #.#.O..#
            #...O..#
            #...O..#
            ########
            """
        ).strip()
    )


def test_sample_moves():
    puzzle_input = PuzzleInput.parse(SAMPLE_INPUT)
    puzzle_input.execute()
    assert (
        puzzle_input.warehouse.format()
        == dedent(
            """
            ##########
            #.O.O.OOO#
            #........#
            #OO......#
            #OO@.....#
            #O#.....O#
            #O.....OO#
            #O.....OO#
            #OO....OO#
            ##########
            """
        ).strip()
    )


def test_part_one_answer():
    assert part_one_answer(SAMPLE_INPUT) == 10092


SECOND_SMALL_EXAMPLE = aoc_input.lines(
    dedent(
        """
        #######
        #...#.#
        #.....#
        #..OO@#
        #..O..#
        #.....#
        #######

        <vv<<^^<<^^
        """
    )
)


def test_parse_wide():
    warehouse = PuzzleInput.parse_wide(SECOND_SMALL_EXAMPLE).warehouse
    assert (
        warehouse.format()
        == dedent(
            """
            ##############
            ##......##..##
            ##..........##
            ##....[][]@.##
            ##....[]....##
            ##..........##
            ##############
            """
        ).strip()
    )


def test_push_boxes_wide():
    warehouse = PuzzleInput.parse_wide(SECOND_SMALL_EXAMPLE).warehouse

    warehouse.move(Direction.LEFT)
    assert (
        warehouse.format()
        == dedent(
            """
            ##############
            ##......##..##
            ##..........##
            ##...[][]@..##
            ##....[]....##
            ##..........##
            ##############
            """
        ).strip()
    )

    warehouse.move(Direction.DOWN)
    warehouse.move(Direction.DOWN)
    warehouse.move(Direction.LEFT)
    warehouse.move(Direction.LEFT)
    warehouse.move(Direction.UP)
    assert (
        warehouse.format()
        == dedent(
            """
            ##############
            ##......##..##
            ##...[][]...##
            ##....[]....##
            ##.....@....##
            ##..........##
            ##############
            """
        ).strip()
    )

    warehouse.move(Direction.LEFT)
    warehouse.move(Direction.LEFT)
    warehouse.move(Direction.UP)
    warehouse.move(Direction.UP)
    assert (
        warehouse.format()
        == dedent(
            """
            ##############
            ##...[].##..##
            ##...@.[]...##
            ##....[]....##
            ##..........##
            ##..........##
            ##############
            """
        ).strip()
    )


def test_edge_cases():
    warehouse = Warehouse.parse(
        aoc_input.lines(
            dedent(
                """
                ##############
                ##......##..##
                ##...[][]...##
                ##....[]....##
                ##.....@....##
                ##..........##
                ##############
                """
            ).strip()
        )
    )
    warehouse.move(Direction.UP)
    assert (
        warehouse.format()
        == dedent(
            """
            ##############
            ##......##..##
            ##...[][]...##
            ##....[]....##
            ##.....@....##
            ##..........##
            ##############
            """
        ).strip()
    )


def test_wide_moves():
    puzzle_input = PuzzleInput.parse_wide(SAMPLE_INPUT)
    puzzle_input.execute()
    assert (
        puzzle_input.warehouse.format()
        == dedent(
            """
            ####################
            ##[].......[].[][]##
            ##[]...........[].##
            ##[]........[][][]##
            ##[]......[]....[]##
            ##..##......[]....##
            ##..[]............##
            ##..@......[].[][]##
            ##......[][]..[]..##
            ####################
            """
        ).strip()
    )
    assert puzzle_input.warehouse.sum_box_gps() == 9021
