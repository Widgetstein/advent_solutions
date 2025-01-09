

class ObstacleError(Exception):
    pass

class OutOfBoardError(Exception):
    pass


class Board:
    def __init__(self, board_input: str):
        self.board = board_input
        self.row_size = None
        self.column_size = None
        self.rows = None
        self.agent_symbol = "OX^><v"
        self.obstacle_symbol = "#"
        self.agent = None
        self.list_of_obstacles = None
        self._calculate_grid_size()
        self.generate_list_of_obstacles()
        self.initialize_agent()

    def _calculate_grid_size(self):
        self.rows = self.board.split("\n")
        self.list_of_rows = self.rows
        self.row_size = len(self.rows[0])
        self.column_size = len(self.rows)

    def recognize_agent_s(self, row: str):
        for symbol in self.agent_symbol:
            row_index = row.find(symbol)
            if row_index >= 0:
                return row_index
        return -1

    def find_position(self):
        for col_index, row in enumerate(self.rows):
            row_index = self.recognize_agent_s(row=row)
            if row_index >=0:
                return col_index, row_index
    
    def find_active_direction(self):
        for row in self.rows:
            for symbol in self.agent_symbol:
                row_index = row.find(symbol)
                if row_index >= 0:
                    return symbol
        return -1
    
    def recognize_obstacles(self, row: str):
        for symbol in self.obstacle_symbol:
            row_index = row.find(symbol)
            if row_index >= 0:
                return row_index
        return -1

    def generate_list_of_obstacles(self):
        list_of_obstacles = []
        for col_index, row in enumerate(self.rows):
            for row_index, letter in enumerate(row):
                if letter in self.obstacle_symbol:
                    list_of_obstacles.append((col_index, row_index))
        self.list_of_obstacles=list_of_obstacles

    def initialize_agent(self):
        col, row = self.find_position()
        active_direction = self.find_active_direction()
        agent = Agent(
            col=col, 
            row=row, 
            max_col=self.column_size, 
            max_row=self.row_size, 
            list_of_obstacles=self.list_of_obstacles,
            active_direction=active_direction
        )
        self.agent=agent

    def update_target_row(self, previous_rows: list):
        row = previous_rows[self.agent.col]
        if self.agent.row < self.agent.max_row:
            right_part = row[self.agent.row + 1:]
        else:
            right_part = ""
        if self.agent.row > self.agent.min_row:
            left_part = row[:self.agent.row]
        else:
            left_part = ""
        middle_part = "O"
        new_row = left_part + middle_part + right_part
        new_row
        return new_row

    def update_board(self):
        previous_rows = [row.replace("O", "X") for row in self.rows]
        new_row = self.update_target_row(previous_rows=previous_rows)
        if self.agent.col < self.agent.max_col:
            lower_part = previous_rows[self.agent.col + 1:]
        else:
            lower_part = None
        if self.agent.col > self.agent.min_col:
            upper_part = previous_rows[:self.agent.col]
        else:
            lower_part = []
        new_rows = [*upper_part, new_row, *lower_part]
        self.rows=new_rows[:]
        self.board = "\n".join(new_rows[:])

    def do_step(self):
        self.agent.move()
        self.update_board()

    def calculate_number_of_steps(self):
        number_of_steps = 0
        for row in self.rows:
            for letter in row:
                if letter in self.agent_symbol:
                    number_of_steps += 1
        return number_of_steps

    def do_simulation(self):
        try:
            while True:
                self.do_step()
        except OutOfBoardError:
            return self.calculate_number_of_steps()

    def __repr__(self):
        return self.board


class Agent:
    def __init__(
            self, row: int, 
            max_row: int, 
            col: int, 
            max_col: int, 
            list_of_obstacles: list, 
            active_direction:str
    ):
        self.row = row
        self.col = col
        self.max_row = max_row
        self.max_col = max_col
        self.min_row = 0
        self.min_col = 0

        self.list_of_obstacles = list_of_obstacles
        self.active_direction = active_direction

    def check_obstacles(self, col, row):
        coordinates = col, row
        if coordinates in self.list_of_obstacles:
            raise ObstacleError("Obstacle, turn please")
        
    def check_out_of_board(self, col, row):
        if (col > self.max_col -1) or  (col < self.min_col):
            raise OutOfBoardError("OutOfBoard, terminate process please")
        if (row > self.max_row - 1) or  (row < self.min_row):
            raise OutOfBoardError("OutOfBoard, terminate process please")

    def update_position(self, row=None, col=None, new_direction: str=None):
        if row is None:
            row = self.row
        if col is None:
            col = self.col
        if new_direction is None:
            new_direction = self.active_direction
        self.check_obstacles(col=col, row=row)
        self.check_out_of_board(col=col, row=row)
        self.row=row
        self.col=col
        self.active_direction=new_direction
    
    def normal_move(self):
        if self.active_direction == "^":
            self.update_position(row=self.row, col=self.col -1, new_direction=self.active_direction)
        elif self.active_direction == ">":
            self.update_position(row=self.row +1, col=self.col, new_direction=self.active_direction)
        elif self.active_direction == "v":
            self.update_position(row=self.row, col=self.col + 1, new_direction=self.active_direction)
        elif self.active_direction == "<":
            self.update_position(row=self.row -1, col=self.col, new_direction=self.active_direction)

    def turn(self):
        if self.active_direction == "^":
            self.update_position(new_direction='>')
        elif self.active_direction == ">":
            self.update_position(new_direction='v')
        elif self.active_direction == "v":
            self.update_position(new_direction='<')
        elif self.active_direction == "<":
            self.update_position(new_direction="^")

    def turn_move(self):
        self.turn()
        self.normal_move()

    def move(self):
        on_going=True
        while on_going: 
            try:
                self.normal_move()
                on_going = False
            except ObstacleError:
                self.turn_move()
                on_going = False
                

    def __repr__(self):
        return f"{self.active_direction} {self.col, self.row}"


board_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


big_board = """.......#.........#..............#........................#......#....#............................#..#...............#............
...................#.............................................#...................................#............................
...............#.................................##.........#..........#.....##...#...#.....#....#..................#.............
#.............................................#..#.............#..........#.##.............................................#......
#.........................................................#.....#........................................##.......................
...........#.......#.#...........#....#.#...#......................................#...........................#...##............#
........................................................#..#.....................................#..#................#....#...#...
#.#.....#.........................#...........#.......................................#.......#.....................##............
.......#..........##.....#........#..................................................#.........................................#.#
#.#..............#.#.............................#............#....#...............#.........................#............#..#.#.#
..........................................................#....................................................#..................
.......................#....#...........#.....................#....#...#.......#..............#.......................#...........
..............................#..............#.......#....................................#.....................#...#...#.........
........#.................#...#....##..............#...........................#............................#.................#...
..................#........................................#......#......................................................#........
.............#.................#...#..............................................................................#...#...........
.....................................#..........................................................#.#.#......#.........#............
..........#...................................................................#.........##.......#..#.............................
...#.#....................................#..#...........#.......................................................##...............
........................................................................................................#.........................
.........#...........#......#..............#........#....................#...#......#.............................................
........#....#...............#....................#..........#.....................................#......#......#........#.#.....
........................#..........................#.......#........................#................#......#.....................
......................................#.........................................#............................#....................
...................................#.#...#...........#.........................................#.....................#............
.................#....#.....................................................................#..................#.........#........
...........#...........................................................#.............................#...............#..#.........
..#.....................#.........................................................................................................
....................#....#.#...........................#...........................................#..............#...............
...#...................................................#.............................................#.........#..........#.......
.............................###.....#..#..#......................................................................................
##................#.#.......#..............#.....#...............#..#............#................................................
......#...............................................#.#..#............................#............#.................#..........
........................................#.#...................................................#.....#.............................
#.......#.#.......................#.....#....................................#...................#................................
...##................................................................................................#.....................#......
............#.............#..................#.................#..................................................................
...#..............#..............................................................................#..........#......#..............
...#..#...#................................................#.....................#......#......................#.......#..........
.................#..#........#...............#.#................#......##.................#.................................#.....
#.....#.......#...........................................#..........#..............................#...#.#..#......#.....#.......
....................................#.........#........#..................#.............................................#.........
#...............................#........................#.................................................#.....#................
..#..................................#.......#.....................#..............................................................
........#...#.....................................#......#..............#..#..#..........................#.#....#.................
.............#..........#....#................#.......#..........................................#.....#..........................
.............................................#................................#.........................#...#.....................
.........#........#...................................................................#.......#....#..............................
....................................#.......................#..............#...............................#......................
....#....................#................................#....#...........#.............#........................................
....#...........#...................#.#..................................................#.....................#..................
..........#....................#............#.##...#.......#....#...............#.....#...#.........................#.............
.......#....................................................................................................#.................#...
...............................................................................#......#.................#...#.....................
..................#........#..........#..........................................................................#................
..........................................................................................#.......................................
.#..#...........#.................................##...........................#.....#...................#..#.....................
........................#..#..........................................................#............#..................#..........#
...........#...................................................##...........................#...............................#.....
........#......................................................................................................#..................
........#..#............................#..#...........#..............................#......................#.##...........#....#
........#...#.#..............#...#.....................#....................#.#..............................#....................
.......................................................#....................................................#..#..................
...........................................#......................#................#........................#....................#
.............#...............#................................................................................#...................
..#...#............#.............#.....#........................#............#....................#...............................
.....#...................................................................................................................#........
....................#..#...........#....#.............................................................................#.......#...
..............#......#.........................#...........#...#...........................................#...#..................
..............................#.....#.........................................................#......#.#......#...................
............................................................#...................#.#............................#..................
.............###.#........................................#........................................................#..............
......#................................#...............##.........................................................................
.........#.....#.#.....................#.......................................#...............#..........#....#....#.............
..............................................#....................................#...........................................#..
............#.#..........#........#..#.....#.............#..........#............#......#...................##..........#.........
............#....#...................................#.............................#.........................#....................
.#..................................#....#.........................................................................#..............
.........................#...#...#.................#..................#.............#.#...#...............#.......................
.........#...............................#...........#.............................#...........................#..........#.......
......#..........................#.............#..........#.......................................................................
.......#...............#.........#.............#...............................#..................................................
..#......#....................##...........................................#........................................#.............
..........................#.....#.......................#...........................................................#.#...........
..#....................#.............#................................................................#.#.........................
.........#....................#.....#....#...............#.......................#........#.......................................
..............#...................................................................#................#...#..........................
....................#.....#.......#..#......................................#...........#..................................##....#
.......#.......................................................................#..................................................
......#.............##..........................#..#......................^.......................................................
..............................#..........#...................#.................................#.....................#............
.......................##..........................#.......#..............................#...................................#.#.
................#....................................................................#...............................#.........#..
..........................................#......#.....................................#................#........#................
#......................................#.......................................................#..#...........#...................
.......#.............#..................#..#...#............#.......#.....#.....#.#...............................................
.............................#........#.............#.....#.......#...................................#.#..................#......
.................#......................................................................................#........#..#.............
........................................................................#..............#.....#..............................#.....
....#....#..........................................#......##...#....................#...................#..........#.............
.................##.......................##.#.........#................................................#.........................
.#..............................................#.........................#.#.#..........#.....................................##.
............................................................#..........#....#...................................................#.
....#...........#.............................#.....................#.........#..................#...........................#....
......#.#.......#..#......#........#..#...................#....#..................................................................
............#........................................................................................................#............
.....................................................#..........................................#................#................
...#.......#..#..............#.............................#....................................#.................................
.................##.........#........................#....................................#...............#.#.#...................
................#......#......................#..#..........................................#.....................................
......#..................................................##.#.#........#...........................#.......................#......
........................#............#......#.........#.............#.............................................#.....#.##......
......................#........................................#.......#.........#.................#..#...........#...............
..#.......#.........##..#.#................................................................................#.........#............
........................................................................................#............#...........#................
................#...#....................#..##..#...............#.............................................................#...
...#........#..........................#.....#..........................#....................................#.........#.......##.
.................#...........................#.........#......#............................#.....................#................
...................#..........#....#.......#...................#.............................#..........#.........................
.......#..............#.................................#.........#....................................#.................#....##.#
..................................#.......................#....#..#.........................#....................#................
.....#.........#............#...#.........#........#...................#...#......................#.....#............#............
#.#....#...#........#................................##..........................#.............................##...#....#........
.............##..........##...#......#.......#.#................#.#.......................#.............#.........................
.............#....................................#....................................#..........................................
..................................#..............................#.......................................#................#.......
...................#...............#..............................................................................................
....#........#.................................#........#.....................................#.......#................#........#.
.................#......#.......................................................##.....#..................#.......................
...............#.......................#.#........#...........................................#........#.........................."""

if __name__ == "__main__":
    b = Board(big_board)
    print(b.do_simulation())