import sys, ast, functools


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


def parse_input(lines: list[str]) -> list[tuple[list, list]]:
    curr = 0
    results = []
    while curr < len(lines):
        if lines[curr] == "":
            curr += 1
            continue

        left = ast.literal_eval(lines[curr])
        curr += 1
        right = ast.literal_eval(lines[curr])
        curr += 1
        results.append((left, right))

    return results


def wrap_if_int(val: any) -> list:
    return val if isinstance(val, list) else [val]


def in_right_order(left, right) -> bool:
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None

        return left < right

    if isinstance(left, list) and isinstance(right, list):
        for l in range(0, len(left)):
            # Right ran out
            if l >= len(right):
                return False

            result = in_right_order(left[l], right[l])
            if result == None:
                continue
            else:
                return result

        # Left ran out
        if len(left) < len(right):
            return True

        return None

    if isinstance(left, int) or isinstance(right, int):
        return in_right_order(wrap_if_int(left), wrap_if_int(right))


def part1(pairs: list[tuple[list, list]]) -> int:
    in_order = []
    for p in range(0, len(pairs)):
        pair = pairs[p]
        if in_right_order(pair[0], pair[1]):
            in_order.append(p + 1)

    return sum(in_order)


def part2(pairs: list[tuple[list, list]]) -> int:
    # Flattening the pairs
    packets = [[[2]], [[6]]]
    for pair in pairs:
        packets.append(pair[0])
        packets.append(pair[1])

    # Sorting the packets (bubble sort)
    sorted = False
    while not sorted:
        sorted = True
        for i in range(0, len(packets) - 1):
            if not in_right_order(packets[i], packets[i + 1]):
                sorted = False
                temp = packets[i]
                packets[i] = packets[i + 1]
                packets[i + 1] = temp

    # Finding and multiplying divider indexes
    div_packets = {"[[2]]", "[[6]]"}
    div_indexes = []
    for p in range(0, len(packets)):
        if packets[p].__str__() in div_packets:
            div_indexes.append(p + 1)

    return functools.reduce(lambda a, b: a * b, div_indexes)


def main(file_name: str):
    lines = read_file(file_name)
    pairs = parse_input(lines)
    print("Part1:", part1(pairs))
    print("Part2:", part2(pairs))


if __name__ == "__main__":
    main(sys.argv[1])
