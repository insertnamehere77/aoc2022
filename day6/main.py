import sys


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


def scan_for_no_repeats(signal: str, window: int) -> int:
    look_behind = window - 1
    for i in range(look_behind, len(signal)):
        marker = signal[i - look_behind : i + 1]
        if len(set(marker)) == window:
            return i + 1


def main(file_name: str):
    line = read_file(file_name)[0]
    print("Part1:", scan_for_no_repeats(line, 4))
    print("Part2:", scan_for_no_repeats(line, 14))


if __name__ == "__main__":
    main(sys.argv[1])
