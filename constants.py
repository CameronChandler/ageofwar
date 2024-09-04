from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)

    def __get__(self, instance, owner):
        return self.value