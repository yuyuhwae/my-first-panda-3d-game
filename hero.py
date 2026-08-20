class Hero():
    def __init__(self,pos,land):
	  # create the land = land property


        self.land = land
        self.mode = True
    # create a hero property and load the model
        self.hero = loader.loadModel('panda')
    # set the color for the hero
        #self.hero.setColor(1, 0.5, 0)    
    # set the size for the hero
        self.hero.setScale(0.1)
    # set the position for the hero
        self.hero.setPos(pos)
    # set the parent render node
        self.hero.reparentTo(render)
        self.cameraBind() # run camera everytime we staart the game
        self.accept_events()

# Camera settings
    def cameraBind(self):
        # disable camera control using the mouse
        base.disableMouse()
        base.camera.setH(180)
        # bind the camera to the self.hero object node
        base.camera.reparentTo(self.hero)
        # set the camera at the given coordinates
        base.camera.setPos(0, -1, 6)
        self.cameraOn = True

    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def changeMode(self):
        if self.mode == True:
            self.mode = False
        else:
            self.mode = True


    # ROTATION
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        # returns the coordinates which thero at the point (x, y)
        # moves to if they step towards angle

        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from

    def check_dir(self, angle):
        if angle >= 0 and angle <= 20:
            return(0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return(1, 0)
        elif angle <= 155:
            return(1, 1)
        elif angle <= 200:
            return(0, 1)
        elif angle <= 245:
            return(-1, 1)
        elif angle <= 290:
            return(-1, 0)
        elif angle <= 335:
            return(-1, -1)
        else:
            return (0, -1)

#Algorithm for handling movement in Spectator Mode
    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)

#Algorithm for handling movement in Main Game Mode
    def try_move(self, angle):
        pos = self.look_at(angle)
        # algorithm for handling movement
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.landd.isEmpty(pos):
                self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)

# Movement
    def forward(self):
        angle = (self.hero.getH()) % 360
        self.move_to(angle)

    def back(self):
        angle = (self.hero.getH() + 180) % 360
        self.move_to(angle)

    def left(self):
        angle = (self.hero.getH() + 90) % 360
        self.move_to(angle)

    def right(self):
        angle = (self.hero.getH() + 270) % 360
        self.move_to(angle)

    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ() + 1)

    def down(self):
        if self.mode and self.hero.getZ() > 1:
            self.hero.setZ(self.hero.getZ() - 1)

# Hero action
    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos)
        else:
            self.land.buildBlock(pos)

    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.delBlock(pos)
        else:
            self.land.delBlockfrom(pos)


    def accept_events(self):
        base.accept('c', self.changeView)
        base.accept('z', self.changeMode)
        base.accept('m', self.turn_right)
        base.accept('m' + '-repeat', self.turn_right)
        base.accept('n', self.turn_left)
        base.accept('n' + '-repeat', self.turn_left)

        base.accept('w', self.forward)
        base.accept('w' + '-repeat', self.forward)
        base.accept('a', self.left)
        base.accept('a' + '-repeat', self.left)
        base.accept('s', self.back)
        base.accept('s' + '-repeat', self.back)
        base.accept('d', self.right)
        base.accept('d' + '-repeat', self.right)

        base.accept('e', self.up)
        base.accept('e' + '-repeat', self.up)
        base.accept('q', self.down)
        base.accept('q' + '-repeat', self.down)

        base.accept('b', self.build)
        base.accept('x', self.destroy)
