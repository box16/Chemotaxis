import copy
import random
import time


class Nature():
    def __init__(self):
        self.mark = None

    def get_mark(self):
        return self.mark


class Creature(Nature):
    def __init__(self, row_pos, column_pos):
        self.mark = None
        self.row_pos = row_pos
        self.column_pos = column_pos

    def suggest_next_pos(self):
        move_direction = [-1, 0, 1]
        row_move = random.choice(move_direction)
        column_move = random.choice(move_direction)
        return (self.row_pos + row_move,
                self.column_pos + column_move)

    def get_pos(self):
        return (self.row_pos, self.column_pos)

    def set_pos(self, row_pos, column_pos):
        self.row_pos = row_pos
        self.column_pos = column_pos


class Predator(Creature):
    def __init__(self, row_pos, column_pos):
        super().__init__(row_pos, column_pos)
        self.mark = "O"
        self.search_radius = 5
    
    def get_search_range(self):
        return ((self.row_pos - self.search_radius,
                 self.column_pos - self.search_radius),
                (self.row_pos + self.search_radius,
                 self.column_pos + self.search_radius))


class Prey(Creature):
    def __init__(self, row_pos, column_pos):
        super().__init__(row_pos, column_pos)
        self.mark = "X"


class Terrain(Nature):
    def __init__(self):
        self.mark = None


class Flat(Terrain):
    def __init__(self):
        self.mark = "-"


class Cell():
    def __init__(self, nature):
        self.nature = nature

    def change_nature(self, nature):
        self.nature = nature

    def get_mark(self):
        return self.nature.get_mark()


class Field():
    def __init__(self, row_num, column_num, nature):
        self.field = [[Cell(nature) for i in range(column_num)]
                      for j in range(row_num)]

    def print_field(self):
        for line in self.field:
            for element in line:
                print(element.get_mark(), end="  ")
            print()

    def change_nature(self, row, column, nature):
        self.field[row][column].change_nature(nature)

    def check_field_over(self, row, column):
        if (row < 0) or (row >= len(self.field)):
            return True
        elif (column < 0) or (column >= len(self.field[0])):
            return True
        else:
            return False

    def get_mark(self, row, column):
        return self.field[row][column].get_mark()


ROW = 20
COLUMN = 20


def find_flat_pos(field):
    while(True):
        row = random.choice(range(ROW))
        column = random.choice(range(COLUMN))
        if(field.get_mark(row, column) == Flat().get_mark()):
            return (row, column)


def random_move_predator(field, predator):
    while(True):
        now_pos = predator.get_pos()
        suggest_pos = predator.suggest_next_pos()
        if (field.check_field_over(suggest_pos[0],
                                   suggest_pos[1])):
            continue
        if(now_pos == suggest_pos):
            continue
        predator.set_pos(suggest_pos[0],
                         suggest_pos[1])
        field.change_nature(predator.get_pos()[0],
                            predator.get_pos()[1],
                            predator)
        field.change_nature(now_pos[0],
                            now_pos[1],
                            Flat())
        return

def move_predator_for_prey(field, predator,prey_row,prey_column):
    predator_row = predator.get_pos()[0]
    predator_column = predator.get_pos()[1]
    diff_row = prey_row - predator_row
    diff_column = prey_column - predator_column
    move_row = 0 if diff_row == 0 else int(diff_row/abs(diff_row))
    move_column = 0 if diff_column == 0 else int(diff_column/abs(diff_column))
    predator.set_pos(predator_row + move_row,
                     predator_column + move_column)
    field.change_nature(predator.get_pos()[0],
                        predator.get_pos()[1],
                        predator)
    field.change_nature(predator_row,
                        predator_column,
                        Flat())
    return

def search_prey(field, predator):
    search_range = predator.get_search_range()
    min_row = search_range[0][0]
    max_row = search_range[1][0]
    min_column = search_range[0][1]
    max_column = search_range[1][1]
    for i in range(min_row,max_row):
        for j in range(min_column,max_column):
            if(field.check_field_over(i,j)):
                continue
            if(field.get_mark(i, j) == Prey(0,0).get_mark()):
                return (i,j)
    return None

def create_prey(field):
    pos = find_flat_pos(field)
    preys = Prey(pos[0], pos[1])
    field.change_nature(preys.get_pos()[0],
                        preys.get_pos()[1],
                        preys)

if __name__ == "__main__":
    field = Field(ROW, COLUMN, Flat())

    pos = find_flat_pos(field)
    predator = Predator(pos[0], pos[1])
    field.change_nature(predator.get_pos()[0],
                        predator.get_pos()[1],
                        predator)

    for i in range(3):
        create_prey(field)
        
    while(True):
        field.print_field()
        prey_pos = search_prey(field, predator)
        if prey_pos:
            move_predator_for_prey(field, predator,prey_pos[0],prey_pos[1])
        else:
            random_move_predator(field,predator)
        
        if random.choice(range(100)) < 5:
            create_prey(field)
        print("\n=======================\n")
        time.sleep(0.1)