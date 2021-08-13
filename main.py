import copy
import random
import time

PREY = "×"

ROW = range(5)
COLUMN = range(5)

class Field():
    def __init__(self,row,column):
        self.field = [["-" for i in range(column)] for j in range(row)]
    
    def print_field(self):
        for line in self.field:
            for element in line:
                print(element,end="  ")
            print()
        print("\n=======================\n")
    
    def update_field(self,row,column,mark="-"):
        self.field[row][column] = mark
    
    def check_field_over(self,row,column):
        if (row < 0) or (row >= len(self.field)):
            return True
        elif (column < 0) or (column >= len(self.field[0])):
            return True
        else:
            return False

class Predator():
    def __init__(self):
        self.mark = "〇"
        self.pos_row = 0
        self.pos_column = 0

    def get_mark(self):
        return self.mark
    
    def update_pos(self,row,column):
        self.pos_row = row
        self.pos_column = column
    
    def get_pos(self):
        return (self.pos_row,self.pos_column)

def suggest_next_pos(row,column):
    move_direction = [-1,0,1]
    move_row = random.choice(move_direction)
    move_column = random.choice(move_direction)
    next_row = row + move_row
    next_column = column + move_column
    return (next_row,next_column)

if __name__=="__main__":
    ROW = 10
    COLUMN = 10
    field = Field(ROW,COLUMN)
    predator = Predator()

    field.print_field()

    while(True):
        # Predatorの現在位置取得
        now_pos = predator.get_pos()

        # Predatorの移動位置決定
        next_pos = suggest_next_pos(now_pos[0],now_pos[1])
        if field.check_field_over(next_pos[0],next_pos[1]):
            continue
        elif now_pos == next_pos:
            continue
        else:
            predator.update_pos(next_pos[0],next_pos[1])

        # Fieldの更新
        field.update_field(now_pos[0],now_pos[1])
        next_pos = predator.get_pos()
        field.update_field(next_pos[0],next_pos[1],mark=predator.get_mark())

        field.print_field()
        time.sleep(1)