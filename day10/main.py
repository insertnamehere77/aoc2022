import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


class CPU:
    x: int = 1
    cycle: int = 0

    def noop(self):
        self.cycle += 1

    def add_x(self, val: int):
        self.x += val

    def signal_strength(self) -> int:
        return self.x * self.cycle

    def __str__(self) -> str:
        return (
            f"CPU (x: {self.x}, cycle: {self.cycle}, signal: {self.signal_strength()})"
        )


def part1(lines: list[str]) -> int:
    cpu = CPU()
    check_cycles = {20, 60, 100, 140, 180, 220}
    signals = []
    for line in lines:
        is_noop = line == "noop"
        for _ in range(0, 1 if is_noop else 2):
            cpu.noop()
            if cpu.cycle in check_cycles:
                signals.append(cpu.signal_strength())

        if not is_noop:
            val = int(line.split(" ")[1])
            cpu.add_x(val)

    return sum(signals)


class Screen:
    width: int = 40
    height: int = 6
    vals: list[list[str]]

    def __init__(self) -> None:
        self.vals = [["." for _ in range(0, self.width)] for _ in range(0, self.height)]

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self.vals])

    def draw(self, cpu: CPU):
        screen_x = cpu.cycle % self.width
        if cpu.x in [screen_x - 1, screen_x, screen_x + 1]:
            y = int(cpu.cycle / self.width)
            self.vals[y][screen_x] = "#"


def part2(lines: list[str]) -> str:
    screen = Screen()
    cpu = CPU()
    for line in lines:
        is_noop = line == "noop"
        for _ in range(0, 1 if is_noop else 2):
            screen.draw(cpu)
            cpu.noop()

        if not is_noop:
            val = int(line.split(" ")[1])
            cpu.add_x(val)

    return "\n" + screen.__str__()


def main(file_name: str):
    lines = read_file(file_name)
    print("Part1:", part1(lines))
    print("Part2:", part2(lines))


if __name__ == "__main__":
    main(sys.argv[1])
