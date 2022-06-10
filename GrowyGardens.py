import pyxel

class Bed:
    pass

class Player:
    pass

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