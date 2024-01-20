from uuid import uuid4

from fastapi import FastAPI, Response, status
from game.dice import DiceOptions
from game.game import Game, GameData
from game.guess import Guess
from player.player import Player, PlayerStatus

app =  FastAPI()
games: list[Game] = []
player_ids: list[int] = []

@app.post("/take_guess")
def take_guess(
    player_id: int,
    dice_value: int,
    number_of_hits: int,
    response: Response,
    ) -> None:
    game = find_game_by_player_id(player_id)
    if player_id != game.current_player.id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return

    if dice_value not in DiceOptions.values():
        response.status_code = status.HTTP_400_BAD_REQUEST
        return

    guess = Guess(number_of_hits, DiceOptions(dice_value))
    if guess > game.last_guess:
        game.last_guess = guess
        game.continue_to_next_player()
        response.status_code = status.HTTP_200_OK

    else:
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE

@app.post("/lie")
def lie(player_id: int, response: Response) -> list[PlayerStatus] | str:
    game = find_game_by_player_id(player_id)
    if player_id != game.current_player.id:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return f"Thats not your turn bro. This is {game.current_player.id} turn."

    game.lie()
    return game.status


@app.post("/create_new_game")
def create_new_game(player_id: int, response: Response) -> str:
    if player_id in player_ids:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return f"player id {player_id} already in use."

    new_player = Player(player_id)
    player_ids.append(player_id)
    new_game = Game(game_id=str(uuid4()))
    new_game.players.append(new_player)
    games.append(new_game)
    response.status_code = status.HTTP_201_CREATED
    return new_game.game_id


@app.patch("/join_game")
def join_game(game_id: str, player_id: int, response: Response) -> None:
    game = find_game_by_id(game_id)
    if player_id not in player_ids:
        player_ids.append(player_id)
        game.players.append(Player(player_id))

    else:
        response.status_code = status.HTTP_400_BAD_REQUEST

@app.post("/roll_dices")
def roll_dices(game_id: str) -> None:
    find_game_by_id(game_id).roll_dices()


@app.get("/get_dice")
def get_dice(player_id: int) -> list[int]:
    return find_player_by_id(player_id).dices


@app.get("/get_games")
def get_games() -> list[GameData]:
    return [GameData(game_id=game.game_id, players_ids=game.players_ids) for game in games]

@app.get("/get_current_player_id")
def get_current_player_id(game_id: str) -> int:
    return find_game_by_id(game_id).current_player.id

def find_game_by_id(game_id: str) -> Game:
    for game in games:
        if game.game_id == game_id:
            return game

    raise ValueError(f"Game id {game_id} was not found in games.")


def find_game_by_player_id(player_id: int) -> Game:
    for game in games:
        if player_id in game.players_ids:
            return game

    raise ValueError(f"player id {player_id} was not found in any of the games.")


def find_player_by_id(player_id: int) -> Player:
    for player in find_game_by_player_id(player_id).players:
        if player.id == player_id:
            return player

    raise ValueError(f"player id {player_id} was not found.")
