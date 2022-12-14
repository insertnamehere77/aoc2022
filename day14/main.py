import sys
from dataclasses import dataclass


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


def point_key(x: int, y: int) -> str:
    return f"({x}, {y})"


@dataclass
class Point:
    x: int
    y: int

    def key(self) -> str:
        return point_key(self.x, self.y)


@dataclass
class LineSegment:
    start: Point
    end: Point

    def points(self) -> list[Point]:
        x_max = max(self.start.x, self.end.x)
        x_min = min(self.start.x, self.end.x)

        y_max = max(self.start.y, self.end.y)
        y_min = min(self.start.y, self.end.y)

        points = []
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                points.append(Point(x, y))

        return points


def parse_input(lines: list[str]) -> list[LineSegment]:
    segments = []
    for line in lines:
        prev_point = None
        point_strs = [p.strip(" ") for p in line.split("->")]
        for point_str in point_strs:
            [x_str, y_str] = point_str.split(",")
            point = Point(int(x_str), int(y_str))
            if prev_point != None:
                segments.append(LineSegment(prev_point, point))
            prev_point = point

    return segments


def fall(sand: Point, grid: set[str]) -> bool:
    next = point_key(sand.x, sand.y + 1)
    if next not in grid:
        sand.y += 1
        return True

    next = point_key(sand.x - 1, sand.y + 1)
    if next not in grid:
        sand.x -= 1
        sand.y += 1
        return True

    next = point_key(sand.x + 1, sand.y + 1)
    if next not in grid:
        sand.x += 1
        sand.y += 1
        return True

    return False


def drop(y_max: int, grid: set[str]) -> bool:
    sand = Point(500, 0)
    while fall(sand, grid):
        if y_max < sand.y:
            return False

    grid.add(sand.key())
    return True


def flatten(matrix: list[list[any]]) -> list[any]:
    result = []
    for row in matrix:
        for item in row:
            result.append(item)

    return result


def part1(segments: list[LineSegment]) -> int:
    segment_points = flatten([s.points() for s in segments])
    y_max = max([p.y for p in segment_points])
    grid = set(p.key() for p in segment_points)

    num_sand = 0
    while drop(y_max, grid):
        num_sand += 1

    return num_sand


def drop_with_floor(floor_level: int, grid: set[str]) -> bool:
    sand = Point(500, 0)
    while fall(sand, grid):
        if floor_level < sand.y:
            return False

        # Add a point to the grid at the floor level for any possible x the sand might drop to
        # If there's no sand around to fall on the floor, does the floor really exist?
        grid.update(point_key(x, floor_level) for x in [sand.x - 1, sand.x, sand.x + 1])

    grid.add(sand.key())
    return True


def part2(segments: list[LineSegment]) -> int:
    segment_points = flatten([s.points() for s in segments])
    floor_level = max([p.y for p in segment_points]) + 2
    grid = set(p.key() for p in segment_points)

    num_sand = 0
    while drop_with_floor(floor_level, grid):
        num_sand += 1
        if point_key(500, 0) in grid:
            break

    return num_sand


def main(file_name: str):
    lines = read_file(file_name)
    segments = parse_input(lines)
    print("Part1:", part1(segments))
    print("Part2:", part2(segments))


if __name__ == "__main__":
    main(sys.argv[1])
