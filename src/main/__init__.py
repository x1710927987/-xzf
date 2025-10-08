"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple


class Facing(Enum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}

    @property
    def current_pos(self) -> Tuple[int, int]:
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        # 检查输入类型和长度
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError("current_pos must be a tuple of length 2")

        # 强制转换为int
        try:
            x = int(value[0])
            y = int(value[1])
        except (ValueError, TypeError):
            raise TypeError("tuple elements must be convertible to int")

        # 修正：坐标边界应为width和height（而非width-1和height-1）
        x = max(0, min(x, self.width))
        y = max(0, min(y, self.height))

        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:
        x, y = self.current_pos

        # 根据当前方向计算新坐标
        if self.current_direction == Facing.RIGHT:
            new_pos = (x + 1, y)
        elif self.current_direction == Facing.UP:
            new_pos = (x, y + 1)
        elif self.current_direction == Facing.LEFT:
            new_pos = (x - 1, y)
        elif self.current_direction == Facing.DOWN:
            new_pos = (x, y - 1)
        else:
            new_pos = (x, y)

        self.current_pos = new_pos
        return self.current_pos

    def turn_left(self) -> Facing:
        new_value = (self.current_direction.value + 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def turn_right(self) -> Facing:
        new_value = (self.current_direction.value - 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def find_enemy(self) -> bool:
        # 直接比较当前位置和敌人位置（边界处理修正后可正确匹配）
        return self.current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:
        self.position_history[step] = self.current_pos

    def get_position_at_step(self, step: int) -> tuple:
        return self.position_history.get(step)


class AdvancedGrid(Grid):
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        super().__init__(width, height, enemy_pos)
        self.steps = 0

    def move_forward(self) -> Tuple[int, int]:
        super().move_forward()
        self.steps += 1
        return self.current_pos

    def distance_to_enemy(self) -> int:
        x1, y1 = self.current_pos
        x2, y2 = self.enemy_pos
        return abs(x1 - x2) + abs(y1 - y2)
