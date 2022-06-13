from typing import List
import pyxel
from random import randint
from math import sqrt

"""
Bienvenue dans notre jardin en pleine croissance : Growy Gardens! L'objectif du jeu est de faire pousser 
le plus de plantes possible en 3 minutes en les plantant rapidement et en assommant les corbeaux qui ont 
faim! Vous pouvez suivre votre score en bas à gauche. Pour vous déplacer utilisez les touches WASD ou les 
flèches. Vous pouvez effectuer trois actions : arroser une plante en appuyant sur la touche 1 ou J, planter 
des graines en appuyant sur la touche 2 ou K, et assommer un corbeau avec la touche 3 ou L. Quand les bacs a 
plantes sont sèches vous devez les arroser pour que votre plante puisse grandir. Une fois que la plante a grandi, 
courrez dessus pour la prendre et regardez votre score augmenter. Bonne chance!

"""

# Key bindings
UP_KEYS = [pyxel.KEY_UP, pyxel.KEY_W]
DOWN_KEYS = [pyxel.KEY_DOWN, pyxel.KEY_S]
LEFT_KEYS = [pyxel.KEY_LEFT, pyxel.KEY_A]
RIGHT_KEYS = [pyxel.KEY_RIGHT, pyxel.KEY_D]

WATER_KEYS = [pyxel.KEY_1, pyxel.KEY_J]
PLANT_KEYS = [pyxel.KEY_2, pyxel.KEY_K]
BONK_KEYS = [pyxel.KEY_3, pyxel.KEY_L]


def input_pressed(key_list):
    for k in key_list:
        if pyxel.btn(k):
            return True
    return False


FIELD_X = 128
FIELD_Y = 120
BOTTOM_BAR_HEIGHT = 8
PATH_SIZE = 8
BED_ROW_SIZE = 5
BED_COLUMN_SIZE = 5
DIAG_SPEED_COEF = 0.707 # Aprox cos(45 degrees), and is what each axis of speed should be multiplied by if the player is moving in 2 axes at once

# Balance Variables
GAME_DURATION = 3 * 60 * 30
PLAYER_SPEED = 2.2

MIN_PLANT_AGE = 10 * 30
MAX_PLANT_AGE = 20 * 30
MIN_PLANT_AGE = 5 * 30
MAX_PLANT_AGE = 17 * 30

CROW_EAT_TIME = 3 * 30
CROW_CHANCE = 0.3
ACTION_COOLDOWN = 0.2 * 30
COLLECT_COOLDOWN = 15  # Number of frames after growing before smth can be collected

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


CAN_ICON_SPRITE = Sprite(48, 96, 8, 8)
BAT_ICON_SPRITE = Sprite(56, 96, 8, 8)
SEED_BAG_ICON_SPRITE = Sprite(48, 104, 8, 8)
COIN_ICON_SPRITE = Sprite(56, 104, 8, 8)
CLOCK_FIRST_SPRITE = Sprite(48, 112, 16, 8, 7)
CLOCK_SECOND_SPRITE = Sprite(48, 120, 16, 8, 7)
CLOCK_THIRD_SPRITE = Sprite(48, 128, 16, 8, 7)
CLOCK_FOURTH_SPRITE = Sprite(48, 136, 16, 8, 7)
DRY_BED_SPRITE = Sprite(32, 128, 16, 16)
WET_BED_SPRITE = Sprite(32, 144, 16, 16)
CROW_SPRITE = Sprite(0, 160, 16, 16, 7)
CROW_FLY_SPRITE = Sprite(16, 160, 16, 16, 7)

PERSON_STAND_FRONT_SPRITE = Sprite(32, 0, 16, 30)
PERSON_STAND_BACK_SPRITE = Sprite(48, 0, 16, 30)
PERSON_LEFT_SPRITE = Sprite(48, 32, 16, 30)
PERSON_RIGHT_SPRITE = Sprite(32, 32, 16, 30)
PERSON_BONK_SPRITE = Sprite(32, 64, 16, 30)
PERSON_WATER_SPRITE = Sprite(48, 64, 16, 30)
PERSON_PLANT_SPRITE = Sprite(32, 96, 16, 30)

PLANT_NAMES = ["pinkFlower", "blueFlower", "yellowFlower",
              "tomato", "blueberry", "lettuce", "carrot", "mushroom"]
PLANT_POINTS = {"pinkFlower": 30, "blueFlower": 10, "yellowFlower": 15,
               "tomato": 5, "lettuce": 5, "carrot": 10, "blueberry": 15, "mushroom": 25}

PLANT_SPRITES = {
    "pinkFlower": PlantSprite(
        Sprite(16, 0, 16, 16),
        Sprite(0, 176, 16, 16),
        Sprite(0, 0, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "blueFlower": PlantSprite(
        Sprite(16, 16, 16, 16),
        Sprite(16, 176, 16, 16),
        Sprite(0, 16, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "yellowFlower": PlantSprite(
        Sprite(16, 32, 16, 16),
        Sprite(32, 176, 16, 16),
        Sprite(0, 32, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "tomato": PlantSprite(
        Sprite(16, 48, 16, 16),
        Sprite(16, 192, 16, 16),
        Sprite(0, 48, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "blueberry": PlantSprite(
        Sprite(16, 64, 16, 16),
        Sprite(32, 192, 16, 16),
        Sprite(0, 64, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "lettuce": PlantSprite(
        Sprite(16, 80, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 80, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "carrot": PlantSprite(
        Sprite(16, 96, 16, 16),
        Sprite(0, 144, 16, 16),
        Sprite(0, 96, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "mushroom": PlantSprite(
        Sprite(16, 112, 16, 16),
        Sprite(0, 192, 16, 16),
        Sprite(0, 112, 16, 16),
        Sprite(16, 144, 16, 16),
    ),
    "Empty": PlantSprite(
        Sprite(0, 0, 0, 0),
        Sprite(0, 0, 0, 0),
        Sprite(0, 0, 0, 0),
        Sprite(0, 0, 0, 0),
    )
}


class Crow:
    def __init__(self, targetX: int, targetY: int):
        self.movesToGo = 60  # frames
        self.targetX = targetX
        self.targetY = targetY
        self.arrived = False
        self.onWayBack = False
        self.clock = CROW_EAT_TIME
        self.atePlant = False
        edge = randint(0, 3)  # 0 bottom, 1 left, 2 top, 3 right
        if edge == 0:
            self.x = randint(0, 127)
            self.y = 127 + CROW_SPRITE.sheetH
        elif edge == 1:
            self.x = 0 - CROW_SPRITE.sheetW
            self.y = randint(0, 127)
        elif edge == 2:
            self.x = randint(0, 127)
            self.y = 0 - CROW_SPRITE.sheetH
        elif edge == 3:
            self.x = 127 + CROW_SPRITE.sheetW
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
                    self.targetY = 127 + CROW_SPRITE.sheetH
                elif edge == 1:
                    self.targetX = 0 - CROW_SPRITE.sheetW
                    self.targetY = randint(0, 127)
                elif edge == 2:
                    self.targetX = randint(0, 127)
                    self.targetY = 0 - CROW_SPRITE.sheetH
                elif edge == 3:
                    self.targetX = 127 + CROW_SPRITE.sheetW
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
                self.targetY = 127 + CROW_SPRITE.sheetH
            elif edge == 1:
                self.targetX = 0 - CROW_SPRITE.sheetW
                self.targetY = randint(0, 127)
            elif edge == 2:
                self.targetX = randint(0, 127)
                self.targetY = 0 - CROW_SPRITE.sheetH
            elif edge == 3:
                self.targetX = 127 + CROW_SPRITE.sheetW
                self.targetY = randint(0, 127)

    def draw(self) -> None:
        if self.arrived:
            CROW_SPRITE.draw(self.x, self.y)
        else:
            CROW_FLY_SPRITE.draw(self.x, self.y)


class Bed:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.isDead = False
        self.isPopulated = False
        self.isWatered = False
        self.plantType = "Empty"
        self.plantAge = 0
        self.maturityAge = 1
        self.waterLeft = 0
        self.timeUntilCrow = 1
        self.crow = None
        self.hasCrowSpawned = False
        self.state = 0  # n = 0 for seed, n = 1 for sprout, n = 2 for grown
        self.centerCoords = (self.x + DRY_BED_SPRITE.sheetW / 2,
                             self.y + DRY_BED_SPRITE.sheetH / 2)
        self.readyTime = 0

    def draw(self) -> None:
        if self.isWatered:
            WET_BED_SPRITE.draw(self.x, self.y)
        else:
            DRY_BED_SPRITE.draw(self.x, self.y)
        if self.isPopulated or self.isDead:
            try:
                sprite = PLANT_SPRITES[self.plantType]
                sprite.draw(self.x, self.y, self.state)
            except:
                print("Error getting plant sprite", self.isDead,
                      self.isPopulated, self.isWatered, self.state)

    def drawLandedCrow(self) -> None:
        if type(self.crow) == Crow and self.crow.arrived:
            self.crow.draw()

    def drawFlyingCrow(self) -> None:
        if type(self.crow) == Crow and not self.crow.arrived:
            self.crow.draw()

    def water(self) -> None:
        if not self.isDead:
            self.waterLeft = randint(MIN_PLANT_AGE, MAX_PLANT_AGE)
            self.isWatered = True

    def plant(self) -> None:
        if not self.isPopulated:
            type = PLANT_NAMES[randint(0, len(PLANT_NAMES)-1)]
            self.isPopulated = True
            self.plantType = type
            self.plantAge = 0
            self.maturityAge = randint(MIN_PLANT_AGE, MAX_PLANT_AGE)
            self.timeUntilCrow = randint(
                30, int(self.maturityAge * (1/CROW_CHANCE)))
            self.hasCrowSpawned = False
            self.readyTime = 0

    def bonk(self) -> None:
        if type(self.crow) == Crow:
            self.crow.shoo()

    def collect(self) -> int:
        if self.isPopulated and self.plantAge >= self.maturityAge and not self.isDead and self.readyTime + COLLECT_COOLDOWN <= pyxel.frame_count:
            pointsToGive = PLANT_POINTS[self.plantType]

            self.isPopulated = False
            self.plantType = "Empty"
            self.maturityAge = 0
            self.state = 0
            self.bonk()

            pyxel.play(0, 3)
            return pointsToGive
        return 0

    def age(self):

        # If crow is present then update it
        if type(self.crow) == Crow:
            self.crow.update()
            if self.crow.atePlant == True:
                self.isDead = True
                self.isPopulated = False
                self.state = 3

                self.isWatered = False
                self.waterLeft = 0

                # Play death music
                pyxel.play(0, 2)

                self.crow.atePlant = False # Reset it

            if self.crow.arrived and self.crow.onWayBack:
                self.crow = True  # Crow is gone

        if not self.isDead:
            if self.isPopulated and self.isWatered:
                self.plantAge += 1
                self.timeUntilCrow -= 1
                self.waterLeft -= 1

            if self.waterLeft <= 0:
                self.isWatered = False

            if self.timeUntilCrow == 0 and self.crow == None and self.hasCrowSpawned == False:
                self.crow = Crow(self.x, self.y)
                self.timeUntilCrow = -1
                self.hasCrowSpawned = True

            if self.plantAge >= self.maturityAge:
                if self.state != 2:
                    self.readyTime = pyxel.frame_count
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
    def __init__(self, bedList: List[List[Bed]]):
        self.x = 0
        self.y = 0
        self.speed = PLAYER_SPEED
        self.cooldown = 0
        self.direction = 0  # 0 down, 1 left, 2 right, 3 up, for sprite drawing
        self.lastAction = 0  # 0 water, 1 plant, 2 bonk, also for drawing
        self.bedList = bedList
        self.centerCoords = (self.x + PERSON_STAND_FRONT_SPRITE.sheetW / 2,
                             self.y + PERSON_STAND_FRONT_SPRITE.sheetH / 2)
        self.closestBed = self.computeClosestBed()

    def move(self) -> int:  # Returns the number of points earned
        vertSpeed = self.speed
        horizSpeed = self.speed
        if input_pressed(LEFT_KEYS) ^ input_pressed(RIGHT_KEYS): # if moving horizontally
            vertSpeed *= DIAG_SPEED_COEF
        if input_pressed(UP_KEYS) ^ input_pressed(DOWN_KEYS):
            horizSpeed *= DIAG_SPEED_COEF
        if input_pressed(UP_KEYS):
            if self.y - vertSpeed >= 0:
                self.y -= vertSpeed
                self.direction = 3
                self.closestBed = self.computeClosestBed()
        if input_pressed(DOWN_KEYS):
            if self.y + vertSpeed < FIELD_Y - PERSON_STAND_FRONT_SPRITE.sheetH:
                self.y += vertSpeed
                self.direction = 0
                self.closestBed = self.computeClosestBed()
        if input_pressed(LEFT_KEYS):
            if self.x - horizSpeed >= 0:
                self.x -= horizSpeed
                self.direction = 1
                self.closestBed = self.computeClosestBed()
        if input_pressed(RIGHT_KEYS):
            if self.x + horizSpeed < FIELD_X - PERSON_STAND_FRONT_SPRITE.sheetW:
                self.x += horizSpeed
                self.direction = 2
                self.closestBed = self.computeClosestBed()
        return self.closestBed.collect()

    def computeClosestBed(self) -> Bed:
        self.centerCoords = (self.x + PERSON_STAND_FRONT_SPRITE.sheetW / 2,
                             self.y + PERSON_STAND_FRONT_SPRITE.sheetH / 2)
        closest = self.bedList[0][0]
        closestDist = sqrt((closest.centerCoords[0] - self.centerCoords[0])**2 + (
            closest.centerCoords[1] - self.centerCoords[1])**2)
        for y, row in enumerate(self.bedList):
            for x, bed in enumerate(row):
                dist = sqrt((bed.centerCoords[0] - self.centerCoords[0])
                            ** 2 + (bed.centerCoords[1] - self.centerCoords[1])**2)
                if dist < closestDist:
                    closest = self.bedList[y][x]
                    closestDist = dist
        return closest

    def act(self) -> None:
        self.cooldown -= 1
        if self.cooldown <= 0:
            if input_pressed(WATER_KEYS):
                self.cooldown = ACTION_COOLDOWN
                self.lastAction = 0
                self.closestBed.water()
            elif input_pressed(PLANT_KEYS):
                self.cooldown = ACTION_COOLDOWN
                self.lastAction = 1
                self.closestBed.plant()
            elif input_pressed(BONK_KEYS):
                self.cooldown = ACTION_COOLDOWN
                self.lastAction = 2
                self.closestBed.bonk()
        # print("act",self.lastAction,self.cooldown)

    def draw(self) -> None:
        if self.cooldown > 0:
            if self.lastAction == 0:
                PERSON_WATER_SPRITE.draw(self.x, self.y)
            elif self.lastAction == 1:
                PERSON_PLANT_SPRITE.draw(self.x, self.y)
            elif self.lastAction == 2:
                PERSON_BONK_SPRITE.draw(self.x, self.y)
        else:
            if self.direction == 0:
                PERSON_STAND_FRONT_SPRITE.draw(self.x, self.y)
            elif self.direction == 3:
                PERSON_STAND_BACK_SPRITE.draw(self.x, self.y)
            elif self.direction == 1:
                PERSON_LEFT_SPRITE.draw(self.x, self.y)
            elif self.direction == 2:
                PERSON_RIGHT_SPRITE.draw(self.x, self.y)


class App:
    def __init__(self):
        pyxel.init(FIELD_X, FIELD_Y + BOTTOM_BAR_HEIGHT, title="Growy Gardens")
        pyxel.load("GrowyGardens.pyxres")
        self.startFrame = float("inf")
        self.points = 0
        self.gameOver = False
        self.gameStarted = False

        self.bedList = [
            [
                Bed(
                    (x+1) * PATH_SIZE + x * DRY_BED_SPRITE.sheetW,
                    (y+1) * PATH_SIZE + y * DRY_BED_SPRITE.sheetH
                ) for x in range(BED_ROW_SIZE)
            ] for y in range(BED_COLUMN_SIZE)
        ]
        self.player = Player(self.bedList)

        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        if not self.gameStarted:
            if input_pressed(WATER_KEYS):
                self.gameStarted = True
                self.startFrame = pyxel.frame_count
        if not self.gameOver and self.gameStarted:
            if pyxel.frame_count - self.startFrame >= GAME_DURATION:
                self.gameOver = True
            for row in self.bedList:
                for bed in row:
                    bed.age()
            self.points += self.player.move()
            self.player.act()

            self.clockState = int(((pyxel.frame_count - self.startFrame) * 4) / GAME_DURATION) % 4 # This mod is just incase anything funky happens

    def draw(self) -> None:
        if not self.gameStarted:
            pyxel.cls(3)
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            pyxel.rect(20, 20, 88, 88, 0)
            pyxel.text(43, 24, "GrowyGardens", 10)
            pyxel.text(24, 42,
                f"Bienvenue dans le\njeu GrowyGardens.\nRecoltez le plus de \nplantes possibles\nen {int(GAME_DURATION/(30 * 60))} minutes.",
            7)
            pyxel.text(24, 86, "Appuyez sur 1 pour\njouer.", 7)
        
        elif not self.gameOver and self.gameStarted:
            pyxel.cls(3)
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)  # draw the tilemap

            for row in self.bedList:
                for bed in row:
                    bed.draw()
                    bed.drawLandedCrow()

            self.player.draw()

            for row in self.bedList:
                for bed in row:
                    bed.drawFlyingCrow()

            # Draw the bottom bar

            COIN_ICON_SPRITE.draw(0, 120)
            pyxel.text(10, 121, str(self.points), col=0)

            CAN_ICON_SPRITE.draw(42, 120)
            pyxel.text(50, 121, str(1), col=0)

            SEED_BAG_ICON_SPRITE.draw(58, 120)
            pyxel.text(66, 121, str(2), col=0)

            BAT_ICON_SPRITE.draw(74, 120)
            pyxel.text(80, 121, str(3), col=0)

            # Draw clock
            if self.clockState == 0:
                CLOCK_FIRST_SPRITE.draw(112, 120)
            if self.clockState == 1:
                CLOCK_SECOND_SPRITE.draw(112, 120)
            if self.clockState == 2:
                CLOCK_THIRD_SPRITE.draw(112, 120)
            if self.clockState == 3:
                CLOCK_FOURTH_SPRITE.draw(112, 120)

        else:
            # Render game over screen
            pyxel.rect(20, 20, 88, 88, 0)
            pyxel.text(43, 24, "C'EST FINI!", 10)
            pyxel.text(
                24, 42, f"Vous avez reussi\na obtenir {self.points} points\nen {int(GAME_DURATION/30)} secondes.", 7)
            pyxel.text(
                24, 68, "Appuyez sur la touche\nEscape/Echapper pour\nquitter le jeu.", 7)


game = App()
