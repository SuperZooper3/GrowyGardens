import pyxel

"""
Comment utilliser
------
README GOES HERE

"""

# Key bindings
up_key = "KEY_UP"
down_key = "KEY_DOWN"
left_key = "KEY_LEFT"
right_key = "KEY_RIGHT"

water_key = "KEY_1"
plant_key = "KEY_2"
bonk_key = "KEY_3"


feild_x = 128
feild_y = 120


class Bed:
    pass

class Player:
    pass

    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.cooldown = 0
        self.direction = 0 # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = # 0 water, 1 plant, 2 bonk, also for drawing

    def move(self):
        if pyxel.btnp(up_key):
            self.y -= 1
            self.direction = 3
        if pyxel.btnp(down_key):
            self.y += 1
            self.direction = 0
        if pyxel.btnp(left_key):
            self.x -= 1
            self.direction = 1
        if pyxel.btnp(right_key):
            self.x += 1
            self.direction = 2
    
    def draw(self):


    

class Crow:
    pass

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.run(self.update, self.draw)
    
    def update(self) -> None:
        pass

    def draw(self) -> None:
        pass

App()
