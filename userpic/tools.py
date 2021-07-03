from random import random
from typing import Tuple

WHITE_COLOR = "#fff"


def random_bool() -> bool:
    return random() < 0.5


def choose_color() -> str:
    return "f" if random_bool() else "6"


def preferred_colors() -> Tuple[str, str]:
    color = None
    while not color or color == WHITE_COLOR:
        color = f"#{choose_color()}{choose_color()}{choose_color()}"
    return WHITE_COLOR, color
