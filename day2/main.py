import sys
import part1, part2


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip(), f.readlines()))


def main(file_name: str):
    lines = read_file(file_name)
    print("Part1:", part1.run(lines))
    print("Part2:", part2.run(lines))


if __name__ == "__main__":
    main(sys.argv[1])
