import sys, math
from dataclasses import dataclass


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


@dataclass
class Move:
    dir: str
    mag: int


@dataclass
class Knot:
    x: int = 0
    y: int = 0

    def move_one(self, dir: str):
        if dir == "U":
            self.y += 1
        elif dir == "D":
            self.y -= 1
        elif dir == "R":
            self.x += 1
        elif dir == "L":
            self.x -= 1
        else:
            raise Exception(f"Idk what this direction is: {dir}")

    def distance_between(self, head: "Knot") -> int:
        return math.floor(math.dist([head.y, head.x], [self.y, self.x]))

    def follow_one(self, head: "Knot"):
        total_dist = self.distance_between(head)
        if total_dist <= 1:
            return

        x_dist = math.dist([head.x], [self.x])
        y_dist = math.dist([head.y], [self.y])
        if x_dist > 1 or (y_dist >= 2 and x_dist != 0):
            self.x += -1 if head.x < self.x else 1

        if y_dist > 1 or (x_dist >= 2 and y_dist != 0):
            self.y += -1 if head.y < self.y else 1


def parse_input(lines: list[str]) -> list[Move]:
    moves = []
    for line in lines:
        [dir, mag] = line.split(" ")
        moves.append(Move(dir, int(mag)))
    return moves


def simulate_knots(moves: list[Move], num_knots: int) -> int:
    knots = [Knot() for _ in range(0, num_knots)]
    head = knots[0]
    tail = knots[len(knots) - 1]
    visited = set()
    for move in moves:
        for _ in range(0, move.mag):
            head.move_one(move.dir)

            for i in range(1, len(knots)):
                knots[i].follow_one(knots[i - 1])

            visited.add(f"{tail.x}-{tail.y}")

    return len(visited)


def main(file_name: str):
    lines = read_file(file_name)
    moves = parse_input(lines)
    print("Part1:", simulate_knots(moves, 2))
    print("Part2:", simulate_knots(moves, 10))


if __name__ == "__main__":
    main(sys.argv[1])
