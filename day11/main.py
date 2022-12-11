import sys, re, functools
from typing import Callable


def read_file(file_name: str) -> list[str]:
    with open(file_name, "r") as f:
        return list(map(lambda l: l.strip("\n"), f.readlines()))


class Monkey:
    items: list[int]
    operation: Callable
    test: Callable
    test_val: int
    num_inspections = 0

    def inspect(self, careful: bool) -> int:
        self.num_inspections += 1
        self.items[0] = self.operation(self.items[0])
        if careful:
            self.items[0] = self.items[0] // 3

    def throw(self) -> tuple[int, int]:
        val = self.items.pop(0)
        throw_to = self.test(val)
        return (throw_to, val)


class MonkeyParser:
    curr_line: int = 0

    def consume(self):
        self.curr_line += 1

    def parse_items(self, line: str) -> list[int]:
        matches = re.findall("([\d]+)", line)
        self.consume()
        return [int(x) for x in matches]

    def parse_operation(self, line: str) -> Callable:
        [operator, operand] = re.findall("([*+]) ([\d]+|old)", line)[0]
        operator_lambda = lambda a, b: a * b if operator == "*" else a + b
        self.consume()
        return (
            lambda a: operator_lambda(a, a)
            if operand == "old"
            else operator_lambda(a, int(operand))
        )

    def parse_test(self, lines: list[str]) -> Callable:
        div_check = int(re.findall("([\d]+)", lines[self.curr_line])[0])
        self.consume()
        true_val = int(re.findall("([\d]+)", lines[self.curr_line])[0])
        self.consume()
        false_val = int(re.findall("([\d]+)", lines[self.curr_line])[0])
        self.consume()
        return (lambda a: true_val if (a % div_check == 0) else false_val, div_check)

    def parse_monkey(self, lines: list[str]) -> Monkey:
        monkey = Monkey()
        monkey.items = self.parse_items(lines[self.curr_line])
        monkey.operation = self.parse_operation(lines[self.curr_line])
        [monkey.test, monkey.test_val] = self.parse_test(lines)
        self.consume()
        return monkey

    def parse_monkeys(self, lines: list[str]) -> list[Monkey]:
        monkeys = []
        while self.curr_line < len(lines):
            line = lines[self.curr_line]
            if line[0:6] == "Monkey":
                self.consume()
                monkeys.append(self.parse_monkey(lines))
            else:
                raise Exception(f"Expected beginning on Monkey definition, got {line}")

        return monkeys


def run_rounds(lines: list[str], num_rounds: int, careful: bool) -> int:
    monkeys = MonkeyParser().parse_monkeys(lines)
    # Running part 2 causes our item values to get crazy high and takes forever to run/overflows
    # Because all of our test functions are checking if the item value is divisible by test_val,
    # We really only care about remainder of (item / test_val) and don't actually need the full value
    # Here LCM acts as a "cap" on the item values using modulo
    # Our items values never exceed LCM, and bc it's a multiple of all test vals it preserves the remainders for all of them
    least_common_multiple = functools.reduce(
        lambda a, b: a * b, [monkey.test_val for monkey in monkeys]
    )

    for _ in range(0, num_rounds):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                monkey.inspect(careful)
                [throw_to, item] = monkey.throw()
                monkeys[throw_to].items.append(item % least_common_multiple)

    num_inspections = sorted(
        [monkey.num_inspections for monkey in monkeys], reverse=True
    )
    return num_inspections[0] * num_inspections[1]


def main(file_name: str):
    lines = read_file(file_name)
    print("Part1:", run_rounds(lines, 20, True))
    print("Part2:", run_rounds(lines, 10000, False))


if __name__ == "__main__":
    main(sys.argv[1])
