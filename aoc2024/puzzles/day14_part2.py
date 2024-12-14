import curses
import time
import aoc2024.common.input as aoc_input
from .day14 import Robot, debug_robot_counts, real_shape

TIME_BETWEEN_TICKS = 0.06


def main(stdscr: curses.window):
    stdscr.clear()
    curses.curs_set(False)
    stdscr.nodelay(True)

    puzzle_input = aoc_input.load_lines("day14input")
    robots = Robot.parse_all(puzzle_input)
    shape = real_shape()
    grid = debug_robot_counts(robots, shape)

    running = True
    last_valid_key = None

    tick = 0
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
                    r.move(shape)
                grid = debug_robot_counts(robots, shape)
                tick += 1
            elif key == "KEY_LEFT":
                tick -= 1
                robots = Robot.parse_all(puzzle_input)
                for r in robots:
                    r.move(shape, tick)
                grid = debug_robot_counts(robots, shape)

        if running and now > prev_tick_time + TIME_BETWEEN_TICKS:
            for r in robots:
                r.move(shape)
            grid = debug_robot_counts(robots, shape)
            prev_tick_time = now
            tick += 1

        if running:
            status_line = "Running - press SPACE to pause"
        else:
            status_line = "Paused - press SPACE to unpause, or LEFT/RIGHT to step"

        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, f"[{last_valid_key}]" if last_valid_key else "None")
        stdscr.move(1, 0)
        stdscr.clrtoeol()
        stdscr.addstr(1, 0, f"Tick {tick} - {status_line}")
        stdscr.addstr(2, 0, grid)
        stdscr.refresh()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
