import enum


class Move(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(enum.IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


class Round:
    opponent: Move
    out: Outcome

    def __init__(self, opponent: Move, out: Outcome) -> None:
        self.opponent = opponent
        self.out = out

    def score(self) -> int:
        if self.out == Outcome.DRAW:
            return self.out + self.opponent
        if self.out == Outcome.WIN:
            me = Move.ROCK if self.opponent == Move.SCISSORS else self.opponent + 1
            return self.out + me
        if self.out == Outcome.LOSE:
            me = Move.SCISSORS if self.opponent == Move.ROCK else self.opponent - 1
            return self.out + me


def translate_opponent(m: str) -> Move:
    if m == "A":
        return Move.ROCK
    elif m == "B":
        return Move.PAPER
    else:
        return Move.SCISSORS


def translate_outcome(o: str) -> Outcome:
    if o == "X":
        return Outcome.LOSE
    elif o == "Y":
        return Outcome.DRAW
    else:
        return Outcome.WIN


def parse_input(lines: list[str]) -> list[Round]:
    rounds = []
    for line in lines:
        opp = line[0]
        out = line[2]
        rounds.append(Round(translate_opponent(opp), translate_outcome(out)))

    return rounds


def score_rounds(rounds: list[Round]) -> int:
    total = 0
    for round in rounds:
        total += round.score()

    return total


def run(lines: list[str]) -> int:
    rounds = parse_input(lines)
    return score_rounds(rounds)
