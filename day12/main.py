import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


class Node:
    x: int
    y: int
    val: str
    height: int
    adjacents: list["Node"]

    def __init__(self, x: int, y: int, val: str) -> None:
        self.x = x
        self.y = y
        self.val = val
        self.height = ord(val)
        self.adjacents = []

    def get_key(self) -> str:
        return f"({self.x}, {self.y})"

    def __str__(self) -> str:
        return self.get_key()


def get_adj_coords(x: int, y: int, grid: list[list[any]]) -> list[tuple[int, int]]:
    coords = []
    if x > 0:
        coords.append((x - 1, y))

    if x < len(grid[y]) - 1:
        coords.append((x + 1, y))

    if y > 0:
        coords.append((x, y - 1))

    if y < len(grid) - 1:
        coords.append((x, y + 1))

    return coords


def get_adj_nodes(curr: Node, grid: list[list[Node]]) -> list[Node]:
    adj_nodes = []
    adj_coords = get_adj_coords(curr.x, curr.y, grid)
    for coord in adj_coords:
        adj_nodes.append(grid[coord[1]][coord[0]])

    return adj_nodes


def parse_input(lines: list[str]) -> tuple[Node, Node, list[list[Node]]]:
    grid = [[None for _ in range(0, len(line))] for line in lines]
    start = None
    end = None
    for y in range(0, len(lines)):
        row = lines[y]
        for x in range(0, len(row)):
            val = row[x]
            node = Node(x, y, val)
            grid[y][x] = node

            if val == "S":
                node.height = ord("a")
                start = node
            elif val == "E":
                node.height = ord("z")
                end = node

    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            node = row[x]
            node.adjacents = get_adj_nodes(node, grid)

    return (start, end, grid)


def shortest_path(start: Node, end: Node) -> int:
    shortest = {start.get_key(): 0}
    queue = [start]
    while queue:
        curr = queue.pop(0)
        path = shortest.get(curr.get_key()) + 1

        for adj in curr.adjacents:
            if adj.height - curr.height <= 1 and (
                adj.get_key() not in shortest or shortest[adj.get_key()] > path
            ):
                shortest[adj.get_key()] = path
                queue.append(adj)

    return shortest.get(end.get_key()) if end.get_key() in shortest else float("inf")


def part2(end: Node, grid: list[list[Node]]) -> int:
    possible_starts = []
    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            node = row[x]
            if node.height == ord("a"):
                possible_starts.append(node)

    return min([shortest_path(node, end) for node in possible_starts if node != None])


def main(file_name: str):
    lines = read_file(file_name)
    [start, end, grid] = parse_input(lines)
    print("Part1:", shortest_path(start, end))
    print("Part2:", part2(end, grid))


if __name__ == "__main__":
    main(sys.argv[1])
