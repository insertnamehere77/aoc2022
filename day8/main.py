import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


class Node:
    x: int
    y: int
    height: int

    def __init__(self, x: int, y: int, height: int) -> None:
        self.x = x
        self.y = y
        self.height = height

    def __str__(self) -> str:
        return f"h: {self.height}, x: {self.x}, y: {self.y}"


def parse_input(lines: list[str]) -> list[list[Node]]:
    map = [[None for _ in range(0, len(lines[0]))] for _ in range(0, len(lines))]

    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(line)):
            height = int(line[x])
            map[y][x] = Node(x, y, height)

    return map


def is_on_edge(node: Node, map: list[list[Node]]) -> bool:
    if node.x == 0 or node.y == 0:
        return True

    if node.x == (len(map[0]) - 1) or node.y == (len(map) - 1):
        return True

    return False


def is_visible_in_dir(
    start_node: Node, curr_node: Node, x_step: int, y_step: int, map: list[list[Node]]
) -> bool:

    if is_on_edge(curr_node, map):
        return True

    # Node inside
    adj_node = map[curr_node.y + y_step][curr_node.x + x_step]
    return adj_node.height < start_node.height and is_visible_in_dir(
        start_node, adj_node, x_step, y_step, map
    )


def is_visible(node: Node, map: list[list[Node]]) -> bool:
    return (
        is_visible_in_dir(node, node, 1, 0, map)
        or is_visible_in_dir(node, node, -1, 0, map)
        or is_visible_in_dir(node, node, 0, 1, map)
        or is_visible_in_dir(node, node, 0, -1, map)
    )


def part1(map: list[list[Node]]) -> int:
    num_visible = 0
    for y in range(0, len(map)):
        line = map[y]
        for x in range(0, len(line)):
            node = line[x]
            if is_visible(node, map):
                num_visible += 1

    return num_visible


def count_in_dir(
    start_node: Node, curr_node: Node, x_step: int, y_step: int, map: list[list[Node]]
) -> int:

    view_dist = 1

    if curr_node.height < start_node.height and not is_on_edge(curr_node, map):
        adj_node = map[curr_node.y + y_step][curr_node.x + x_step]
        view_dist += count_in_dir(start_node, adj_node, x_step, y_step, map)

    return view_dist


def scenic_score(node: Node, map: list[list[Node]]) -> int:

    if is_on_edge(node, map):
        return 0

    return (
        count_in_dir(node, map[node.y][node.x + 1], 1, 0, map)
        * count_in_dir(node, map[node.y][node.x - 1], -1, 0, map)
        * count_in_dir(node, map[node.y + 1][node.x], 0, 1, map)
        * count_in_dir(node, map[node.y - 1][node.x], 0, -1, map)
    )


def part2(map: list[list[Node]]) -> int:
    scores = []
    for y in range(0, len(map)):
        line = map[y]
        for x in range(0, len(line)):
            node = line[x]
            scores.append(scenic_score(node, map))

    return max(scores)


def main(file_name: str):
    lines = read_file(file_name)
    map = parse_input(lines)
    print("Part1:", part1(map))
    print("Part2:", part2(map))


if __name__ == "__main__":
    main(sys.argv[1])
