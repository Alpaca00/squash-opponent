import random
from functools import cached_property


class Cache:
    def __init__(self, email=False):
        self.email = email
        self.letters_v = ["a", "e", "i", "o", "u"]
        self.letters_c = [
            "b",
            "c",
            "d",
            "f",
            "g",
            "h",
            "j",
            "k",
            "l",
            "m",
            "n",
            "p",
            "q",
            "r",
            "s",
            "t",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]
        self.symbols = [".", "-", "_"]
        self.symbol_at = "@"
        self.numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.random_quantity = random.randint(256, 300)
        self.result = ""

    @cached_property
    def get_more_than_255_characters(self) -> str:
        for char in range(1, self.random_quantity + 1):
            rand_char_C = random.choice(self.letters_c)
            rand_char_V = random.choice(self.letters_v)
            rand_symbol = random.choice(self.symbols)
            rand_number = random.choice(self.numbers)
            self.result += (
                rand_char_C + rand_char_V + rand_symbol + rand_number
                )
        if self.email:
            return self.result + self.symbol_at + "gmail.com"
        else:
            return self.result
