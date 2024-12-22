import pygame
from levelData import levels
from collections import Counter

pygame.init()

class Mouse():
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.direction = 3
  def addPos(self,a,b):
    if len(a) != len(b):
      raise ValueError('Both lists must be the same length.')
    return tuple(a[i]+b[i] for i in range(len(a)))
  def checkPos(self,pos):
    if pos[0] < 0 or pos[0] >= levels[currentLevel].width:
      return False
    if pos[1] < 0 or pos[1] >= levels[currentLevel].height:
      return False
    if levels[currentLevel].data[pos[1]][pos[0]] == 0:
      return False
    return True
  def move(self,direction):
    global cheese
    self.direction = direction
    do = directionOffsets[direction]
    newPos = self.addPos([self.x,self.y],do)
    if not self.checkPos(newPos):
      return
    if newPos in cheese:
      newnewPos = self.addPos(newPos,do)
      if not self.checkPos(newnewPos) or newnewPos in cheese:
        return
      cheese[cheese.index(newPos)] = newnewPos
    [self.x,self.y] = newPos
  def setPos(self,pos):
    self.x = pos[0]
    self.y = pos[1]
    self.direction = 3

class Text():
  def __init__(self, text, pos, size, color):
    self.text = text
    self.pos = pos
    self.size = size
    self.color = color
    self.font = pygame.font.Font('assets/font.ttf', size)
    self.render = self.font.render(self.text, True, self.color)
    self.rect = self.render.get_rect()
    self.rect.center = self.pos
  def draw(self):
    screen.blit(self.render, self.rect)

screen = pygame.display.set_mode((400, 400))
icon = pygame.image.load("assets/icon.png")
pygame.display.set_caption("Cheese Terminator")
pygame.display.set_icon(icon)

currentLevel = 0
endLevel = 4
paused = 1
mouse = Mouse(0,0)
cheese = []
goals = []
directionOffsets = [[0,-1],[0,1],[-1,0],[1,0]]
movementKeys = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]
blockSize = 30

textColour = (255,255,0)
black = (0,0,0)
floor = (192,192,192)
wallA = (255,255,255)
wallB = (128,128,128)

mouseBase = pygame.image.load("assets/images/mouse.png")
mouseUp = mouseBase.subsurface((0,270,30,30))
mouseDown = mouseBase.subsurface((0,90,30,30))
mouseLeft = mouseBase.subsurface((0,180,30,30))
mouseRight = mouseBase.subsurface((0,0,30,30))
cheeseBase = pygame.image.load("assets/images/cheese.png")
cheeseWhole = cheeseBase.subsurface((0,30,30,30))
cheeseSlice = cheeseBase.subsurface((0,0,30,30))
targetBase = pygame.image.load("assets/images/goal.png")
targetRed = targetBase.subsurface((0,0,30,30))
targetBlue = targetBase.subsurface((0,30,30,30))

start1 = Text("Cheese Terminator", (200, (200-30)), 32, textColour)
start2 = Text("Press Enter To Start", (200, (200-3)), 20, textColour)
start3 = Text("Use Arrow Keys To Move", (200, (200+18)), 20, textColour)
next1 = Text("Well Done!", (200, (200-15)), 32, textColour)
next2 = Text("Press Enter To Continue", (200, (200+15)), 20, textColour)
win1 = Text("You Won!!! :D", (200, (200-15)), 32, textColour)
win2 = Text("Press Enter To Play Again", (200, (200+15)), 20, textColour)
reset1 = Text("Restart The Level?", (200, (200-30)), 32, textColour)
reset2 = Text("Press Enter To Restart", (200, (200-3)), 20, textColour)
reset3 = Text("Press Any Arrow Key To Cancel", (200, (200+18)), 20, textColour)

def setScreenSize(w,h):
  global screen
  screen = pygame.display.set_mode((w,h))

def updateLevel():
  global cheese, goals
  level = levels[currentLevel]
  pygame.display.set_caption("Cheese Terminator - Level "+str(currentLevel+1))
  setScreenSize(level.width*blockSize,level.height*blockSize)
  cheese = level.cheese.copy()
  goals = level.goals.copy()
  mouse.setPos(level.mouse)

def checkWon():
  return Counter(tuple(cheese)) == Counter(goals)

def drawLevel():
  if paused > 0:
    return
  level = levels[currentLevel]
  screen.fill(floor)
  for y in range(level.height):
    for x in range(level.width):
      if level.data[y][x] == 0:
        for offset in directionOffsets:
          if mouse.checkPos(mouse.addPos([x,y],offset)):
            if offset == directionOffsets[0]:
              pygame.draw.line(screen,wallA,(x*blockSize,y*blockSize),(x*blockSize+blockSize,y*blockSize),2)
            elif offset == directionOffsets[1]:
              pygame.draw.line(screen,wallB,(x*blockSize,y*blockSize+blockSize-2),(x*blockSize+blockSize,y*blockSize+blockSize-2),2)
            elif offset == directionOffsets[2]:
              pygame.draw.line(screen,wallA,(x*blockSize,y*blockSize),(x*blockSize,y*blockSize+blockSize),2)
            else:
              pygame.draw.line(screen,wallB,(x*blockSize+blockSize-2,y*blockSize),(x*blockSize+blockSize-2,y*blockSize+blockSize),2)
      else:
        pygame.draw.rect(screen,floor,(x*blockSize,y*blockSize,blockSize,blockSize))
      cheeseGoal = 0
      if (x,y) in cheese:
        cheeseGoal += 1
      if (x,y) in goals:
        cheeseGoal += 2
      
      if cheeseGoal == 1:
        screen.blit(cheeseWhole,(x*blockSize,y*blockSize))
      elif cheeseGoal == 2:
        screen.blit(targetRed,(x*blockSize,y*blockSize))
      elif cheeseGoal == 3:
        screen.blit(cheeseSlice,(x*blockSize,y*blockSize))
      
      if (x,y) == (mouse.x,mouse.y):
        mousedir = mouse.direction
        if mousedir == 0:
          screen.blit(mouseUp,(x*blockSize,y*blockSize))
        elif mousedir == 1:
          screen.blit(mouseDown,(x*blockSize,y*blockSize))
        elif mousedir == 2:
          screen.blit(mouseLeft,(x*blockSize,y*blockSize))
        else:
          screen.blit(mouseRight,(x*blockSize,y*blockSize))

def drawPause():
  if paused == 0:
    return
  screen = pygame.display.set_mode((400,400))
  screen.fill(black)
  if paused == 1:
    start1.draw()
    start2.draw()
    start3.draw()
  elif paused == 2:
    reset1.draw()
    reset2.draw()
    reset3.draw()
  elif paused == 3:
    next1.draw()
    next2.draw()
  elif paused == 4:
    win1.draw()
    win2.draw()

drawPause()
pygame.display.update()
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    if event.type == pygame.KEYDOWN:
      if paused in [0,2] and event.key in movementKeys:
        if paused == 2:
          paused = 0
          setScreenSize(levels[currentLevel].width,levels[currentLevel].height)
        else:
          mouse.move(movementKeys.index(event.key))
      if event.key == pygame.K_RETURN:
        if paused > 0:
          if paused != 4:
            paused = 0
            updateLevel()
          else:
            exit()
        else:
          paused = 2
          drawPause()
    if checkWon() and paused == 0:
      currentLevel += 1
      if currentLevel == endLevel:
        paused = 4
      else:
        paused = 3
      drawPause()
    drawLevel()
    pygame.display.update()