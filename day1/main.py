import sys


def read_file(file_name: str):
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip(), f.readlines()))


def parse_input(lines: list[str]) -> list[int]:
    totals = []
    curr_total = 0
    for line in lines:
        if line == "":
            totals.append(curr_total)
            curr_total = 0
        else:
            curr_total += int(line)

    return totals


def part2(totals: list[int]) -> int:
    totals.sort(reverse=True)
    top_three = totals[0:3]
    return sum(top_three)


def main(file_name: str):
    lines = read_file(file_name)
    totals = parse_input(lines)
    print("Part1:", max(totals))
    print("Part2", part2(totals))


if __name__ == "__main__":
    main(sys.argv[1])
