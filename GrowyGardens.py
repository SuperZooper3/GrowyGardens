import pyxel
from random import randint
from math import sqrt

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
bottom_bar_height = 8
path_size = 8
bed_row_size = 5
bed_column_size = 5

# Balance Variables
min_plant_age = 10 * 30
max_plant_age = 20 * 30
min_plant_dry = 5 * 30
max_plant_dry = 15 * 30
min_plant_age = 10 * 30
max_plant_age = 20 * 30
crow_eat_time = 10 * 30
crow_chance = 0.5
actionCooldown = 1 * 30


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
crowColourIconSprite = Sprite(32,168,8,8,7)
crowGreyIconSprite = Sprite(40,168,8,8,7)
clockFirstSprite = Sprite(48,112,16,8)
clockSecondSprite = Sprite(48,120,16,8)
clockThirdSprite = Sprite(48,128,16,8)
clockFourthSprite = Sprite(48,136,16,8)
dryBedSprite = Sprite(32,128,16,16)
wetBedSprite = Sprite(32,144,16,16)
crowSprite = Sprite(0,160,16,16,7)
crowFlySprite = Sprite(16,160,16,16,7)

personStandFrontSprite = Sprite(32,0,16,30)
personStandBackSprite = Sprite(48,0,16,30)
personLeftSprite = Sprite(48,32,16,30)
personRightSprite = Sprite(32,32,16,30)
personBonkSprite = Sprite(32,64,16,30)
personWaterSprite = Sprite(48,64,16,30)
personPlantSprite = Sprite(32,96,16,30)

plantNames = ["pinkFlower", "blueFlower", "yellowFlower", "tomato","blueberry","lettuce","carrot","mushroom"]

plantSprites = {
    "pinkFlower": PlantSprite(
        Sprite(16, 0, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 0, 16, 16),
        Sprite(16,144,16,16),
    ),
    "blueFlower": PlantSprite(
        Sprite(16, 16, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 16, 16, 16),
        Sprite(16,144,16,16),
    ),
    "yellowFlower": PlantSprite(
        Sprite(16, 32, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 32, 16, 16),
        Sprite(16,144,16,16),
    ),
    "tomato": PlantSprite(
        Sprite(16, 48, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 48, 16, 16),
        Sprite(16,144,16,16),
    ),
    "blueberry": PlantSprite(
        Sprite(16, 64, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 64, 16, 16),
        Sprite(16,144,16,16),
    ),
    "lettuce": PlantSprite(
        Sprite(16, 80, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 80, 16, 16),
        Sprite(16,144,16,16),
    ),
    "carrot": PlantSprite(
        Sprite(16, 96, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 96, 16, 16),
        Sprite(16,144,16,16),
    ),
    "mushroom": PlantSprite(
        Sprite(16, 112, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 112, 16, 16),
        Sprite(16,144,16,16),
    ),
}

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
            self.y = 127 + crowSprite.sheetH
        elif edge == 1:
            self.x = 0 - crowSprite.sheetW
            self.y = randint(0, 127)
        elif edge == 2:
            self.x = randint(0, 127)
            self.y = 0 - crowSprite.sheetH
        elif edge == 3:
            self.x = 127 + crowSprite.sheetW
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
                    self.targetY = 127 + crowSprite.sheetH
                elif edge == 1:
                    self.targetX = 0 - crowSprite.sheetW
                    self.targetY = randint(0, 127)
                elif edge == 2:
                    self.targetX = randint(0, 127)
                    self.targetY = 0 - crowSprite.sheetH
                elif edge == 3:
                    self.targetX = 127 + crowSprite.sheetW
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
        if self.arrived:
            self.movesToGo = 15  # frames
            self.onWayBack = True
            self.arrived = False
            edge = randint(0, 3)  # 0 bottom, 1 left, 2 top, 3 right
            if edge == 0:
                self.targetX = randint(0, 127)
                self.targetY = 127 + crowSprite.sheetH
            elif edge == 1:
                self.targetX = 0 - crowSprite.sheetW
                self.targetY = randint(0, 127)
            elif edge == 2:
                self.targetX = randint(0, 127)
                self.targetY = 0 - crowSprite.sheetH
            elif edge == 3:
                self.targetX = 127 + crowSprite.sheetW
                self.targetY = randint(0, 127)

    def draw(self) -> None:
        if self.arrived:
            crowSprite.draw(self.x, self.y)
        else:
            crowFlySprite.draw(self.x,self.y)

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
        self.timeUntilCrow = 1
        self.crow = None
        self.state = 0  # n = 0 for seed, n = 1 for sprout, n = 2 for grown
        self.centerCoords = (self.x + dryBedSprite.sheetW / 2, self.y + dryBedSprite.sheetH / 2)

    def draw(self) -> None:
        if self.isWatered:
            wetBedSprite.draw(self.x, self.y)
        else:
            dryBedSprite.draw(self.x, self.y)
        if self.isPopulated:
            sprite = plantSprites[self.plantType]
            sprite.draw(self.x, self.y, self.state)

    def drawLandedCrow(self) -> None:
        if type(self.crow) == Crow and self.crow.arrived:
            self.crow.draw()
    
    def drawFlyingCrow(self) -> None:
        if type(self.crow) == Crow and not self.crow.arrived:
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
        if self.timeUntilCrow > 0:
            self.timeUntilCrow = randint(30, self.maturityAge * (1/crow_chance))

    def bonk(self) -> None:
        if type(self.crow) == Crow:
            self.crow.shoo()

    def age(self):

        # print(self.waterLeft, self.plantAge, self.maturityAge)

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
                self.isPopulated = False
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
        if type(self.crow) == Crow:
            self.crow.shoo()
            self.timeUntilCrow = -1


class Player:
    def __init__(self, bedList):
        self.x = 0
        self.y = 0
        self.speed = 1.5
        self.cooldown = 0
        self.direction = 0  # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = 0  # 0 water, 1 plant, 2 bonk, also for drawing
        self.bedList = bedList
        self.centerCoords = (self.x + personStandFrontSprite.sheetW / 2, self.y + personStandFrontSprite.sheetH / 2)
        self.closestBed = self.computeClosestBed()

    def move(self) -> None:
        if input_pressed(up_keys):
            if self.y -1 >= 0:
                self.y -= 1
                self.direction = 3
                self.closestBed = self.computeClosestBed()
        if input_pressed(down_keys):
            if self.y + 1 < field_y - personStandFrontSprite.sheetH:
                self.y += 1
                self.direction = 0
                self.closestBed = self.computeClosestBed()
        if input_pressed(left_keys):
            if self.x - 1 >= 0:
                self.x -= 1
                self.direction = 1
                self.closestBed = self.computeClosestBed()
        if input_pressed(right_keys):
            if self.x + 1 < field_x - personStandFrontSprite.sheetW:
                self.x += 1
                self.direction = 2
                self.closestBed = self.computeClosestBed()

    def computeClosestBed(self) -> Bed:
        self.centerCoords = (self.x + personStandFrontSprite.sheetW / 2, self.y + personStandFrontSprite.sheetH / 2)
        closest = self.bedList[0][0]
        closestDist = sqrt((closest.centerCoords[0] - self.centerCoords[0])**2 + (closest.centerCoords[1] - self.centerCoords[1])**2)
        for y, row in enumerate(self.bedList):
            for x, bed in enumerate(row):
                dist = sqrt((bed.centerCoords[0] - self.centerCoords[0])**2 + (bed.centerCoords[1] - self.centerCoords[1])**2)
                if dist < closestDist:
                    closest = self.bedList[y][x]
                    closestDist = dist
        return closest

    def act(self) -> None:
        self.cooldown -= 1
        if self.cooldown <= 0:
            if input_pressed(water_keys):
                self.cooldown = actionCooldown
                self.lastAction = 0
                self.closestBed.water()
            elif input_pressed(plant_keys):
                self.cooldown = actionCooldown
                self.lastAction = 1
                self.closestBed.plant()
            elif input_pressed(bonk_keys):
                self.cooldown = actionCooldown
                self.lastAction = 2
                self.closestBed.bonk()
        print("act",self.lastAction,self.cooldown)

    def draw(self) -> None:
        if self.cooldown > 0:
            if self.lastAction == 0:
                personWaterSprite.draw(self.x, self.y)
            elif self.lastAction == 1:
                personPlantSprite.draw(self.x, self.y)
            elif self.lastAction == 2:
                personBonkSprite.draw(self.x, self.y)
        else:
            if self.direction == 0:
                personStandFrontSprite.draw(self.x, self.y)
            elif self.direction == 3:
                personStandBackSprite.draw(self.x, self.y)
            elif self.direction == 1:
                personLeftSprite.draw(self.x, self.y)
            elif self.direction == 2:
                personRightSprite.draw(self.x, self.y)
                


class App:
    def __init__(self):
        pyxel.init(field_x, field_y + bottom_bar_height, title="Nuit du c0de 2022")
        pyxel.load("GrowyGardens.pyxres")
        self.startFrame = 0
        self.bedList = [
            [
                Bed(
                    (x+1) * path_size + x * dryBedSprite.sheetW,
                    (y+1) * path_size + y * dryBedSprite.sheetH
                ) for x in range(bed_row_size)
            ] for y in range(bed_column_size)
        ]
        self.player = Player(self.bedList)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        for row in self.bedList:
            for bed in row:
                bed.age()
        clockState=int()
        if clockState==0:
            pass #draw clockFirstSprite
        if clockState==1:
            pass #draw clockSecondSprite 
        if clockState==2:
            pass #draw clockThirdSprite
        if clockState==3:
            pass #draw clockFourthSprite



        self.player.move()
        self.player.act()

    def draw(self) -> None:
        pyxel.cls(3)
        pyxel.bltm(0,0,0,0,0,128,128) # draw the tilemap

        for row in self.bedList:
            for bed in row:
                bed.draw()

        for row in self.bedList:
            for bed in row:
                bed.drawLandedCrow()

        self.player.draw()

        for row in self.bedList:
            for bed in row:
                bed.drawFlyingCrow()


game = App()
