# Author: Daniel Beeunas
# Date: 08/13/2020
# Description: Implement a simple version of the "Black Box Game".
# It takes place on a 10x10 grid. Rows 0 and 9, and columns 0 and 9 (border squares), are used by the guessing
# player for shooting rays into the black box. The atoms are restricted to being within rows 1-8 and columns 1-8
# Each player starts with 25 points. Each entry and exit location counts as a point (but not more than once),
# each wrong guess of an atom's location costs 5 points (but not for duplicate guesses).
# This is all accomplished using a class named BlackBoxGame and methods to methods to set up the board, place atoms,
# display the board (for testing purposes),
# shoot rays, check the results of shooting rays and account for hits/reflects/deflects,
# and it will allow players to guess an atoms location and keep track of their score


class BlackBoxGame():
    """A class representing a 10x10 game board  with methods to play “Black Box.
     It will include methods to set up the board, place atoms, display the board (for testing purposes),
     shoot rays, check the results of shooting rays and account for hits/reflects/deflects,
     and it will allow players to guess an atoms location and keep track of their score"""

    def __init__(self, atoms_list):
        self.board = [[' ' for x in range(10)] for y in range(10)]
        self.atoms_list = atoms_list
        self.set_up_board()
        self.score = 25
        self.guesses = []

    def set_up_board(self):
        """Sets up the board in a human-readable way."""
        # Place the atoms
        self.place_atoms()
        for row in range(10):
            for column in range(10):
                # Mark the edges with 'E' to show they are fresh edges. 'e' shows they have been an entry/exit point
                if row == 0 or row == 9 or column == 0 or column == 9:
                    self.board[row][column] = 'E'
        # Mark the corners with Xs to show they're invalid
        for corner in [[0,0],[0,9],[9,0],[9,9]]:
            self.board[corner[0]][corner[1]] = 'X'

    def place_atoms(self):
        """Marks the atoms on game board. They are marked as an 'A'."""
        for row, column in self.atoms_list:
            self.board[row][column] = 'A'

    def display_board(self):
        """Prints a representation of the board to the terminal."""
        for row in self.board:
            print(row)

    def shoot_ray(self, row, column):
        """Make a move by shooting a ray from the given position.

        Parameters:
            row, column: the coordinates for the move. coordinates must be for a non-corner edge cell.

        Returns:
            False if the coordinates are invalid
            (r, c): a tuple indidcating where the ray exited
            None if the ray hit an atom directly
        """
        if row in [0, 9] or column in [0, 9]:
            # Return False if the move is at a corner
            if self.board[row][column] == 'X':
                return False
            # Mark the entry point and adjust the score
            if self.board[row][column] == 'E':
                self.board[row][column] = 'e'
                self.score -= 1

            # Determine the direction the ray is moving in and make one move
            if row == 0:
                direction = [1,0]# 'DOWN'
            elif row == 9:
                direction = [-1,0]# 'UP'
            elif column == 0:
                direction = [0,1]# 'RIGHT'
            elif column == 9:
                direction = [0,-1]# 'LEFT'

            return self.ray_walk(row, column, direction)

        # Return False if the coordinates are invalid
        else:
            return False

    def ray_walk(self, row, column, direction):
        """Recursively walk along the path through the black box."""
        # Move in the given direction
        row += direction[0]
        column += direction[1]
        # Return None if the ray hit an atom
        if self.board[row][column] == 'A':
            return None
        # Return if the ray hit an edge
        elif self.board[row][column] == 'E':
            self.board[row][column] = 'e'
            self.score -= 1
            return (row, column)
        elif self.board[row][column] == 'e':
            return (row, column)
        # Check for nearby atoms and update the direction.
        direction = self.check_surroundings(row, column, direction)
        return self.ray_walk(row, column, direction)

    def check_surroundings(self, row, column, direction):
        """Check the area around the given coordinate for atoms."""
        # Create a list of neighbors to check.
        cardinal_neighbors = [(row + 1, column), (row-1, column), (row, column + 1), (row, column-1)]
        # Remove the neighbor that the ray is about to move to. This prevents reflecting instead of absorbing
        cardinal_neighbors.remove((row+direction[0], column+direction[1]))
        corner_neighbors = [(row+1, column +1), (row-1, column+1), (row+1, column-1), (row-1, column-1)]
        # If there's an atom up, down, left, or right, reflect the ray.
        for r, c in cardinal_neighbors:
            if self.board[r][c] == 'A':
                direction[0]  *= -1
                direction[1]  *= -1
                return direction

        for r, c in corner_neighbors:
            if self.board[r][c] == 'A':
                direction[0] = row + direction[0] - r
                direction[1] = column + direction[1] - c
        return direction

    def guess_atom(self, row, column):
        """Allow the player to guess an atom position.

        Indicate if there is an atom at the given position.
        Update the score appropriately.

        Parameters:
            row, column: the coordinates for the move

        Returns:
            correct: True if an atom is at the position, False otherwise.

        """
        guess = (row, column)
        if self.board[row][column] == 'A':
            if guess in self.atoms_list:
                self.atoms_list.remove(guess)
            self.guesses.append(guess)
            return True
        else:
            if guess not in self.guesses:
                self.score -= 5
                self.guesses.append(guess)
            return False

    def get_score(self):
        """Returns the current score"""
        return self.score

    def atoms_left(self):
        """Returns the number of un-found atoms left"""
        return len(self.atoms_list)


