#write here code for app's main window

from direct.showbase.ShowBase import ShowBase
from hero import Hero
from mapmanager import Mapmanager
 
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        x, y = self.land.loadLand('land.txt')
        self.hero = Hero((x//2, y//2, 1.5), self.land)
        base.camLens.setFov(90)
 
game = Game()
game.run()