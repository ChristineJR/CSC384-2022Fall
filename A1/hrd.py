import sys
import heapq
from typing import Any, List, Optional

# Implement a data structure to store a state. 
class Node:
    """A node that stores the state representing the position of
    ten pieces on the Hua Rong Dao puzzle board. 
    The empty squares are denoted by 0. The single pieces are denoted by 7.
    The 2x2 piece is denoted by 1. The 5 1x2 pieces are denoted by one of 
    {2, 3, 4, 5, 6}, but the numbers are assigned at random.

    === Attributes ===
    parent:
        The parent node of this node.
    state:
        The list storing five lists to represent the position of 
        ten pieces on the Hua Rong Dao puzzle board.
    id:
        A 20-digit int which is consist of all number in the state
        from left to right, from top to bottom.
    cost:
        An int representing the cost from the start state to the state
        stored in this Node.

    === Representation Invariants ===
    - len(state) == 5
    - for 0 <= i <= 4, len(state[i]) == 4; and for 0 <= j <= 3, 
    0 <= int(state[i][j]) <= 7
    """
    parent: Optional[Any]
    state: List[list[str]]
    id: int
    cost: int
    
    def __init__(self, state: List[list[str]]) -> None:
        """Initialize a new Node."""
        self.parent = None
        self.state = state
        result = ""
        for i in self.state:
            s = "".join(i)
            result += s
        self.id = int(result)
        self.cost = 0
    
    def __str__(self) -> str:
        """The string representation of this node."""
        result = ""
        for i in self.state:
            s = "".join(i)
            s += "\n"
            result += s
        return result
    
    def __eq__(self, other) -> bool:
        """Return True if the two nodes storing the same state."""
        if other is None:
            return False
        if self.id == other.id:
            return True
        return False

# Implement a LIFO stack to store the frontier.
class Stack:
    """A last-in-first-out (LIFO) stack of items.

    Stores data in a last-in, first-out order. When removing an item from 
    the stack, the most recently-added item is the one that is removed.

    === Private attributes ===
    lst:
        The items stored in this stack. The end of the list represents
        the top of the stack.
    """
    lst: List

    def __init__(self) -> None:
        """Initialize a new empty stack."""
        self.lst = []

    def is_empty(self) -> bool:
        """Return whether this stack contains no items."""
        return not self.lst

    def push(self, item: Any) -> None:
        """Add a new element to the top of this stack."""
        self.lst.append(item)

    def pop(self) -> Optional[Any]:
        """Remove and return the element at the top of this stack."""
        if self.is_empty():
            return None
        else:
            return self.lst.pop()

# Implement a function which tests whether a state is a goal state.
def test_goal(given: Node) -> bool:
    """Return True is the state stored in <given> is a goal state. 
    Otherwise, return False.
    """
    if given.state[4][1] != '1' or given.state[4][2] != '1':
        return False
    return True

# A helper function for successors().
def is_vertical(given: Node, x: int, y: int) -> bool:
    """Return True if the piece at <given>[<x>][<y>] is vertical 1x2 piece. 
    Otherwise, return False.
    """
    if given.state[x][y] == '0' or given.state[x][y] == '1':
        return False
    if x != 0 and given.state[x][y] == given.state[x-1][y]:
        return True
    if x != 4 and given.state[x][y] == given.state[x+1][y]:
        return True
    return False

# A helper function for successors().
def is_horizontal(given: Node, x: int, y: int) -> bool:
    """Return True if the piece at <given>[<x>][<y>] is horizontal 1x2 piece. 
    Otherwise, return False.
    """
    if given.state[x][y] == '0' or given.state[x][y] == '1':
        return False
    if y != 0 and given.state[x][y] == given.state[x][y-1]:
        return True
    if y != 3 and given.state[x][y] == given.state[x][y+1]:
        return True
    return False

# A helper function for successors().
def copy_state(given: Node) -> list:
    """Return a copy of the state stored in <given>.
    """
    new_state = []
    for i in given.state:
        new_state.append(i[:])
    return new_state

# A helper function for successors().
def move_single_empty(zero: tuple, given: Node, result: list) -> list:
    """Add a list of successor states of <given> when the empty piece at
    <zero> is moved to <result>, and then return this list.
    """
    # Move upward.
    if zero[0] != 0:
        if given.state[zero[0]-1][zero[1]] == '7' or \
            is_vertical(given, zero[0]-1, zero[1]):
                new_state = copy_state(given)
                if given.state[zero[0]-1][zero[1]] == '7':
                    new_state[zero[0]][zero[1]] = '7'
                    new_state[zero[0]-1][zero[1]] = '0'
                else:
                    new_state[zero[0]][zero[1]] = new_state[zero[0]-1][zero[1]]
                    new_state[zero[0]-2][zero[1]] = '0'
                new = Node(new_state)
                new.parent = given
                new.cost = given.cost + 1
                result.append(new)
    # Move left.
    if zero[1] != 0:
        if given.state[zero[0]][zero[1]-1] == '7' or\
            is_horizontal(given, zero[0], zero[1]-1):
                new_state = copy_state(given)
                if given.state[zero[0]][zero[1]-1] == '7':
                    new_state[zero[0]][zero[1]] = '7'
                    new_state[zero[0]][zero[1]-1] = '0'
                else:
                    new_state[zero[0]][zero[1]] = new_state[zero[0]][zero[1]-1]
                    new_state[zero[0]][zero[1]-2] = '0'
                new = Node(new_state)
                new.parent = given
                new.cost = given.cost + 1
                result.append(new)
    # Move downward.
    if zero[0] != 4:
        if given.state[zero[0]+1][zero[1]] == '7' or\
            is_vertical(given, zero[0]+1, zero[1]):
                new_state = copy_state(given)
                if given.state[zero[0]+1][zero[1]] == '7':
                    new_state[zero[0]][zero[1]] = '7'
                    new_state[zero[0]+1][zero[1]] = '0'
                else:
                    new_state[zero[0]][zero[1]] = new_state[zero[0]+1][zero[1]]
                    new_state[zero[0]+2][zero[1]] = '0'
                new = Node(new_state)
                new.parent = given
                new.cost = given.cost + 1
                result.append(new)
    # Move right.
    if zero[1] != 3:
        if given.state[zero[0]][zero[1]+1] == '7' or\
            is_horizontal(given, zero[0], zero[1]+1):
                new_state = copy_state(given)
                if given.state[zero[0]][zero[1]+1] == '7':
                    new_state[zero[0]][zero[1]] = '7'
                    new_state[zero[0]][zero[1]+1] = '0'
                else:
                    new_state[zero[0]][zero[1]] = new_state[zero[0]][zero[1]+1]
                    new_state[zero[0]][zero[1]+2] = '0'
                new = Node(new_state)
                new.parent = given
                new.cost = given.cost + 1
                result.append(new)
    return result

# Implement a function which takes a state and returns a list of 
# its successor states. 
def successors(given: Node) -> List[Node]:
    """Return a list of successor states of <given>."""
    result = []
    general = []
    for i in given.state:
        general += i
    num = general.index('0')
    num2 = num + 1 + general[num+1:].index('0')
    zero1 = (num//4, num%4)
    zero2 = (num2//4, num2%4)
    # Two empty pieces are moved together.
    # These two empty pieces form a horizontal 1x2 piece.
    if zero1[0] == zero2[0] and zero1[1] + 1 == zero2[1]:
        # Move upward.
        if zero1[0] != 0 and given.state[zero1[0]-1][zero1[1]] != '7' and \
            given.state[zero1[0]-1][zero1[1]] == \
                given.state[zero2[0]-1][zero2[1]]:
                    new_state = copy_state(given)
                    char = given.state[zero1[0]-1][zero1[1]]
                    if char == '1':
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]-2][zero1[1]] = '0'
                        new_state[zero2[0]-2][zero2[1]] = '0'
                    else:
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]-1][zero1[1]] = '0'
                        new_state[zero2[0]-1][zero2[1]] = '0'
                    new = Node(new_state)
                    new.parent = given
                    new.cost = given.cost + 1
                    result.append(new)
        # Move downward.
        if zero1[0] != 4 and given.state[zero1[0]+1][zero1[1]] != '7' and \
            given.state[zero1[0]+1][zero1[1]] == \
                given.state[zero2[0]+1][zero2[1]]:
                    new_state = copy_state(given)
                    char = given.state[zero1[0]+1][zero1[1]]
                    if char == '1':
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]+2][zero1[1]] = '0'
                        new_state[zero2[0]+2][zero2[1]] = '0'
                    else:
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]+1][zero1[1]] = '0'
                        new_state[zero2[0]+1][zero2[1]] = '0'
                    new = Node(new_state)
                    new.parent = given
                    new.cost = given.cost + 1
                    result.append(new)
    # These two empty pieces form a vertical 1x2 piece.
    if zero1[0] + 1 == zero2[0] and zero1[1] == zero2[1]:
        # Move left.
        if zero1[1] != 0 and given.state[zero1[0]][zero1[1]-1] != '7' and \
            given.state[zero1[0]][zero1[1]-1] == \
                given.state[zero2[0]][zero2[1]-1]:
                    new_state = copy_state(given)
                    char = given.state[zero1[0]][zero1[1]-1]
                    if char == '1':
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]][zero1[1]-2] = '0'
                        new_state[zero2[0]][zero2[1]-2] = '0'
                    else:
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]][zero1[1]-1] = '0'
                        new_state[zero2[0]][zero2[1]-1] = '0'
                    new = Node(new_state)
                    new.parent = given
                    new.cost = given.cost + 1
                    result.append(new)
        # Move right.
        if zero1[1] != 3 and given.state[zero1[0]][zero1[1]+1] != '7' and \
            given.state[zero1[0]][zero1[1]+1] == \
                given.state[zero2[0]][zero2[1]+1]:
                    new_state = copy_state(given)
                    char = given.state[zero1[0]][zero1[1]+1]
                    if char == '1':
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]][zero1[1]+2] = '0'
                        new_state[zero2[0]][zero2[1]+2] = '0'
                    else:
                        new_state[zero1[0]][zero1[1]] = char
                        new_state[zero2[0]][zero2[1]] = char
                        new_state[zero1[0]][zero1[1]+1] = '0'
                        new_state[zero2[0]][zero2[1]+1] = '0'
                    new = Node(new_state)
                    new.parent = given
                    new.cost = given.cost + 1
                    result.append(new)
    # Only one empty piece is moved.
    result = move_single_empty(zero1, given, result)
    result = move_single_empty(zero2, given, result)
    
    return result

# Implement a function to read in an initial configuration of 
# the puzzle from an input file and store it as a state.
def start_state(file: str) -> Node:
    """Read in an initial configuration of the puzzle from <file>.
    Return the Node storing the start state.
    """
    f = open(file)
    state = []
    i = 0
    for line in f:
        lst = []
        for x in line[:-1]:
            lst.append(x)
        state.append(lst)
        i += 1
    f.close()
    return Node(state)

# Implement a function that takes a solution and 
# returns the cost of the solution.
def cost(given: Node) -> int:
    """Return the cost from the start state to the state <given>.
    """
    return given.cost

# Implement a function that performs DFS given an initial state 
# and returns a solution.
def DFS(given: Node) -> Node:
    """Return a Node stored a goal state with a reference of 
    its parent node after DFS."""
    frontier = Stack()
    frontier.push(given)
    explored = set()
    while not frontier.is_empty():
        curr = frontier.pop()
        if curr.id not in explored:
            explored.add(curr.id)
            if test_goal(curr):
                return curr
            for i in successors(curr):
                frontier.push(i)
    return None

# Implement a function which takes a state and returns the heuristic 
# estimate for the state (i.e. the cost of the optimal path from the 
# state to a goal state based on your heuristic function). That is, 
# this function returns the h value of the state.
def Manhattan_h(given: Node) -> int:
    """Return the Manhattan distance heuristic estimate for the state <given>.
    """
    general = []
    for i in given.state:
        general += i
    num = 20 - general[::-1].index('0') - 1
    lower_right = (num//4, num%4)
    h = abs(4 - lower_right[0]) + abs(2 - lower_right[1])
    return h

def advanced_h(given: Node) -> int:
    """Return an advanced heuristic estimate for the state <given>.
    The advanced heuristic function here is admissible but dominates 
    the Manhattan distance heuristic.
    """
    general = []
    for i in given.state:
        general += i
    num = 20 - general[::-1].index('0') - 1
    lower_right = (num//4, num%4)
    h = abs(4 - lower_right[0]) + abs(2 - lower_right[1])
    if lower_right[0] == 1:
        h += 2
    if lower_right[0] == 2:
        h += 1
    return h

# Implement a priority queue to store the frontier.
class priority_queue:
    """A priority queue ordered by f(n) = g(n) + h(n).

    Stores data ordered by f(n). When removing an item from the 
    priority queue, the item with the smallest f(n) is the one that is removed.
    When two or more items have the same f(n), the oldest one will be removed.
    
    h(n) is the Manhattan distance heuristic function.

    === Private attributes ===
    heap:
        The items stored in this priority queue, which is a min-heap. Each item
        stored as a tuple, where the third element is a Node storing a state
        and the first element is the f value - the sum of the cost and the
        heuristic estimate - for this state. In addition, the second element
        is the order that this node is added into the priority queue.
    """
    lst: List

    def __init__(self) -> None:
        """Initialize a new empty priority queue."""
        self.lst = []

    def is_empty(self) -> bool:
        """Return whether this priority queue contains no items."""
        return not self.lst

    def enqueue(self, item: Node, order: int) -> None:
        """Add a new element to the priority queue."""
        heapq.heappush(self.lst, (cost(item)+Manhattan_h(item), order, item))

    def dequeue(self) -> Optional[Node]:
        """Remove and return the element the priority queue."""
        if self.is_empty():
            return None
        else:
            return heapq.heappop(self.lst)[2]

# Implement a function that performs A* search given an initial state 
# and returns a solution. This solution should be the optimal solution 
# if your heuristic is admissible.
def A_star(given: Node) -> Node:
    """Return a Node stored a goal state with a reference of 
    its parent node after A* search."""
    order = 0
    frontier = priority_queue()
    frontier.enqueue(given, order)
    explored = set()
    while not frontier.is_empty():
        curr = frontier.dequeue()
        if curr.id not in explored:
            explored.add(curr.id)
            if test_goal(curr):
                return curr
            for i in successors(curr):
                order += 1
                frontier.enqueue(i, order)
    return None

# A helper function for solution().
def output(s: str) -> str:
    """Return the representation of a state in a solution. 
    The empty squares are denoted by 0. The single pieces are denoted by 4.
    The 2x2 piece is denoted by 1. The horizontal 1x2 pieces are denoted by 2.
    The vertical 1x2 pieces are denoted by 3.
    """
    horizontal = ['22', '33', '44', '55', '66']
    vertical = ['2', '3', '4', '5', '6']
    for i in horizontal:
        s = s.replace(i, '88')
    for j in vertical:
        s = s.replace(j, '3')
    s = s.replace('8', '2')
    s = s.replace('7', '4')
    return s

def solution(file: str, given: Node) -> None:
    """Write the solution into <file> with <given>, which 
    is the Node storing a goal state and a reference to its
    parent node.
    """
    result = Stack()
    curr = given
    while curr is not None:
        result.push(curr)
        curr = curr.parent
    f = open(file, 'w')
    f.write("Cost of the solution: " + str(cost(given)) +"\n")
    while not result.is_empty():
        f.write(output(str(result.pop())))
        f.write("\n")
    f.close()
    return None

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 hrd.py  <input file> "
              "<DFS output file>  <A* output file> ")
        sys.exit()

    start = start_state(sys.argv[1])
    solution(sys.argv[2], DFS(start))
    solution(sys.argv[3], A_star(start))
    