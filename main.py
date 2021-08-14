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
        print("\n=======================\n")

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


ROW = 10
COLUMN = 10


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

if __name__ == "__main__":
    field = Field(ROW, COLUMN, Flat())

    pos = find_flat_pos(field)
    predator = Predator(pos[0], pos[1])

    pos = find_flat_pos(field)
    prey = Prey(pos[0], pos[1])

    field.change_nature(predator.get_pos()[0],
                        predator.get_pos()[1],
                        predator)
    field.change_nature(prey.get_pos()[0],
                        prey.get_pos()[1],
                        prey)

    field.print_field()

    while(True):
        random_move_predator(field,predator)
        field.print_field()
        time.sleep(1)
