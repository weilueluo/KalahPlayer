from game.mancala import Mancala


class Agent:
    def get_move(self, game: Mancala, side: str):
        raise NotImplementedError
