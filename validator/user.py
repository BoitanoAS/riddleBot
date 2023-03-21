from dataclasses import dataclass

from guess import Guess


@dataclass
class User:
    user_id: str
    guess: Guess
    has_guessed: bool = False
    name: str = ""
