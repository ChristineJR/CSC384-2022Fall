from json.encoder import INFINITY
import sys
from typing import List, Tuple
DEPTH = 10
explored = {}

class Position:
    """A Node that stores the player whose turn it is, and the 
    state representing the position of chess board. 
    'r' denotes a red piece, 'b' denotes a black piece,
    'R' denotes a red king, 'B' denotes a black king, and
    '.' (the period character) denotes an empty square.

    === Attributes ===
    player:
        The string representing the player whose turn it is in this position. 
    state:
        The list storing eight lists to represent the position of chess board.

    === Representation Invariants ===
    - player can only be either 'red' or 'black'.
    - len(state) == 8
    - for 0 <= i <= 7, len(state[i]) == 8; and for 0 <= j <= 7, state[i][j] can
    only be 'r', 'R', 'b', 'B', or '.'.
    """
    player: str
    state: List[list[str]]
    
    def __init__(self, player: str, state: List[list[str]]) -> None:
        """Initialize a new Node."""
        self.player = player
        self.state = state
    
    def __str__(self) -> str:
        """The string representation of this position."""
        result = ""
        for i in self.state:
            s = "".join(i)
            s += "\n"
            result += s
        return result[:-1]
    
    # Consider that whether self.player == other.player is needed or not
    def __eq__(self, other) -> bool:
        """Return True if the two positions are the same."""
        if other is None:
            return False
        if self.state == other.state:
            return True
        return False

def start(file: str) -> Position:
    """Read in an initial configuration of the chess board from <file>.
    Return the Position storing the start state.
    """
    f = open(file, 'r')
    state = []
    i = 0
    for line in f:
        lst = []
        for x in line:
            lst.append(x.strip('\n'))
        state.append(lst)
        i += 1
    f.close()
    return Position("red", state)

def red_black_points(p: Position):
    """Return the points for red player and black players respectively,
    with each regular piece worth 1 point and each king worth 2.
    """
    red = 0
    black = 0
    for i in p.state:
        red += i.count('r')
        red += i.count('R') * 2
        black += i.count('b')
        black += i.count('B') * 2
    return red, black

def utility(p: Position) -> int:
    """Return the utility of a game board state for red player, i.e., the
    number of red pieces minus the number of black pieces.
    """
    red, black = red_black_points(p)
    return red - black

def copy_state(given: Position) -> list:
    """Return a copy of the state stored in <given>.
    """
    new_state = []
    for i in given.state:
        new_state.append(i[:])
    return new_state

def red_capture(p: Position, i: int, j: int) -> \
    List[Tuple[Position, int, int]]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the red piece which is originally at <p>.state[<i>][<j>]
    after this piece captures other pieces if avaliable.
    """
    result = []
    temp = []
    if (i in range(2, 8) and j in range(2, 8)) and \
        (p.state[i-1][j-1] == 'b' or p.state[i-1][j-1] == 'B') and \
            p.state[i-2][j-2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j-1] = '.'
            if i == 2:
                new_state[i-2][j-2] = 'R'
            else:
                new_state[i-2][j-2] = 'r'
            temp.append((Position("red", new_state), i-2, j-2))
    if (i in range(2, 8) and j in range(0, 6)) and \
        (p.state[i-1][j+1] == 'b' or p.state[i-1][j+1] == 'B') and \
            p.state[i-2][j+2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j+1] = '.'
            if i == 2:
                new_state[i-2][j+2] = 'R'
            else:
                new_state[i-2][j+2] = 'r'
            temp.append((Position("red", new_state), i-2, j+2))
    for item in temp:
        lst = red_capture(item[0], item[1], item[2])
        if len(lst) == 0:
            result.append(item)
        else:
            temp += lst
    return result

def black_capture(p: Position, i: int, j: int) -> \
    List[Tuple[Position, int, int]]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the black piece which is originally at <p>.state[<i>][<j>]
    after this piece captures other pieces if avaliable.
    """
    result = []
    temp = []
    if (i in range(0, 6) and j in range(2, 8)) and \
        (p.state[i+1][j-1] == 'r' or p.state[i+1][j-1] == 'R') and \
            p.state[i+2][j-2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j-1] = '.'
            if i == 5:
                new_state[i+2][j-2] = 'B'
            else:
                new_state[i+2][j-2] = 'b'
            temp.append((Position("black", new_state), i+2, j-2))
    if (i in range(0, 6) and j in range(0, 6)) and \
        (p.state[i+1][j+1] == 'r' or p.state[i+1][j+1] == 'R') and \
            p.state[i+2][j+2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j+1] = '.'
            if i == 5:
                new_state[i+2][j+2] = 'B'
            else:
                new_state[i+2][j+2] = 'b'
            temp.append((Position("black", new_state), i+2, j+2))
    for item in temp:
        lst = black_capture(item[0], item[1], item[2])
        if len(lst) == 0:
            result.append(item)
        else:
            temp += lst
    return result

def king_capture(p: Position, i: int, j: int) -> \
    List[Tuple[Position, int, int]]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the king piece which is originally at <p>.state[<i>][<j>]
    after this piece captures other pieces if avaliable.
    """
    if p.player == "red":
        king = 'R'
        opp = 'b'
        opp_king = 'B'
    else:
        king = 'B'
        opp = 'r'
        opp_king = 'R'
    result = []
    temp = []
    if (i in range(2, 8) and j in range(2, 8)) and \
        (p.state[i-1][j-1] == opp or p.state[i-1][j-1] == opp_king) and \
            p.state[i-2][j-2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j-1] = '.'
            new_state[i-2][j-2] = king
            temp.append((Position(p.player, new_state), i-2, j-2))
    if (i in range(2, 8) and j in range(0, 6)) and \
        (p.state[i-1][j+1] == opp or p.state[i-1][j+1] == opp_king) and \
            p.state[i-2][j+2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j+1] = '.'
            new_state[i-2][j+2] = king
            temp.append((Position(p.player, new_state), i-2, j+2))
    if (i in range(0, 6) and j in range(2, 8)) and \
        (p.state[i+1][j-1] == opp or p.state[i+1][j-1] == opp_king) and \
            p.state[i+2][j-2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j-1] = '.'
            new_state[i+2][j-2] = king
            temp.append((Position(p.player, new_state), i+2, j-2))
    if (i in range(0, 6) and j in range(0, 6)) and \
        (p.state[i+1][j+1] == opp or p.state[i+1][j+1] == opp_king) and \
            p.state[i+2][j+2] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j+1] = '.'
            new_state[i+2][j+2] = king
            temp.append((Position(p.player, new_state), i+2, j+2))
    for item in temp:
        lst = king_capture(item[0], item[1], item[2])
        if len(lst) == 0:
            result.append(item)
        else:
            temp += lst
    return result

def red_move(p: Position, i: int, j: int) -> List[Position]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the red piece which is originally at <p>.state[<i>][<j>]
    after this piece move to an empty space if avaliable.
    """
    lst = []
    if (i in range(1, 8) and j in range(1, 8)) and \
        p.state[i-1][j-1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            if i == 1:
                new_state[i-1][j-1] = 'R'
            else:
                new_state[i-1][j-1] = 'r'
            lst.append(Position("black", new_state))
    if (i in range(1, 8) and j in range(0, 7)) and \
        p.state[i-1][j+1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            if i == 1:
                new_state[i-1][j+1] = 'R'
            else:
                new_state[i-1][j+1] = 'r'
            lst.append(Position("black", new_state))
    return lst

def black_move(p: Position, i: int, j: int) -> List[Position]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the black piece which is originally at <p>.state[<i>][<j>]
    after this piece move to an empty space if avaliable.
    """
    lst = []
    if (i in range(0, 7) and j in range(1, 8)) and \
        p.state[i+1][j-1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            if i == 6:
                new_state[i+1][j-1] = 'B'
            else:
                new_state[i+1][j-1] = 'b'
            lst.append(Position("red", new_state))
    if (i in range(0, 7) and j in range(0, 7)) and \
        p.state[i+1][j+1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            if i == 6:
                new_state[i+1][j+1] = 'B'
            else:
                new_state[i+1][j+1] = 'b'
            lst.append(Position("red", new_state))
    return lst

def king_move(p: Position, i: int, j: int) -> List[Position]:
    """
    Return a list of Tuple consisting of possible new Position, and the
    coordinates of the king piece which is originally at <p>.state[<i>][<j>]
    after this piece move to an empty space if avaliable.
    """
    if p.player == "red":
        opp = "black"
        king = 'R'
    else:
        opp = "red"
        king = 'B'
    lst = []
    if (i in range(1, 8) and j in range(1, 8)) and \
        p.state[i-1][j-1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j-1] = king
            lst.append(Position(opp, new_state))
    if (i in range(1, 8) and j in range(0, 7)) and \
        p.state[i-1][j+1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i-1][j+1] = king
            lst.append(Position(opp, new_state))
    if (i in range(0, 7) and j in range(1, 8)) and \
        p.state[i+1][j-1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j-1] = king
            lst.append(Position(opp, new_state))
    if (i in range(0, 7) and j in range(0, 7)) and \
        p.state[i+1][j+1] == '.':
            new_state = copy_state(p)
            new_state[i][j] = '.'
            new_state[i+1][j+1] = king
            lst.append(Position(opp, new_state))
    return lst

def successors(p: Position) -> List[Position]:
    """Return a list of results after all legal moves for 
    <p>.player in position <p>.state.
    """
    lst = []
    if p.player == "red":
        for i in range(0, 8):
            for j in range(0, 8):
                temp = []
                if p.state[i][j] == 'r':
                    temp = red_capture(p, i, j)
                elif p.state[i][j] == 'R':
                    temp = king_capture(p, i, j)
                for item in temp:
                    new = item[0]
                    new.player = "black"
                    lst.append(new)
        if len(lst) == 0:
            for i in range(0, 8):
                for j in range(0, 8):
                    temp = []
                    if p.state[i][j] == 'r':
                        temp = red_move(p, i, j)
                    elif p.state[i][j] == 'R':
                        temp = king_move(p, i, j)
                    for item in temp:
                        lst.append(item)
    else:
        for i in range(0, 8):
            for j in range(0, 8):
                temp = []
                if p.state[i][j] == 'b':
                    temp = black_capture(p, i, j)
                elif p.state[i][j] == 'B':
                    temp = king_capture(p, i, j)
                for item in temp:
                    new = item[0]
                    new.player = "red"
                    lst.append(new)
        if len(lst) == 0:
            for i in range(0, 8):
                for j in range(0, 8):
                    temp = []
                    if p.state[i][j] == 'b':
                        temp = black_move(p, i, j)
                    elif p.state[i][j] == 'B':
                        temp = king_move(p, i, j)
                    for item in temp:
                        lst.append(item)
    return lst

def terminal(p: Position) -> bool:
    """Return True is the game is over in position <p>.state.
    """
    red, black = red_black_points(p)
    if red == 0 or black == 0:
        return True
    if len(successors(p)) == 0:
        return True
    return False

def alpha_beta(p: Position, alpha: int, beta: int, depth: int):
    """Return the best move for <p>.player and red player's value for <p>.
    """
    depth -= 1
    best_move = None
    if terminal(p) or depth == 0:
        if best_move is None:
            best_move = p
        return best_move, utility(p)
    if p.player == "red":
        value = -INFINITY
    else:
        value = INFINITY
    for i in successors(p):
        if str(i.state) in explored:
            nxt_val = explored[str(i.state)]
        else:
            nxt_val = alpha_beta(i, alpha, beta, depth)[1]
            explored[str(i.state)] = nxt_val
        if p.player == "red":
            if value < nxt_val:
                value, best_move = nxt_val, i
            if value >= beta:
                if best_move is None:
                    best_move = p
                return best_move, value
            alpha = max(alpha, value)
        else:
            if value > nxt_val:
                value, best_move = nxt_val, i
            if value <= alpha:
                if best_move is None:
                    best_move = p
                return best_move, value
            beta = min(beta, value)
    if best_move is None:
        best_move = p
    return best_move, value

def solution(file: str, p: Position) -> None:
    """Write the solution into <file> with <given>, which 
    is the Position representing the best move.
    """
    f = open(file, 'w')
    f.write(str(p))
    f.close()
    return None

def heuristic(p: Position) -> int:
    """Return an advanced heuristic estimate for <p>.state.
    """
    red = 0
    black = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if p.state[i][j] == 'r' or p.state[i][j] == 'R':
                if p.state[i][j] == 'r':
                    red += 1
                else:
                    red += 3
                if j == 0 and i != 7 and (p.state[i+1][1] == 'r' or \
                    p.state[i+1][1] == 'R'):
                    red += 1
                elif j == 7 and i != 7 and (p.state[i+1][6] == 'r' or \
                    p.state[i+1][6] == 'R'):
                    red += 1
                elif i != 7 and j in range(1, 7) and \
                    (p.state[i+1][j+1] == 'r' or p.state[i+1][j+1] == 'R') \
                        and (p.state[i+1][j-1] == 'r' or p.state[i+1][j-1] == 'R'):
                        red += 1
            elif p.state[i][j] == 'b' or p.state[i][j] == 'B':
                if p.state[i][j] == 'b':
                    black += 1
                else:
                    black += 3
                if j == 0 and i != 0 and (p.state[i-1][1] == 'b' or \
                    p.state[i-1][1] == 'B'):
                    black += 1
                elif j == 7 and i != 0 and (p.state[i-1][6] == 'b' or \
                    p.state[i-1][6] == 'B'):
                    black += 1
                elif i != 0 and j in range(1, 7) and \
                    (p.state[i-1][j+1] == 'b' or p.state[i-1][j+1] == 'B') \
                        and (p.state[i-1][j-1] == 'b' or p.state[i-1][j-1] == 'B'):
                        black += 1
    return red - black

def sort_successors(lst: List[Position]) -> List[Position]:
    """
    Return a sorted list for successors.
    """
    if len(lst) == 0:
        return lst
    if lst[0].player == "red":
        return sorted(lst, key=lambda Position: heuristic(Position))
    else:
        return sorted(lst, key=lambda Position: heuristic(Position))[::-1]

def advanced_alpha_beta(p: Position, alpha: int, beta: int, depth: int):
    """Return the best move for <p>.player and red player's value for <p>.
    Using heuristic function instead of the utility function given.
    """
    depth -= 1
    best_move = None
    if terminal(p) or depth == 0:
        if best_move is None:
            best_move = p
        return best_move, heuristic(p)
    if p.player == "red":
        value = -INFINITY
    else:
        value = INFINITY
    for i in sort_successors(successors(p)):
        if str(i.state) in explored:
            nxt_val = explored[str(i.state)]
        else:
            nxt_val = advanced_alpha_beta(i, alpha, beta, depth)[1]
            explored[str(i.state)] = nxt_val
        if p.player == "red":
            if value < nxt_val:
                value, best_move = nxt_val, i
            if value >= beta:
                if best_move is None:
                    best_move = p
                return best_move, value
            alpha = max(alpha, value)
        else:
            if value > nxt_val:
                value, best_move = nxt_val, i
            if value <= alpha:
                if best_move is None:
                    best_move = p
                return best_move, value
            beta = min(beta, value)
    if best_move is None:
        best_move = p
    return best_move, value

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 checkers.py <input file> <output file>")
        sys.exit()
    # solution(sys.argv[2], alpha_beta(start(sys.argv[1]), -INFINITY, INFINITY, DEPTH)[0])
    solution(sys.argv[2], advanced_alpha_beta(start(sys.argv[1]), -INFINITY, INFINITY, DEPTH)[0])
