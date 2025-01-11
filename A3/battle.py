import sys
import heapq
from typing import Optional

# of rows/columns of this puzzle
N = 0
# of 'S'
S = 0
# of 'L' and 'T'
LT = 0
# of 'R' and 'B'
RB = 0
# of 'M'
M = 0

class Variable:
    """A variable represents a grid of the puzzle given.
    '0' (zero) represents no hint for that square
    'S' represents a submarine,
    'W' represents water,
    'L' represents the left end of a horizontal ship,
    'R' represents the right end of a horizontal ship,
    'T' represents the top end of a vertical ship, 
    'B' represents the bottom end of a vertical ship, and
    'M' represents a middle segment of a ship (horizontal or vertical).

    === Attributes ===
    row:
        Which row the grid represented by this variable is in.
    column:
        Which column the grid represented by this variable is in.
    domain:
        A list of strings that this variable can be.
    curDom:
        A list of strings that this variable can be in partial state.
    value:
        What this variable is.
    
    === Representation Invariants ===
    - value can only be '0', 'S', 'W', 'L', 'R', 'T', 'B', and 'M'.
    - The elements in domain and curDom can only be 'S', 'W', 'L', 
    'R', 'T', 'B', and 'M'.
    """
    row: int
    column: int
    domain: list[str]
    curDom: list[str]
    value: str
    
    def __init__(self, row: int, column: int, value: int) -> None:
        """Initialize a new Variable."""
        self.row = row
        self.column = column
        self.value = value
        if value == '0':
            self.domain = ['S', 'W', 'L', 'R', 'T', 'B', 'M']
            if self.row == 0:
                self.domain.remove('B')
            if self.row == N-1:
                self.domain.remove('T')
            if self.column == 0:
                self.domain.remove('R')
            if self.column == N-1:
                self.domain.remove('L')
            self.curDom = self.domain[:]
        else:
            self.domain = [value]
            self.curDom = [value]
    
    def __str__(self) -> str:
        """The string representation of this Variable."""
        return self.value
    
    def __eq__(self, other) -> bool:
        """Return True if the two Variables are the same."""
        if self.row == other.row and self.column == other.column \
            and self.value == other.value:
            return True
        return False

class Constraint:
    """A constraint that some variables should follow.
    About the number of grids assigned for each row/column.

    === Attributes ===
    scope:
        A set of the coordinates of variables that this constraint is over.
    r_or_c:
        Row or column this constraint is for.
        0 for row and 1 for column.
    index:
        Which row/column this constriant is for.
    value:
        The number of grids having ship in this row/column.
    
    === Representation Invariants ===
    - r_or_c == 0 or r_or_c == 1
    """
    scope: set[tuple[int]]
    r_or_c: int
    index: int
    value: int
    
    def __init__(self, N: int, r_or_c: int, index: int, value: int) -> None:
        """Initialize a new Constraint."""
        self.r_or_c = r_or_c
        self.index = index
        self.scope = set()
        if r_or_c == 0:
            for i in range(0, N):
                self.scope.add((index, i))
        else:
            for i in range(0, N):
                self.scope.add((i, index))
        self.value = value

    def __str__(self) -> str:
        """The string representation of this Constraint."""
        if self.r_or_c == 0:
            temp = "row"
        else:
            temp = "column"
        return "This is the {} {} constraint, which is {}, and its scope is {}"\
            .format(self.index, temp, self.value, self.scope)
    
    def difference(self) -> int:
        """The difference between the value and the size
        of scope of this Constraint."""
        return len(self.scope) - self.value

class priority_queue:
    """A priority queue ordered by difference between the value and the size
    of scope of a Constraint.

    Stores data ordered by the difference. When removing an item from the 
    priority queue, the item with the smallest differnece is the one that 
    is removed.

    === Private attributes ===
    heap:
        The items stored in this priority queue, which is a min-heap. Each item
        stored as a tuple, where the first element is the difference and the
        second element is a tuple reprensenting a Constriant.
    """
    lst: list

    def __init__(self) -> None:
        """Initialize a new empty priority queue."""
        self.lst = []

    def is_empty(self) -> bool:
        """Return whether this priority queue contains no items."""
        return not self.lst

    def enqueue(self, diff: int, c: tuple) -> None:
        """Add a new element to the priority queue."""
        heapq.heappush(self.lst, (diff, c))

    def dequeue(self) -> Optional[tuple]:
        """Remove and return the element the priority queue."""
        if self.is_empty():
            return None
        else:
            return heapq.heappop(self.lst)[1]

class State:
    """A state that having a set of variables and a set of constraints.

    === Attributes ===
    variables:
        A dictionary whose value is a Variable and its key is the coordinate
        of this Variable.
    constraints:
        A dictionary whose value is a Constraint and its key is a tuple whose 
        first element is r_or_c and the second element is index.
    assigned_ship:
        A dictionary whose value is the content of an assigned grid which is part
        of a ship and its key is the coordinate of this grid.
    assigned_water:
        A set of coordinates for grids which are assigned water.
    """
    variables: dict[tuple[int], Variable]
    constraints: dict[tuple[int], Constraint]
    assigned_ship: dict[tuple[int], str]
    assigned_water: set[tuple[int]]
    
    def __init__(self, variables: dict[tuple[int], Variable], \
        constraints: dict[tuple[int], Constraint], assigned_ship: \
            dict[tuple[int], str], assign_water: set[tuple[int]]) -> None:
            """Initialize a new Constraint."""
            self.variables = variables
            self.constraints = constraints
            self.assigned_ship = assigned_ship
            self.assigned_water = assign_water
    
    def __str__(self) -> str:
        """The string representation of this State."""
        s = ""
        for i in range(0, N):
            for j in range(0, N):
                s += self.variables[(i, j)].value
            s += "\n"
        return s[:-1]
    
    def update_surrounding(self, coord: tuple[int]) -> None:
        """Preprocessing. Update all squares surrounding the ship
        squares to avoid touching each other.
        """
        temp = self.assigned_ship[coord]
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (coord[0]+i, coord[1]+j) in self.variables:
                    if i == 0 and j == 0:
                        pass
                    elif i == -1 and j == 0 and (temp == 'M' or temp == 'B'):
                        pass
                    elif i == 0 and j == -1 and (temp == 'M' or temp == 'R'):
                        pass
                    elif i == 0 and j == 1 and (temp == 'M' or temp == 'L'):
                        pass
                    elif i == 1 and j == 0 and (temp == 'M' or temp == 'T'):
                        pass
                    else:
                        self.variables[(coord[0]+i, coord[1]+j)].value = 'W'
                        self.assigned_water.add((coord[0]+i, coord[1]+j))
                        self.constraints[(0, coord[0]+i)].scope.\
                            remove((coord[0]+i, coord[1]+j))
                        self.constraints[(1, coord[1]+j)].scope.\
                            remove((coord[0]+i, coord[1]+j))
        return None
    
    def update_zero_constraint(self) -> None:
        """Preprocessing. Pad certain squares with water before search even 
        begins since those columns/rows that add up to 0 are all water.
        """
        lst_remove = []
        for i in self.constraints:
            if self.constraints[i].value == 0:
                if i[0] == 0:
                    for j in range(0, N):
                        if self.variables[(i[1], j)].value == '0':
                            self.variables[(i[1], j)].value = 'W'
                            self.assigned_water.add((i[1], j))
                            self.constraints[(1, j)].scope.remove((i[1], j))
                else:
                    for j in range(0, N):
                        if self.variables[(j, i[1])].value == '0':
                            self.variables[(j, i[1])].value = 'W'
                            self.assigned_water.add((j, i[1]))
                            self.constraints[(0, j)].scope.remove((j, i[1]))
                lst_remove.append(i)
        for key in lst_remove:
            self.constraints.pop(key)
        return None

    def check_constraint(self, x: tuple[int]) -> bool:
        """Check if the constraints about the number of ships in each
        column/row have been followed.
        """
        if self.variables[x].value == 'W':
            if self.constraints[(0, x[0])].difference() == 0 or \
                self.constraints[(1, x[1])].difference() == 0:
                return False
        else:
            if self.constraints[(0, x[0])].value == 0 or \
                self.constraints[(1, x[1])].value == 0:
                return False
        return True

    def check_constraint_ship(self) -> bool:
        """Check if the constraints about the number of ships for each
        types have been followed.
        """
        s = 0
        lt = 0
        rb = 0
        m = 0
        for i in self.assigned_ship:
            if self.assigned_ship[i] == 'S':
                s += 1
            elif self.assigned_ship[i] == 'L' or self.assigned_ship[i] == 'T':
                lt += 1
            elif self.assigned_ship[i] == 'R' or self.assigned_ship[i] == 'B':
                rb += 1
            else:
                m += 1
        if s > S:
            return False
        if lt > LT:
            return False
        if rb > RB:
            return False
        if m > M:
            return False
        return True

    def check_surrounding(self, x: tuple[int]) -> bool:
        """Check if the constraints about the grids surrounding <x>
        are satisfied.
        """
        temp = self.variables[x].value
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x[0]+i, x[1]+j) in self.variables:
                    neighbor = self.variables[(x[0]+i, x[1]+j)].value
                    if i == 0 and j == 0:
                        pass
                    elif neighbor == '0':
                        pass
                    elif neighbor == 'S':
                        return False
                    elif (i == 0 or j == 0) and temp == 'M':
                        if neighbor != 'M' and neighbor != 'W':
                            if i == -1 and neighbor != 'T':
                                return False
                            elif i == 1 and neighbor != 'B':
                                return False
                            elif j == -1 and neighbor != 'L':
                                return False
                            elif j == 1 and neighbor != 'R':
                                return False
                        else:
                            pass
                    elif i == -1 and j == 0 and temp == 'B':
                        if neighbor != 'T' and neighbor != 'M':
                            return False
                    elif i == 0 and j == -1 and temp == 'R':
                        if neighbor != 'L' and neighbor != 'M':
                            return False
                    elif i == 0 and j == 1 and temp == 'L':
                        if neighbor != 'R' and neighbor != 'M':
                            return False
                    elif i == 1 and j == 0 and temp == 'T':
                        if neighbor != 'B' and neighbor != 'M':
                            return False
                    elif neighbor != 'W':
                        return False
        return True

    def check_surrounding_water(self, x: tuple[int]) -> bool:
        temp = self.variables[x].value
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x[0]+i, x[1]+j) in self.variables:
                    neighbor = self.variables[(x[0]+i, x[1]+j)].value
                    if i == 0 or j == 0:
                        if i == -1:
                            if neighbor == 'T':
                                return False
                        elif i == 1:
                            if neighbor == 'B':
                                return False
                        elif j == -1:
                            if neighbor == 'L':
                                return False
                        elif j == 1:
                            if neighbor == 'R':
                                return False
        return True

    def check_constraint_ship2(self) -> bool:
        """Check if the constraints about the number of ships for each types 
        have been followed, which should be equal to the ones in solution.
        """
        s = 0
        lt = 0
        rb = 0
        m = 0
        for i in self.assigned_ship:
            if self.assigned_ship[i] == 'S':
                s += 1
            elif self.assigned_ship[i] == 'L' or self.assigned_ship[i] == 'T':
                lt += 1
            elif self.assigned_ship[i] == 'R' or self.assigned_ship[i] == 'B':
                rb += 1
            else:
                m += 1
        if s != S:
            return False
        if lt != LT:
            return False
        if rb != RB:
            return False
        if m != M:
            return False
        return True

    def check_M(self) -> bool:
        if M == 0:
            return True
        else:
            for i in self.variables:
                if self.variables[i].value == 'M':
                    if (i[0] > 0 and \
                        self.variables[(i[0]-1, i[1])].value == 'W') \
                            or (i[0] < N-1 and \
                                self.variables[(i[0]+1, i[1])].value == 'W'):
                                if (i[0], i[1]-1) not in self.assigned_ship or\
                                    (i[0], i[1]+1) not in self.assigned_ship:
                                    return False
                    if (i[1] > 0 and \
                        self.variables[(i[0], i[1]-1)].value == 'W') \
                            or (i[1] < N-1 and \
                                self.variables[(i[0], i[1]+1)].value == 'W'):
                                if (i[0]-1, i[1]) not in self.assigned_ship or\
                                    (i[0]-1, i[1]) not in self.assigned_ship:
                                    return False
        return True

    def PickUnassignedVariable(self) -> tuple[tuple[int], tuple[int]]:
        mrv = priority_queue()
        for i in self.constraints:
            mrv.enqueue(self.constraints[i].difference(), i)
        c = self.constraints[mrv.dequeue()]
        while len(c.scope) == 0:
            c = self.constraints[mrv.dequeue()]
        v = c.scope.pop()
        c.scope.add(v)
        return ((c.r_or_c, c.index), v)

    def FCCheck(self, x: tuple[int]) -> bool:
        lst = []
        for d in self.variables[x].curDom:
            self.variables[x].value = d
            if d == 'W':
                self.assigned_water.add(x)
                if self.check_constraint(x) is False or \
                    self.check_surrounding_water(x) is False:
                    lst.append(d)
                self.assigned_water.remove(x)
            else:
                self.assigned_ship[x] = d
                if self.check_constraint(x) is False or\
                    self.check_constraint_ship() is False or \
                        self.check_surrounding(x) is False:
                        lst.append(d) 
        self.variables[x].value = '0'
        if x in self.assigned_ship:
            self.assigned_ship.pop(x)
        if len(lst) == len(self.variables[x].curDom):
            return False
        else:
            for i in lst:
                self.variables[x].curDom.remove(i)
        return True

    def FC(self, level: int) -> bool:
        if len(self.assigned_ship) + len(self.assigned_water) == N * N:
            if self.check_constraint_ship2() and self.check_M() is True:
                return True
            else:
                return False
        c, x = self.PickUnassignedVariable()
        if self.FCCheck(x) is True:
            for d in self.variables[x].curDom:
                self.variables[x].value = d
                if c[0] == 0:
                    new = (1, x[1])
                else:
                    new = (0, x[0])
                if d == 'W':
                    self.assigned_water.add(x)
                else:
                    self.assigned_ship[x] = d
                    self.constraints[c].value -= 1
                    self.constraints[new].value -= 1
                self.constraints[c].scope.remove(x)
                self.constraints[new].scope.remove(x)

                if self.FC(level+1) is False:
                    self.variables[x].value = '0'
                    if d == 'W':
                        self.assigned_water.remove(x)
                    else:
                        self.assigned_ship.pop(x)
                        self.constraints[c].value += 1
                        self.constraints[new].value += 1
                    self.constraints[c].scope.add(x)
                    self.constraints[new].scope.add(x)
                else:
                    return True
        self.variables[x].curDom = self.variables[x].domain[:]
        return False

def start(file: str) -> State:
    """Return the start state base on the puzzle given by <file>.
    """
    f = open(file, 'r')
    dict_var = {}
    assigned_ship = {}
    assigned_water = set()
    dict_con = {}
    curr = f.readline().strip("\n")
    global N
    N = len(curr)
    for i in range(0, N):
        dict_con[0, i] = Constraint(N, 0, i, int(curr[i]))
    curr = f.readline().strip("\n")
    for i in range(0, N):
        dict_con[1, i] = Constraint(N, 1, i, int(curr[i]))
    curr = f.readline().strip("\n")
    while len(curr) < 4:
        curr = curr + '0'
    SUB, DES, CRU, BAT = int(curr[0]), int(curr[1]), int(curr[2]), int(curr[3])
    global S, LT, RB, M
    S, LT, RB, M = SUB, DES + CRU + BAT, DES + CRU + BAT, CRU + 2 * BAT
    for i in range(0, N):
        curr = f.readline().strip("\n")
        for j in range(0, N):
            v = Variable(i, j, curr[j])
            dict_var[(i, j)] = v
            if curr[j] != '0':
                dict_con[(0, i)].scope.remove((i, j))
                dict_con[(1, j)].scope.remove((i, j))
                if curr[j] == 'W':
                    assigned_water.add((i, j))
                else:
                    assigned_ship[(i, j)] = curr[j]
                    dict_con[(0, i)].value -= 1
                    dict_con[(1, j)].value -= 1
    f.close()
    result = State(dict_var, dict_con, assigned_ship, assigned_water)
    for item in assigned_ship:
        result.update_surrounding(item)
    result.update_zero_constraint()
    return result

def solution(file: str, result: State) -> None:
    """Write the <result> to <file>.
    """
    f = open(file, 'w')
    f.write(str(result))
    f.close()
    return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 battle.py <input file> <output file>")
        sys.exit()
    s = start(sys.argv[1])
    s.FC(1)
    solution(sys.argv[2], s)
