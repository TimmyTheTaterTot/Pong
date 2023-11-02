from copy import deepcopy


class Grid:
    """
    2D grid with (x, y) int indexed internal storage
    Has .width .height size properties
    """

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.array = [[None for i in range(width)] for j in range(height)]

    def __str__(self):
        """
        selfstr = ''
        for y in range(self.height):
            selfstr += '\n | '
            for x in range(self.width):
                selfstr += f'{self.grid[y][x]} | '
        return selfstr
        """
        return f"Grid({self.height}, {self.width}, first = {self.array[0][0]})"

    def __repr__(self):
        return f"Grid.build({self.array})"

    def __eq__(self, other):
        if isinstance(other, Grid):
            if self.array == other.array:
                return True
        elif type(other) == list:
            if self.array == other:
                return True
        return False

    def __len__(self):
        return len(self.array)

    def in_bounds(self, x, y):
        if x >= 0 and x < len(self.array[0]) and y >= 0 and y < len(self.array):
            return True
        else:
            return False

    def get(self, x, y):
        if self.in_bounds(x, y):
            return self.array[y][x]
        else:
            raise IndexError(f"Invalid grid index: {y}, {x}")

    def set(self, x, y, val):
        if self.in_bounds(x, y):
            self.array[y][x] = val
        else:
            raise IndexError(f"Invalid grid index: {y}, {x}")

    def copy(self):
        return deepcopy(self)

    @staticmethod
    def build(lst):
        Grid.check_list_malformed(lst)
        width = len(lst)
        height = len(lst[0])
        newgrid = Grid(height, width)
        newgrid.array = deepcopy(lst)
        return newgrid

    @staticmethod
    def check_list_malformed(lst):
        if type(lst) == list and len(lst) > 0:
            length = len(lst)
            height = len(lst[0])
            for x in range(length):
                if type(lst) != list or len(lst[x]) != height:
                    raise ValueError(
                        "Invalid input list. Ensure list is rectangular and all primary array values are lists."
                    )
