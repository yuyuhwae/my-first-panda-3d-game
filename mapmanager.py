#write here code for creation and controlling map

class Mapmanager():
  """ Managing map """
  def __init__(self):
    self.model = 'block' # the cube model is in the block.egg file
    # the following textures are used: 
    self.texture = 'wood.png'        
    self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ] #rgba


    # create the main map node:
    self.startNew()
    # create building blocks   
    # self.addBlock((0,10, 0))
    # self.addBlock((0,10, 2.5))
    # self.addBlock((0,10, 5))

  def startNew(self):
    """ creating a base for new map """
    self.land = render.attachNewNode("Land") # the node which all the map blocks are attached to

  def getColor(self, z):
    if z < len(self.colors):
      return self.colors[z]
    else:
      return self.colors[len(self.colors) -1]
  
  def addBlock(self, position):
    self.block = loader.loadModel(self.model)
    self.block.setTexture(loader.loadTexture(self.texture))
    self.block.setPos(position)
    self.color = self.getColor(int(position[2]))
    self.block.setColor(self.color)
    self.block.reparentTo(self.land)

  def clear(self):
    self.land.removeNode()
    self.startNew()
    
  def loadLand(self, filename):
    self.clear()
    with open(filename) as file:
      y = 0
      for line in file:
        x = 0
        line = line.split(' ')
        for z in line:
          for z0 in range(int(z)+1):
            block = self.addBlock((x, y, z0))
          x += 1
        y += 1
    #return x, y