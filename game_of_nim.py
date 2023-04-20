#! /usr/bin/env python3

from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""
    #DONE
    def __init__(self, board=[3,1]):
        moves = [(x, (y+1)) for x in range(0, len(board))
                 for y in range(0, board[x])]
        self.initial = GameState(to_move='AI', utility=0, board=board, moves=moves)

    def result(self, state, move):
        if move not in state.moves:
            return state
        board = state.board.copy()
        moves = state.moves.copy()

        move_row = move[0]
        stick_amount = move[1]
        board_sticks = board[move_row]
        new_amount = board_sticks - stick_amount

        board[move_row] = new_amount

        moves = [(x, (y+1)) for x in range(0, len(board))
                 for y in range(0, board[x])]

        return GameState(to_move=('Human' if state.to_move == 'AI' else 'AI'), 
                                  utility=self.compute_utility(board, move, state.to_move), 
                                  board=board, moves=moves)

    #DONE
    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    #DONE
    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        return len(state.moves) == 0
        
    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'AI' else -state.utility
        # if player == "AI":
        #     return +1
        # elif player == "Human":
        #     return -1

    #DONE
    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    #DONE
    def display(self, state):
        board = state.board
        print("board: ", board)

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (self.k_in_row(board, move, player, (0, 1)) or
                self.k_in_row(board, move, player, (1, 0)) or
                self.k_in_row(board, move, player, (1, -1)) or
                self.k_in_row(board, move, player, (1, 1))):
            return +1 if player == 'Human' else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y = move
        n = 0  # n is number of moves in row
        while move == player:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = move
        while move == player:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        return n

if __name__ == "__main__":

    #nim = GameOfNim(board=[0, 0, 1, 1]) # Creating the game instance
    nim = GameOfNim(board=[0, 5, 3, 1]) # Creating the game instance
    #nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    print(nim.initial.board) # must be [0, 5, 3, 1]
    print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2,1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1,1) ))
    utility = nim.play_game(alpha_beta_player, query_player) # computer moves first
    if (utility < 0):
        print("MIN won the game")
    else:
        print("MAX won the game")

    # nim = TicTacToe()
    # utility = nim.play_game(alpha_beta_player, query_player)
    # if (utility < 0):
    #     print("MIN won the game")
    # else:
    #     print("MAX won the game")