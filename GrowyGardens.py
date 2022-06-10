import pyxel
from random import randint

"""
Comment utiliser
------
README GOES HERE

"""

# Key bindings
up_keys = [pyxel.KEY_UP, pyxel.KEY_W]
down_keys = [pyxel.KEY_DOWN, pyxel.KEY_S]
left_keys = [pyxel.KEY_LEFT, pyxel.KEY_A]
right_keys = [pyxel.KEY_RIGHT, pyxel.KEY_D]

water_keys = [pyxel.KEY_1, pyxel.KEY_J]
plant_keys = [pyxel.KEY_2, pyxel.KEY_K]
bonk_keys = [pyxel.KEY_3, pyxel.KEY_L]

def input_pressed(key_list):
    for k in key_list:
        if pyxel.btn(k): 
            return True
    return False

field_x = 128
field_y = 120

# Balance Variables
min_plant_age = 10 * 30
max_plant_age = 20 * 30
min_plant_dry = 5 * 30
max_plant_dry = 15 * 30
crow_eat_time = 10 * 30
crow_chance = 0.5


class Sprite:
    def __init__(self, sheetX: int, sheetY: int, sheetW: int, sheetH: int, colourKey: int = 0):
        self.sheetX = sheetX
        self.sheetY = sheetY
        self.sheetW = sheetW
        self.sheetH = sheetH
        self.colKey = colourKey
        self.sheet = 0

    def draw(self, x: int, y: int) -> None:
        pyxel.blt(x, y, self.sheet, self.sheetX, self.sheetY,
                  self.sheetW, self.sheetH, self.colKey)


class PlantSprite:
    def __init__(self, seedSprite, sproutSprite, grownSprite, deadSprite):
        self.seedSprite = seedSprite
        self.sproutSprite = sproutSprite
        self.grownSprite = grownSprite
        self.deadSprite = deadSprite

    def draw(self, x, y, n):  # n = 0 for seed, n = 1 for sprout, n = 2 for grown, n = 3 for dead
        if n == 0:
            self.seedSprite.draw(x, y)
        elif n == 1:
            self.sproutSprite.draw(x, y)
        elif n == 2:
            self.grownSprite.draw(x, y)
        elif n == 3:
            self.deadSprite.draw(x, y)
        else:
            print("plantSpriteDrawError")


canIconSprite = Sprite(48,96,8,8)
batIconSprite = Sprite(56,96,8,8)
seedBagIconSprite = Sprite(48,104,8,8)
coinIconSprite = Sprite(56,104,8,8)
crowColourIconSprite = Sprite(32,168,8,8)
crowGreyIconSprite = Sprite(40,168,8,8)
clockFirstSprite = Sprite(48,112,16,8)
clockSecondSprite = Sprite(48,120,16,8)
clockThirdSprite = Sprite(48,128,16,8)
clockFourthSprite = Sprite(48,136,16,8)


crowSprite = Sprite(32,0,8,8)

crowSprite = Sprite(32, 0, 8, 8)

plantNames = ["green", "pink", "blue", "orang"]

plantSprites = {
    "green": PlantSprite(
        Sprite(16, 16, 8, 8),
        Sprite(16, 32, 8, 8),
        Sprite(16, 0, 8, 8),
        Sprite(40,0,8,8),
    ),
    "pink": PlantSprite(
        Sprite(24, 16, 8, 8),
        Sprite(24, 32, 8, 8),
        Sprite(24, 0, 8, 8),
        Sprite(40,0,8,8),
    ),
    "blue": PlantSprite(
        Sprite(16, 24, 8, 8),
        Sprite(16, 40, 8, 8),
        Sprite(16, 32, 8, 8),
        Sprite(40,0,8,8),
    ),
    "orang": PlantSprite(
        Sprite(24, 24, 8, 8),
        Sprite(24, 40, 8, 8),
        Sprite(24, 32, 8, 8),
        Sprite(40,0,8,8),
    ),
}


class Bed:
    def __init__(self, x: int, y: int):
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
        self.crow = False  # False means crow hasn't spawned yet, True means crow has spawned and is now gone, and if it's a crow object then the crow is on the scene
        self.state = 0  # n = 0 for seed, n = 1 for sprout, n = 2 for grown

    def draw(self) -> None:
        if self.isWatered:
            wetBedSprite.draw(self.x, self.y)
        else:
            dryBedSprite.draw(self.x, self.y)
        if self.isPopulated:
            sprite = plantSprites[self.plantType]
            sprite.draw(self.x, self.y, self.state)

    def drawCrow(self) -> None:
        if type(self.crow) == Crow:
            self.crow.draw()

    def water(self) -> None:
        self.waterLeft = randint(min_plant_dry, max_plant_dry)
        self.isWatered = True

    def plant(self) -> None:
        type = plantNames[randint(0, len(plantNames)-1)]
        self.isPopulated = True
        self.plantType = type
        self.plantAge = 0
        self.maturityAge = randint(min_plant_age, max_plant_age)
        self.timeUntilCrow = randint(30, self.maturityAge * (1/crow_chance))

    def bonk(self) -> None:
        if type(self.crow) == Crow:
            self.crow.shoo()

    def age(self):

        print(self.waterLeft, self.plantAge, self.maturityAge)

        if self.isPopulated and self.isWatered:
            self.plantAge += 1
            self.timeUntilCrow -= 1
            self.waterLeft -= 1

        if self.waterLeft <= 0:
            self.isWatered = False

        if self.timeUntilCrow <= 0 and self.crow == None:
            self.crow = Crow(self.x, self.y)

        # If crow is present then update it
        if type(self.crow) == Crow:
            self.crow.update()
            if self.crow.atePlant == True:
                self.isDead = True
            if self.crow.arrived and self.crow.onWayBack:
                self.crow = True  # Crow is gone

        if self.plantAge >= self.maturityAge:
            self.state = 2
        elif self.plantAge >= self.maturityAge // 2:
            self.state = 1
        elif self.isDead:
            self.state = 3
        else:
            self.state = 0

    def bonk(self):
        pass  # bonk the crow
        self.timeUntilCrow = -1


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.cooldown = 0
        self.direction = 0  # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = 0  # 0 water, 1 plant, 2 bonk, also for drawing

    def move(self) -> None:
        if input_pressed(up_keys):
            if self.y -1 >= 0:
                self.y -= 1
                self.direction = 3
        if input_pressed(down_keys):
            if self.y + 1 > field_y - :
                self.y += 1
                self.direction = 0
        if input_pressed(left_keys):
            self.x -= 1
            self.direction = 1
        if input_pressed(right_keys):
            self.x += 1
            self.direction = 2

    def draw(self) -> None:
        playerSprite.draw(self.x, self.y)


class Crow:
    def __init__(self, targetX: int, targetY: int):
        self.movesToGo = 60  # frames
        self.targetX = targetX
        self.targetY = targetY
        self.arrived = False
        self.onWayBack = False
        self.clock = crow_eat_time
        self.atePlant = False
        edge = randint(0, 3)  # 0 bottom, 1 left, 2 top, 3 right
        if edge == 0:
            self.x = randint(0, 127)
            self.y = 127
        elif edge == 1:
            self.x = 0
            self.y = randint(0, 127)
        elif edge == 2:
            self.x = randint(0, 127)
            self.y = 0
        elif edge == 3:
            self.x = 127
            self.y = randint(0, 127)

    def update(self) -> None:
        if self.arrived:
            self.clock -= 1
            if self.clock == 0:
                self.movesToGo = 60  # frames
                self.onWayBack = True
                self.arrived = False
                self.atePlant = True
                edge = randint(0, 3)  # 0 bottom, 1 left, 2 top, 3 right
                if edge == 0:
                    self.targetX = randint(0, 127)
                    self.targetY = 127
                elif edge == 1:
                    self.targetX = 0
                    self.targetY = randint(0, 127)
                elif edge == 2:
                    self.targetX = randint(0, 127)
                    self.targetY = 0
                elif edge == 3:
                    self.targetX = 127
                    self.targetY = randint(0, 127)

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
        self.movesToGo = 15  # frames
        self.onWayBack = True
        self.arrived = False
        edge = randint(0, 3)  # 0 bottom, 1 left, 2 top, 3 right
        if edge == 0:
            self.targetX = randint(0, 127)
            self.targetY = 127
        elif edge == 1:
            self.targetX = 0
            self.targetY = randint(0, 127)
        elif edge == 2:
            self.targetX = randint(0, 127)
            self.targetY = 0
        elif edge == 3:
            self.targetX = 127
            self.targetY = randint(0, 127)

    def draw(self) -> None:
        crowSprite.draw(self.x, self.y)


class App:
    def __init__(self):
        pyxel.init(128, 128, title="Nuit du c0de 2022")
        pyxel.load("GrowyGardens.pyxres")

        self.player = Player()

        self.testBed = Bed(80, 80)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        self.player.move()
        self.testBed.age()

        # Testing code
        if pyxel.btnp(pyxel.KEY_O):
            self.testBed.plant()
            print(self.testBed.timeUntilCrow)
            self.testBed.timeUntilCrow = 30

        if pyxel.btnp(pyxel.KEY_U):
            self.testBed.water()

    def draw(self) -> None:
        pyxel.cls(3)

        self.testBed.draw()

        self.player.draw()
        self.testBed.drawCrow()


game = App()
