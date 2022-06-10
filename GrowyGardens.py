import pyxel

"""
Comment utiliser
------
README GOES HERE

"""

# Key bindings
up_key = pyxel.KEY_UP
down_key = pyxel.KEY_DOWN
left_key = pyxel.KEY_LEFT
right_key = pyxel.KEY_RIGHT

water_key = pyxel.KEY_1
plant_key = pyxel.KEY_2
bonk_key = pyxel.KEY_3


field_x = 128
field_y = 120

class Sprite:
    pass

    def __init__(self, sheetX, sheetY, sheetW, sheetH, colourKey = 0):
        self.sheetX = sheetX
        self.sheetY = sheetY
        self.sheetW = sheetW
        self.sheetH = sheetH
        self.colKey = colourKey
        self.sheet = 0

    def draw(self,x,y):
        pyxel.blt(x ,y , self.sheet, self.sheetX, self.sheetY, self.sheetW,self.sheetH, self.colKey)


class Bed:
    pass

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.cooldown = 0
        self.direction = 0 # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = 0 # 0 water, 1 plant, 2 bonk, also for drawing

        self.playerSprite = Sprite(0,0,8,16,0)

    def move(self):
        if pyxel.btn(up_key):
            self.y -= 1
            self.direction = 3
        if pyxel.btn(down_key):
            self.y += 1
            self.direction = 0
        if pyxel.btn(left_key):
            self.x -= 1
            self.direction = 1
        if pyxel.btn(right_key):
            self.x += 1
            self.direction = 2
    
    def draw(self):
        self.playerSprite.draw(self.x,self.y)

class Crow:
    def __init__(self, targetX: int, targetY: int, killTime: int):
        self.movesToGo = 60 # frames
        self.targetX = targetX
        self.targetY = targetY
        self.x, self.y = 0, 0
        self.arrived = False
        self.onWayBack = False
        self.clock = killTime

    def update(self) -> None:
        if self.arrived:
            self.clock -= 1
            if self.clock == 0:
                self.movesToGo = 30 # frames
                self.targetX, self.targetY = 0, 0
                self.onWayBack = True
                self.arrived = False

        # Movement
        if not self.arrived:
            if self.movesToGo == 1:
                self.x = self.targetX
                self.y = self.targetY
                self.arrived = True
            else:
                self.x += (self.targetX-self.x)/self.movesToGo
                self.y += (self.targetY-self.y)/self.movesToGo

    def shoo(self) -> None:
        self.movesToGo = 15 # frames
        self.targetX, self.targetY = 0, 0
        self.onWayBack = True
        self.arrived = False

    def draw(self) -> None:
        pass

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.load("TestGraphics.pyxres")

        self.player = Player()
        self.crows = []

        pyxel.run(self.update, self.draw)
    
    def update(self) -> None:
        self.player.move()
        print(self.player.x,self.player.y)

    def draw(self) -> None:
        pyxel.cls(3)
        self.player.draw()

game = App()
