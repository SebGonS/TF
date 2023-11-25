import random

from globals import Global
from pade.core.agent import Agent
from PySide6.QtGui import QColor

class BotAgent(Agent):
    def __init__(self):
        self.x = random.randint(1, Global.width-1)
        self.y = random.randint(1, Global.height-1)
        self.random_c=random.randint(0, 0xffffff)
        self.color = QColor(self.random_c)
        self.size = Global.pixel_size
        self.speed = 4-self.random_c*3/0xffffff
        self.power = 3*self.random_c//0xffffff

        self.direction = random.choice([(1, 0),(1,1),(-1,-1),(1,-1),(-1,1), (-1, 0), (0, 1), (0, -1)])
        self.cleaning = 0
        self.status = -1

    
    def updateStatus(self):
        return
        # self.step+=1
        # self.step=self.step%3
        # if self.y < 500:
        #     self.status = 1
        #     if self.x > 100 + Global.x_center:
        #         self.status = 4;

        # elif self.y > 900:
        #     self.status = 2;
        #     if self.x < 30 + Global.x_center:
        #         self.status = 3

        # else:
        #     if self.x < 30 + Global.x_center:
        #         self.status = 3
        #     else:
        #         self.status = 4
    def spriteDir(self):
        if self.status==1 or self.status==-1: return 2
        if self.status==2: return 1
        if self.status==3: return 3
        if self.status==4: return 0
    def move(self):
        if self.cleaning:
            return
        new_x = self.x + self.direction[0]
        new_y = self.y + self.direction[1]

        
        if 0 < new_x < Global.width-1 and 0 < new_y < Global.height-1:
            self.x = new_x
            self.y = new_y
        else:
            self.x = max(0, min(new_x, Global.width-1))
            self.y = max(0, min(new_y, Global.height-1))
           
            possible_directions = [(1, 0),(1,1),(-1,-1),(1,-1),(-1,1), (-1, 0), (0, 1), (0, -1)]
            if self.direction in possible_directions:
                possible_directions.remove(self.direction)
            self.direction = random.choice(possible_directions)


