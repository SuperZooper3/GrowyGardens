import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Draw Game Test")
        pyxel.load("test.pyxres")
        self.x = 0
        self.y = 0
        self.objectType = "s"
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_W): self.y -= 1
        if pyxel.btn(pyxel.KEY_S): self.y += 1
        if pyxel.btn(pyxel.KEY_A): self.x -= 1
        if pyxel.btn(pyxel.KEY_D): self.x += 1
        if pyxel.btn(pyxel.KEY_1): self.objectType = "s"
        if pyxel.btn(pyxel.KEY_2): self.objectType = "c"
        if pyxel.btn(pyxel.KEY_3): self.objectType = "e"


    def draw(self):
        pyxel.cls(5)

        # Draw sky
        if self.objectType == "s":
            pyxel.blt(self.x, self.y,0, 0, 0, 16, 16,colkey=0)
        elif self.objectType == "c":
            pyxel.blt(self.x, self.y,0, 8, 0, 16, 16,colkey=0)
        elif self.objectType == "e":
            pyxel.blt(self.x, self.y,0, 16, 0, 16,16,colkey=0)


App()

