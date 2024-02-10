from __future__ import annotations

import os

from pydantic import BaseModel

from perudo.game.dice import DiceOptions
from perudo.system.consts import BYTE_ORDER

NUMBER_OF_OPTIONS = 6


class PlayerStatus(BaseModel):
    name: str
    player_id: int
    dices_left: int


class Player:
    def __init__(self, player_id: int, name: str) -> None:
        self.name = name
        self.dices_left = 5
        self._dices: list[DiceOptions] | None = None
        self.id = player_id

    def remove_dice(self) -> None:
        self.dices_left -= 1

    def roll_dices(self) -> None:
        self._dices = [self.roll_dice() for _ in range(self.dices_left)]

    @staticmethod
    def roll_dice() -> DiceOptions:
        return DiceOptions(int.from_bytes(bytes=os.urandom(8), byteorder=BYTE_ORDER) % NUMBER_OF_OPTIONS + 1)

    @property
    def dices(self) -> list[DiceOptions]:
        if self._dices is None:
            raise RuntimeError("Player doesn't have any dices...")

        return self._dices
