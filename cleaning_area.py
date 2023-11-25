import random
from globals import Global
class CleaningArea:
    def __init__(self):
        self.width = Global.width
        self.height= Global.height
        self.cell_size= Global.pixel_size
        self.map = [[random.randint(0, 5) for _ in range(self.width)] for _ in range(self.height)]
        self.initial_dirtiness=sum(sum(row)for row in self.map)
        self.dirtiness=self.initial_dirtiness
        self.progress=0
    def print_map(self):
        for row in self.map:
            print(" ".join(str(cell) for cell in row))

