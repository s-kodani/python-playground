"""this program is based on the program that written in Effective Python.

    credit: https://github.com/bslatkin/effectivepython/blob/1ce625e697b0f71add394a023a4383832d2feb98/example_code/item_56.py

    ↓本家のソースコードはApache License 2.0
    http://www.apache.org/licenses/LICENSE-2.0
"""

from typing import Iterator, Union
from collections import namedtuple
from itertools import product


# Status Symbol
ALIVE = '*'
EMPTY = '-'

# object to recognize completed stepping all cell
TICK = object()

# posses a xy coordinate
Query = namedtuple('Query', ('y', 'x'))

# posses a xy coordinate and a status of next step
Transition = namedtuple('Transition', ('y', 'x', 'state'))


class ColumnPrinter(list):
    """複数StepのGridを横繋ぎで出力するためのクラス"""
    def __init__(self):
        self.columns = []

    def append(self, value: str):
        self.columns.append(value)

    def __str__(self):
        header = ''
        rows = []
        for column_i, column_value in enumerate(self.columns):
            row_length = 0
            for row_i, row_value in enumerate(column_value.split('\n')):
                if len(rows) < (row_i + 1):
                    rows.append(row_value)
                else:
                    rows[row_i] = rows[row_i] + '|' + row_value
                row_length = max(row_length, len(row_value))
            
            header = header + '|' + str(column_i).center(row_length)
        header = header.lstrip('|')
        return '\n'.join([header] + rows)


class Grid():
    """グリッドを設定、取得する"""
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        _str = ''
        for row in self.rows:
            _str = _str + ''.join(row) + '\n'
        
        _str = _str.rstrip('\n')
        return _str
    
    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]
    
    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


def count_neighbors(y: int, x: int) -> Union[namedtuple, int]:
    """隣接セルの状態を見て、生存セルの個数を返す"""
    neighbor_status = []
    for y_offset, x_offset in product(range(-1, 2, 1), repeat=2):
        print(y_offset, x_offset)
        if y_offset == 0 and x_offset == 0:
            # 自分自身のセルになる場合はcontinue
            continue

        _state = yield Query(y + y_offset, x + x_offset)
        neighbor_status.append(_state)

    return sum(1 if state == ALIVE else 0 for state in neighbor_status)


def game_logic(state: str, neighbors: int) -> str:
    """生死判定"""
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY
        elif neighbors > 3:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state


def step_cell(y: int, x: int) -> namedtuple:
    """次ステップのステータス決定"""
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def simulate(height: int, width: int) -> Union[namedtuple, object]:
    """全てのセルに対して、step_cell()を実行する"""
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


def live_a_generation(grid: Grid, sim: Iterator) -> Grid:

    # 次ステップGridを設定するためのオブジェクト
    progeny = Grid(grid.height, grid.width)

    # ここでは初期の座標に対するQueryオブジェクトが取得される
    item = next(sim)

    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            # the item object should be Transition object
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


def main():
    columns = ColumnPrinter()

    # 初期状態のGridを設定
    grid = Grid(5, 9)
    grid.assign(0, 3, ALIVE)
    grid.assign(1, 4, ALIVE)
    grid.assign(2, 2, ALIVE)
    grid.assign(2, 3, ALIVE)
    grid.assign(2, 4, ALIVE)

    # 初期状態のGridをappendしておく
    columns.append(str(grid))

    # simulateコルーチン
    sim = simulate(grid.height, grid.width)

    for _ in range(5):
        grid = live_a_generation(grid, sim)
        columns.append(str(grid))
    
    print(columns)


# def main_throughout_count_neighbors():
#     """count_neighbors()のお試し実行"""
#     it = count_neighbors(10, 5)

#     q1 = next(it)
#     print('q1 yield:', q1)
#     q2 = it.send(ALIVE)
#     print('q2 yield:', q2)
#     q3 = it.send(ALIVE)
#     print('q3 yield:', q3)
#     q4 = it.send(EMPTY)
#     print('q4 yield:', q4)
#     q5 = it.send(EMPTY)
#     print('q5 yield:', q5)
#     q6 = it.send(EMPTY)
#     print('q6 yield:', q6)
#     q7 = it.send(EMPTY)
#     print('q7 yield:', q7)
#     q8 = it.send(EMPTY)
#     print('q8 yield:', q8)
#     try:
#         it.send(EMPTY)
#     except StopIteration as e:
#         print('Count:', e.value)


# def main_throughout_step_cell():
#     """step_cell()のお試し実行"""
#     it = step_cell(10, 5)
#     next(it)
#     it.send(ALIVE)
    
#     for _ in range(2):
#         it.send(ALIVE)
    
#     for _ in range(6):
#         t = it.send(EMPTY)

#     print('Outcome:', t)


# def main_throughout_grid():
#     grid = Grid(5, 9)
#     grid.assign(0, 3, ALIVE)
#     grid.assign(1, 4, ALIVE)
#     grid.assign(2, 2, ALIVE)
#     grid.assign(2, 3, ALIVE)
#     grid.assign(2, 4, ALIVE)
#     print(grid)


if __name__ == '__main__':
    # main_throughout_count_neighbors()
    # main_throughout_step_cell()
    # main_throughout_grid()
    main()