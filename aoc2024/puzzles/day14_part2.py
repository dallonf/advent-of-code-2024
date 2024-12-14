import curses
import time
import argparse
import aoc2024.common.input as aoc_input
from .day14 import Robot, debug_robot_counts, real_shape


def main(stdscr: curses.window, args: argparse.Namespace):
    stdscr.clear()
    curses.curs_set(False)
    stdscr.nodelay(True)

    starting_tick: int = args.startingtick
    step: int = args.step
    speed: float = args.speed
    time_between_ticks = 1 / speed

    puzzle_input = aoc_input.load_lines("day14input")
    robots = Robot.parse_all(puzzle_input)
    shape = real_shape()
    for r in robots:
        r.move(shape, starting_tick)
    grid = debug_robot_counts(robots, shape)

    running = False

    tick = starting_tick
    prev_tick_time = time.time()
    while True:
        now = time.time()

        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == " ":
            running = not running

        if not running:
            if key == "KEY_RIGHT":
                for r in robots:
                    r.move(shape, step)
                grid = debug_robot_counts(robots, shape)
                tick += step
            elif key == "KEY_LEFT":
                tick -= step
                robots = Robot.parse_all(puzzle_input)
                for r in robots:
                    r.move(shape, tick)
                grid = debug_robot_counts(robots, shape)

        if running and now > prev_tick_time + time_between_ticks:
            for r in robots:
                r.move(shape, step)
            grid = debug_robot_counts(robots, shape)
            prev_tick_time = now
            tick += step

        if running:
            status_line = "Running - press SPACE to pause"
        else:
            status_line = "Paused - press SPACE to unpause, or LEFT/RIGHT to step"

        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, f"Tick {tick} - {status_line}")
        stdscr.addstr(1, 0, grid)
        stdscr.refresh()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Day 14 Part Two")
    parser.add_argument("--startingtick", "--start", default=1, type=int)
    parser.add_argument(
        "--step",
        default=1,
        type=int,
        help="Moves robots by this many simulated 'seconds' every iteration",
    )
    parser.add_argument(
        "-s", "--speed", default="30", type=float, help="ticks per real second"
    )
    args = parser.parse_args()

    try:
        curses.wrapper(main, args)
    except KeyboardInterrupt:
        pass
