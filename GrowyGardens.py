import pyxel
from random import randint

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


# Balance Variables
min_plant_age = 10 * 30
max_plant_age = 20 * 30
min_plant_dry = 5 * 30
max_plant_dry = 15 * 30
crow_eat_time = 5 * 30
crow_chance = 0.5

class Sprite:
    def __init__(self, sheetX, sheetY, sheetW, sheetH, colourKey = 0):
        self.sheetX = sheetX
        self.sheetY = sheetY
        self.sheetW = sheetW
        self.sheetH = sheetH
        self.colKey = colourKey
        self.sheet = 0

    def draw(self,x,y):
        pyxel.blt(x ,y , self.sheet, self.sheetX, self.sheetY, self.sheetW,self.sheetH, self.colKey)

playerSprite = Sprite(0,0,8,16,0)
dryBedSprite = Sprite(8,8,8,8)
wetBedSprite = Sprite(8,0,8,8)

crowSprite = Sprite(32,0,8,8)

plantNames = ["green","pink","blue","orange"]

plantSprites = {
    "green": Sprite(16,0,8,8),
    "pink": Sprite(24,0,8,8),
    "blue": Sprite(16,8,8,8),
    "orang": Sprite(24,8,8,8),
    "Empty": Sprite(0,0,0,0),
}

class Bed:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.isDead = False
        self.isPopulated = False
        self.isWatered = False
        self.plantType = "Empty"
        self.plantAge = 0
        self.maturityAge = 0
        self.waterLeft = 0
        self.timeUntilCrow = 0
        self.crow = False # False means crow hasn't spawned yet, True means crow has spawned and is now gone, and if it's a crow object then the crow is on the scene
    
    def draw(self):
        if self.isWatered:
            wetBedSprite.draw(self.x, self.y)
        else:
            dryBedSprite.draw(self.x, self.y)
        plantSprites[self.plantType].draw(self.x,self.y)
    
    def water(self) -> None:
        self.waterLeft = randint(min_plant_dry,max_plant_dry)
        self.isWatered = True

    def plant(self):
        type = plantNames[randint(0,len(plantNames)-1)]
        self.isPopulated = True
        self.plantType = type
        self.plantAge = 0
        self.maturityAge = randint(min_plant_age,max_plant_age)
        self.timeUntilCrow = randint(30, self.maturityAge * (1/crow_chance))
    
    def bonk(self) -> None:
        if type(self.crow) == Crow:
            self.crow.shoo()

    def age(self):
        if self.isPopulated:
            self.plantAge += 1
            if self.timeUntilCrow != 0:
                self.timeUntilCrow -= 1
            elif self.crow == False:
                self.crow = Crow(self.x, self.y)
            if self.waterLeft != 0:
                self.waterLeft -= 1
            else:
                self.isWatered = False
            if type(self.crow) == Crow:
                self.crow.update()
                if self.crow.atePlant == True:
                    self.isDead = True
                if self.crow.arrived and self.crow.onWayBack:
                    self.crow = True # Crow is gone
        

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.cooldown = 0
        self.direction = 0 # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = 0 # 0 water, 1 plant, 2 bonk, also for drawing

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
        playerSprite.draw(self.x,self.y)

class Crow:
    def __init__(self, targetX: int, targetY: int):
        self.movesToGo = 60 # frames
        self.targetX = targetX
        self.targetY = targetY
        self.x, self.y = 0, 0
        self.arrived = False
        self.onWayBack = False
        self.clock = crow_eat_time
        self.atePlant = False

    def update(self) -> None:
        if self.arrived:
            self.clock -= 1
            if self.clock == 0:
                self.movesToGo = 60 # frames
                self.targetX, self.targetY = 0, 0
                self.onWayBack = True
                self.arrived = False
                self.atePlant = True

        # Movement
        if not self.arrived:
            if self.movesToGo == 1:
                self.x = self.targetX
                self.y = self.targetY
                self.arrived = True
            else:
                self.x += (self.targetX-self.x)/self.movesToGo
                self.y += (self.targetY-self.y)/self.movesToGo
            self.movesToGo -= 1

    def shoo(self) -> None:
        self.movesToGo = 15 # frames
        self.targetX, self.targetY = 0, 0
        self.onWayBack = True
        self.arrived = False

    def draw(self) -> None:
        crowSprite.draw(self.x, self.y)

class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.load("TestGraphics.pyxres")

        self.player = Player()

        self.testBed = Bed(8,8)

        pyxel.run(self.update, self.draw)
    
    def update(self) -> None:
        self.player.move()

        # Testing code
        if pyxel.btnp(pyxel.KEY_O):
            self.testBed.plant()

    def draw(self) -> None:
        pyxel.cls(3)
        
        self.testBed.draw()

        self.player.draw()

game = App()
