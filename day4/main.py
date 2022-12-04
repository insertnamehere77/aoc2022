import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip(), f.readlines()))


class Assignment:
    begin: int
    end: int

    def __init__(self, range: str) -> None:
        sections = range.split("-")
        self.begin = int(sections[0])
        self.end = int(sections[1])

    def contains_fully(self, other: "Assignment") -> bool:
        return self.begin <= other.begin and self.end >= other.end

    def overlaps(self, other: "Assignment") -> bool:
        return self.begin <= other.end and self.end >= other.begin


def parse_input(lines: list[str]) -> list[tuple[Assignment]]:
    assignments = []
    for line in lines:
        ranges = line.split(",")
        assignments.append((Assignment(ranges[0]), Assignment(ranges[1])))

    return assignments


def part1(pairs: list[tuple[Assignment]]) -> int:
    num_contained = 0
    for pair in pairs:
        (first, last) = pair
        if first.contains_fully(last) or last.contains_fully(first):
            num_contained += 1

    return num_contained


def part2(pairs: list[tuple[Assignment]]) -> int:
    num_overlap = 0
    for pair in pairs:
        (first, last) = pair
        if first.overlaps(last):
            num_overlap += 1

    return num_overlap


def main(file_name: str):
    lines = read_file(file_name)
    pairs = parse_input(lines)
    print("Part1:", part1(pairs))
    print("Part2:", part2(pairs))


if __name__ == "__main__":
    main(sys.argv[1])
