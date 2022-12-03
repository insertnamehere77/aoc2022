import enum


class Move(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Round:
    opponent: Move
    me: Move

    def __init__(self, opponent: Move, me: Move) -> None:
        self.opponent = opponent
        self.me = me

    def score(self) -> int:
        won = (
            self.opponent < self.me
            or (self.me == Move.ROCK and self.opponent == Move.SCISSORS)
        ) and not (self.me == Move.SCISSORS and self.opponent == Move.ROCK)
        if won:
            return 6 + self.me

        tied = self.opponent == self.me
        if tied:
            return 3 + self.me

        return 0 + self.me


def translate_opponent(m: str) -> Move:
    if m == "A":
        return Move.ROCK
    elif m == "B":
        return Move.PAPER
    else:
        return Move.SCISSORS


def translate_me(m: str) -> Move:
    if m == "X":
        return Move.ROCK
    elif m == "Y":
        return Move.PAPER
    else:
        return Move.SCISSORS


def parse_input(lines: list[str]) -> list[Round]:
    rounds = []
    for line in lines:
        opp = line[0]
        me = line[2]
        rounds.append(Round(translate_opponent(opp), translate_me(me)))

    return rounds


def score_rounds(rounds: list[Round]) -> int:
    total = 0
    for round in rounds:
        total += round.score()

    return total


def run(lines: list[str]) -> int:
    rounds = parse_input(lines)
    return score_rounds(rounds)
