import sys, math


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip(), f.readlines()))


def parse_single_bags(lines: list[str]) -> list[str]:
    shared = []
    for line in lines:
        half_point = math.floor(len(line) / 2)
        first_set = set(line[0:half_point])
        second = line[half_point:]
        for char in second:
            if char in first_set:
                shared.append(char)
                break

    return shared


def sum_shared_priority(shared: list[str]) -> int:
    total = 0
    for char in shared:
        unic_base = 96 if char.lower() == char else 38
        total += ord(char) - unic_base

    return total


def part1(lines: list[str]) -> int:
    shared = parse_single_bags(lines)
    return sum_shared_priority(shared)


def parse_grouped_bags(lines: list[str]) -> list[str]:
    shared = []
    for i in range(0, len(lines), 3):
        group_no_dups = map(lambda x: "".join(set(x)), lines[i : i + 3])
        group_combined = "".join(group_no_dups)
        occurences = dict()
        for char in group_combined:
            curr_count = (occurences[char] if char in occurences else 0) + 1
            occurences[char] = curr_count
            if curr_count == 3:
                shared.append(char)
                break

    return shared


def part2(lines: list[str]) -> int:
    shared = parse_grouped_bags(lines)
    return sum_shared_priority(shared)


def main(file_name: str):
    lines = read_file(file_name)
    print("Part1:", part1(lines))
    print("Part2:", part2(lines))


if __name__ == "__main__":
    main(sys.argv[1])
