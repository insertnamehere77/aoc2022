import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


class File:
    name: str
    size: int

    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size

    def get_size(self) -> int:
        return self.size

    def str(self, depth: int) -> str:
        indent = "  " * depth
        return f"{indent}- {self.name} (file, size={self.size})"


class Folder:
    name: str
    parent: "Folder"
    children: dict["Folder"]

    def __init__(self, name: str, parent: "Folder" = None) -> None:
        self.name = name
        self.parent = parent
        self.children = {}

    def get_size(self) -> int:
        return sum(x.get_size() for x in self.children.values())

    def add_dir(self, name: str):
        self.children[name] = Folder(name, self)

    def add_file(self, name: str, size: int):
        self.children[name] = File(name, size)

    def str(self, depth: int = 0) -> str:
        child_str = "\n".join(x.str(depth + 1) for x in self.children.values())
        indent = "  " * depth
        return f"{indent}- {self.name} (dir)\n{child_str}"


class FileParser:
    root: Folder
    curr_dir = Folder
    curr_line: int

    def __init__(self) -> None:
        self.root = Folder("/")
        self.curr_dir = self.root
        self.curr_line = 0

    def consume(self):
        self.curr_line += 1

    def handle_cd(self, dir_name: str):
        if dir_name == "/":
            self.curr_dir = self.root
        elif dir_name == "..":
            self.curr_dir = self.curr_dir.parent
        else:
            self.curr_dir = self.curr_dir.children[dir_name]

        self.consume()

    def handle_ls(self, lines: list[str]):
        self.consume()
        while self.curr_line < len(lines):
            line = lines[self.curr_line]
            parts = line.split(" ")

            desc = parts[0]
            name = parts[1]
            if desc == "dir":
                self.curr_dir.add_dir(name)
            elif desc.isnumeric():
                self.curr_dir.add_file(name, int(desc))
            else:
                # End of LS output
                break

            self.consume()

    def parse_input(self, lines: list[str]) -> Folder:

        while self.curr_line < len(lines):
            line = lines[self.curr_line]
            op = line[2:4]
            if op == "cd":
                self.handle_cd(line[5:])
            elif op == "ls":
                self.handle_ls(lines)
            else:
                raise Exception(
                    f"Parser expected a $ command but instead got {op} on line {self.curr_line + 1}"
                )

        return self.root


def part1(root: Folder) -> int:
    total_size = 0
    for child in root.children.values():
        if type(child) == Folder:
            total_size += part1(child)
            if child.get_size() <= 100000:
                total_size += child.get_size()

    return total_size


def part2_search(root: Folder, needed: int) -> list[int]:
    delete_options = []
    for child in root.children.values():
        if type(child) == Folder:
            delete_options.extend(part2_search(child, needed))
            if child.get_size() >= needed:
                delete_options.append(child.get_size())

    return delete_options


def part2(root: Folder, total: int, update_size: int) -> int:
    needed = update_size - (total - root.get_size())
    return min(part2_search(root, needed))


def main(file_name: str):
    lines = read_file(file_name)
    parser = FileParser()
    root = parser.parse_input(lines)
    print("Part1:", part1(root))
    print("Part2:", part2(root, 70000000, 30000000))


if __name__ == "__main__":
    main(sys.argv[1])
