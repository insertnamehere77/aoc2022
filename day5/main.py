import sys, re


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


def find_stack_lines(lines: list[str]) -> list[str]:
    stack_lines = []
    for line in lines:
        if line != "":
            stack_lines.append(line)
        else:
            break
    # Reverse them so we can build the stacks easier
    stack_lines.reverse()
    return stack_lines


def parse_initial_stack(lines: list[str]) -> list[list[str]]:
    stack_lines = find_stack_lines(lines)
    num_stacks = len(re.findall("\d+", stack_lines[0]))
    stacks = [[] for i in range(0, num_stacks)]

    for i in range(1, len(stack_lines)):
        # Prolly not a bullet proof regex but works well enough for an AOC
        matches = re.findall("(\[([A-Z])\]|(   )) {0,1}", stack_lines[i])
        for s in range(0, len(matches)):
            match = matches[s][1]
            if match != "":
                stacks[s].append(match)

    return stacks


def find_move_lines(lines: list[str]) -> list[str]:
    for i in range(0, len(lines)):
        if lines[i] == "":
            return lines[i + 1 :]


class Move:
    num: int
    source: int
    dest: int

    def __init__(self, num: int, source: int, dest: int) -> None:
        self.num = num
        self.source = source
        self.dest = dest

    def __str__(self) -> str:
        return f"move {self.num} from {self.source} to {self.dest}"


def parse_moves(lines: list[str]):
    move_lines = find_move_lines(lines)
    moves = []
    for line in move_lines:
        matches = re.findall("\d+", line)
        move = Move(int(matches[0]), int(matches[1]), int(matches[2]))
        moves.append(move)

    return moves


def part1(lines: list[str], moves: list[Move]) -> str:
    # Both part1 and 2 create their own copy of stacks so we can modify in place
    stacks = parse_initial_stack(lines)
    for move in moves:
        source = stacks[move.source - 1]
        dest = stacks[move.dest - 1]
        for _ in range(0, move.num):
            dest.append(source.pop())

    return "".join([stack.pop() for stack in stacks])


def part2(lines: list[str], moves: list[Move]) -> str:
    stacks = parse_initial_stack(lines)
    for move in moves:
        source = stacks[move.source - 1]
        dest = stacks[move.dest - 1]
        dest.extend(source[-move.num :])
        # Need to modify the actual stack variable bc "source" is just a ref to it
        stacks[move.source - 1] = source[: -move.num]

    return "".join([stack.pop() for stack in stacks])


def main(file_name: str):
    lines = read_file(file_name)
    moves = parse_moves(lines)
    print("Part1:", part1(lines, moves))
    print("Part2:", part2(lines, moves))


if __name__ == "__main__":
    main(sys.argv[1])
