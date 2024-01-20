import dataclasses

from game.dice import DiceOptions
from game.guess import Guess
from player.player import Player, PlayerStatus
from pydantic import BaseModel


class GameData(BaseModel):
    game_id: str
    players_ids: list[int]


@dataclasses.dataclass
class Game:
    game_id: str
    last_guess: Guess = None
    current_player_index: int = 0
    players: list[Player] = dataclasses.field(default_factory=list)

    @property
    def dices(self) -> list[DiceOptions]:
        dices: list[DiceOptions] = []
        for player in self.players:
            dices += player.dices

        return dices

    @property
    def status(self) -> list[PlayerStatus]:
        return [
            PlayerStatus(player_id=player.player_id, dices_left=player.dices_left) for player in self.players
            ]

    @property
    def players_ids(self) -> list[int]:
        return [player.id for player in self.players]

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index % len(self.players)]

    @property
    def previes_player(self) -> Player:
        return self.players[(self.current_player_index - 1) % len(self.players)]

    @property
    def last_guess_true(self) -> bool:
        jokers = self.dices.count(DiceOptions.JOKER)
        number_of_hits = self.dices.count(self.last_guess.dice)
        return self.last_guess.number_of_hits >= number_of_hits + jokers

    def lie(self) -> None:
        self.continue_to_next_player()
        if self.last_guess_true:
            self.current_player.remove_dice()
        else:
            self.previes_player.remove_dice()

    def roll_dices(self) -> None:
        for player in self.players:
            player.roll_dices()

    def continue_to_next_player(self) -> None:
        self.current_player_index += 1
