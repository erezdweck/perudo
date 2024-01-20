from __future__ import annotations

from dataclasses import dataclass

from game.dice import DiceOptions
from system.consts import DOUBLE


@dataclass
class Guess:
    number_of_hits: int
    dice: DiceOptions

    def __gt__(self: Guess, last_guess: Guess | None) -> bool:
        if last_guess is None:
            return True

        self.number_of_hits *= DOUBLE if self.dice == DiceOptions.JOKER else 1

        if self.number_of_hits > last_guess.number_of_hits:
            return True

        if self.number_of_hits == last_guess.number_of_hits and\
              self.dice.dice_value > last_guess.dice.dice_value:
            return True

        return False

