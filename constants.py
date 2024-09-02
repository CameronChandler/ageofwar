from enum import Enum

class Color(Enum):
    WHITE = (255, 255, 255)

    def __get__(self, instance, owner):
        return self.value