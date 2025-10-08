"""
A simple robot simulator on a 2D grid.
"""

from enum import Enum
from typing import Tuple


class Facing(Enum):  # Facing 我们定义为一个枚举类，用于定义方向。如有疑问可以自行 Google / Ask AI
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3


class Grid():
    def __init__(self, width: int, height: int, enemy_pos: tuple):  # DO NOT EDIT THIS METHOD
        self.width: int = width
        self.height: int = height
        self._current_pos: tuple = (0, 0)
        self.current_direction = Facing.UP
        self.enemy_pos: tuple = enemy_pos
        self.position_history: dict = {}  # 用于存储位置历史，键为步数，值为坐标

    @property
    def current_pos(self) -> Tuple[int, int]:
        """
        current_pos 属性的 getter，返回私有属性 _current_pos
        """
        return self._current_pos

    @current_pos.setter
    def current_pos(self, value: Tuple[int, int]) -> None:
        """
        current_pos 属性的 setter（作为第 1 题留空）

        要求：
          - 接受一个长度为 2 的 tuple (x, y)
          - 若传入非 tuple 或长度不为 2，应抛出 TypeError
          - 将 x, y 强制转换为 int ，检查是否超出了宽高范围，如果任何一个超出则将其限制在最大宽高范围即可
          - 处理后存入 self._current_pos
        """
        # 检查输入类型和长度
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError("current_pos must be a tuple of length 2")
        
        # 强制转换为int
        try:
            x = int(value[0])
            y = int(value[1])
        except (ValueError, TypeError):
            raise TypeError("tuple elements must be convertible to int")
        
        # 限制在网格范围内
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        
        self._current_pos = (x, y)

    def move_forward(self) -> Tuple[int, int]:
        '''
        让机器人向当前方向走一格
        返回新的坐标 (x,y) 同时更新成员变量
        利用好上面的 setter
        以右为X轴正方向，上为Y轴正方向
        '''
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
            new_pos = (x, y)  # 不应发生
        
        # 使用setter更新位置（自动处理边界）
        self.current_pos = new_pos
        return self.current_pos

    def turn_left(self) -> Facing:
        '''
        让机器人逆时针转向
        返回一个新方向 (Facing.UP/DOWN/LEFT/RIGHT)
        '''
        # 逆时针转向：RIGHT→UP→LEFT→DOWN→RIGHT
        new_value = (self.current_direction.value + 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def turn_right(self) -> Facing:
        '''
        让机器人顺时针转向
        '''
        # 顺时针转向：RIGHT→DOWN→LEFT→UP→RIGHT
        new_value = (self.current_direction.value - 1) % 4
        self.current_direction = Facing(new_value)
        return self.current_direction

    def find_enemy(self) -> bool:
        '''
        如果找到敌人（机器人和敌人坐标一致），就返回true
        '''
        return self.current_pos == self.enemy_pos

    def record_position(self, step: int) -> None:
        '''
        将当前位置记录到 position_history 字典中
        键(key)为步数 step，值(value)为当前坐标 self.current_pos
        例如：step=1 时，记录 {1: (0, 0)}
        '''
        self.position_history[step] = self.current_pos

    def get_position_at_step(self, step: int) -> tuple:
        '''
        从 position_history 字典中获取指定步数的坐标
        如果该步数不存在，返回 None
        '''
        return self.position_history.get(step)


"""
在这里你需要实现 AdvancedGrid 类，继承自 Grid 类，并添加以下功能：
1. 追踪移动步数
2. 计算到敌人的曼哈顿距离

类名：AdvancedGrid
继承自：Grid
包含以下新属性：
- steps: int - 追踪移动步数，初始值为 0

包含以下方法：
1. move_forward(self) -> Tuple[int, int]
    调用父类的 move_forward 方法完成移动
    新增实现：移动步数 self.steps 加 1
    返回：移动后新坐标

2. distance_to_enemy(self) -> int
    计算当前位置到敌人位置的曼哈顿距离
    曼哈顿距离 = |x1 - x2| + |y1 - y2|
    返回：曼哈顿距离值

"""
class AdvancedGrid(Grid):
    def __init__(self, width: int, height: int, enemy_pos: tuple):
        super().__init__(width, height, enemy_pos)
        self.steps = 0  # 初始化移动步数为0

    def move_forward(self) -> Tuple[int, int]:
        # 调用父类方法完成移动
        super().move_forward()
        # 移动步数加1
        self.steps += 1
        # 返回新坐标
        return self.current_pos

    def distance_to_enemy(self) -> int:
        # 获取当前位置和敌人位置
        x1, y1 = self.current_pos
        x2, y2 = self.enemy_pos
        # 计算曼哈顿距离
        return abs(x1 - x2) + abs(y1 - y2)
