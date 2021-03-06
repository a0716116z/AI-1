import copy
from variable import Variable


class Board():
    def __init__(self, inputs):
        args = inputs.split()
        self.size_x = int(args[0])
        self.size_y = int(args[1])
        self.mines_count = int(args[2])
        self.hints = []

        idx = 3
        for i in range(self.size_y):
            for j in range(self.size_x):
                if i == 0:
                    self.hints.append([])
                self.hints[j].append(int(args[idx]))
                idx += 1

    def available_position(self, position):
        # Returns true if the given position is available on this board
        return 0 <= position[0] < self.size_x and 0 <= position[1] < self.size_y

    def around_position(self, position):
        # Returns a list of available postions around the given position
        x = position[0]
        y = position[1]
        psb_pos = [(x-1, y-1), (x, y-1), (x+1, y-1), 
                   (x-1, y),             (x+1, y), 
                   (x-1, y+1), (x, y+1), (x+1, y+1)]
        around = []
        for pos in psb_pos:
            if self.available_position(pos):
                around.append(pos)
        return around

    def current_board(self, asgn_vrbls = []):
        # Return a list of current board status
        current = copy.deepcopy(self.hints)
        for variable in asgn_vrbls:
            x = variable.position[0]
            y = variable.position[1]
            if variable.assignment == 0:
                current[x][y] = -2
            elif variable.assignment == 1:
                current[x][y] = -3
        return current

    def print_board(self, asgn_vrbls = []):
        # Print the current board status
        # _     : Unassigned
        # |     : Assigned no mine
        # *     : Assigned mine
        # [0-8] : Hint
        current = self.current_board(asgn_vrbls)
        for j in range(self.size_y):
            for i in range(self.size_x):
                current[i][j] = '_' if current[i][j] == -1 else current[i][j]
                current[i][j] = '|' if current[i][j] == -2 else current[i][j]
                current[i][j] = '*' if current[i][j] == -3 else current[i][j]
                print(current[i][j], end=" ")
            print()
    
    def forward_checking_limit(self, asgn_vrbls, position):
        # Returns lower and upper bounds of the sum of the given position
        current = self.current_board(asgn_vrbls)
        lower_bound = 0
        upper_bound = 0
        around = self.around_position(position)
        for a in around:
            if current[a[0]][a[1]] == -3:
                lower_bound += 1
                upper_bound += 1
            elif current[a[0]][a[1]] == -1:
                upper_bound += 1
        return lower_bound, upper_bound

    def arc_consistent_check(self, asgn_vrbls, position):
        # Returns difference of hint and mines count
        x = position[0]
        y = position[1]
        if not self.available_position(position):
            return 0
        if self.hints[x][y] == -1:
            return 0
        
        current = self.current_board(asgn_vrbls)
        
        bombs_count = 0
        around = self.around_position(position)
        for a in around:
            if current[a[0]][a[1]] == -3:
                bombs_count += 1

        return self.hints[x][y] - bombs_count

    def global_constraint_check(self, asgn_vrbls):
        # Returns difference of tolal mines and current assigned mines count
        mines_count = 0
        for variable in asgn_vrbls:
            if variable.assignment == 1:
                mines_count += 1

        return self.mines_count - mines_count

