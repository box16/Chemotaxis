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
                print(element,end="\t")
            print()
        print("\n=======================\n")
    
    def update_field(self,row,column,mark="-"):
        self.field[row][column] = mark

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

if __name__=="__main__":
    ROW = 5
    COLUMN = 5
    field = Field(ROW,COLUMN)
    predator = Predator()

    field.print_field()

    for i in range(10):
        # Predatorの現在位置取得
        now_pos = predator.get_pos()

        # Predatorの移動位置決定
        next_row = random.choice(range(ROW))
        next_column = random.choice(range(COLUMN))
        predator.update_pos(next_row,next_column)

        # Fieldの更新
        field.update_field(now_pos[0],now_pos[1])
        next_pos = predator.get_pos()
        field.update_field(next_pos[0],next_pos[1],mark=predator.get_mark())

        field.print_field()
        time.sleep(1)