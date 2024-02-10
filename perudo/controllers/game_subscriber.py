from dataclasses import dataclass

from fastapi import WebSocket

from perudo.player.player import PlayerStatus


@dataclass
class GameSubscribers:
    game_id: str
    subscribers: list[WebSocket]

    def remove_subscriber(self, subscriber: WebSocket) -> None:
        self.subscribers.remove(subscriber)

    def add_subscriber(self, subscriber: WebSocket) -> None:
        self.subscribers.append(subscriber)


class GameSubscriberManager:
    def __init__(self):
        self.games: list[GameSubscribers] = []

    async def connect(self, websocket: WebSocket, game_id: str) -> None:
        await websocket.accept()
        self.add_to_game(websocket, game_id)

    def disconnect(self, subscriber: WebSocket) -> None:
        for game in self.games:
            if subscriber in game.subscribers:
                game.remove_subscriber(subscriber)

    def add_to_game(self, websocket: WebSocket, game_id: str) -> None:
        for game in self.games:
            if game_id == game.game_id:
                game.add_subscriber(websocket)
                return

        self.games.append(GameSubscribers(game_id, [websocket]))

    def get_game_by_id(self, game_id: str) -> GameSubscribers:
        for game in self.games:
            if game_id == game.game_id:
                return game

        raise ValueError(f"Game with id {game_id} doesnt exists.")

    async def broadcast_to_game(self, game_status: list[PlayerStatus], game_id: str) -> None:
        game = self.get_game_by_id(game_id)
        for subscriber in game.subscribers:
            await subscriber.send_json(game_status)
