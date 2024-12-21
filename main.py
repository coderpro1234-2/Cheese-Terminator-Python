import pygame
#Import all of the level data
from gamedata import *
#Start
pygame.init()
#Position/Game variables
DEBUG = False
WIDTH = 400
HEIGHT = 400
cheeselist = []
endlist = []
mousepos = 0
mousedir = 3
levelwidth = 0
levelheight = 0
mouseOffsets = [-levelwidth,levelwidth,-1,1]
blocksize = 30
gamelist = []
level = 1
maxLevel = 50
emptyblock = [1,2,3,4,5]
paused = True
start = True
reset = False
end = False
#Colo(u)r variables
yellow = (255,255,0)
black = (0,0,0)
floor = (192,192,192)
wall1 = (255,255,255)
wall2 = (128,128,128)
#Loop variables
running = True
#Screen variables
screen = pygame.display.set_mode((WIDTH,HEIGHT))
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
icon = pygame.image.load("assets/icon.png")
#Screen display
pygame.display.set_caption("Cheese Terminator")
pygame.display.set_icon(icon)
pygame.display.update()
#Classes
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
#Text
start1 = Text("Cheese Terminator", (WIDTH // 2, ((HEIGHT // 2)-30)), 32, yellow)
start2 = Text("Press Enter To Start", (WIDTH // 2, ((HEIGHT // 2)-3)), 20, yellow)
start3 = Text("Use Arrow Keys To Move", (WIDTH // 2, ((HEIGHT // 2)+18)), 20, yellow)
next1 = Text("Well Done!", (WIDTH // 2, ((HEIGHT // 2)-15)), 32, yellow)
next2 = Text("Press Enter To Continue", (WIDTH // 2, ((HEIGHT // 2)+15)), 20, yellow)
win1 = Text("You Won!!! :D", (WIDTH // 2, ((HEIGHT // 2)-15)), 32, yellow)
win2 = Text("Press Enter To Play Again", (WIDTH // 2, ((HEIGHT // 2)+15)), 20, yellow)
reset1 = Text("Restart The Level?", (WIDTH // 2, ((HEIGHT // 2)-30)), 32, yellow)
reset2 = Text("Press Enter To Restart", (WIDTH // 2, ((HEIGHT // 2)-3)), 20, yellow)
reset3 = Text("Press Any Arrow Key To Cancel", (WIDTH // 2, ((HEIGHT // 2)+18)), 20, yellow)
#Functions
def updateLevel(lvl):
  global endlist, cheeselist, mousepos, screen, levelwidth, levelheight, gamelist, mousedir, mouseOffsets
  pygame.display.set_caption("Cheese Terminator - Level "+str(ldv.index(lvl)+1))
  level = lvl[1:]
  endlist = []
  cheeselist = []
  drawid = 0
  mousedir = 3
  width = lvl[0]
  height = len(level) / width
  if height % 1 != 0:
    raise ValueError("Invalid level data")
  else:
    height = int(height)
  if DEBUG:
    print(f'Level: {str(ldv.index(lvl)+1)}, Width: {width}, Height: {height}')
  screen = pygame.display.set_mode((round(width*blocksize),round(height*blocksize)))
  levelwidth = width
  levelheight = height
  mouseOffsets = [-levelwidth,levelwidth,-1,1]
  for _ in range(levelheight):
    for _ in range(levelwidth):
      if level[drawid] == 2:
        endlist.append(drawid)
      elif level[drawid] == 3:
        cheeselist.append(drawid)
      elif level[drawid] == 4:
        mousepos = drawid
      elif level[drawid] == 5:
        cheeselist.append(drawid)
        endlist.append(drawid)
      drawid = drawid + 1
  gamelist = level
def drawScreen():
  if paused:
    return
  drawid = 0
  for drawy in range(levelheight):
    drawx = 0
    for drawx in range(levelwidth):
      if gamelist[drawid] == 0:
        pygame.draw.rect(screen,floor,(drawx*blocksize,drawy*blocksize,blocksize,blocksize))
        for offset in mouseOffsets:
          if isLegalOffset(drawid,offset):
            if offset == -levelwidth:
              pygame.draw.line(screen,wall1,(drawx*blocksize,drawy*blocksize),(drawx*blocksize+blocksize,drawy*blocksize),2)
            elif offset == levelwidth:
              pygame.draw.line(screen,wall2,(drawx*blocksize,drawy*blocksize+blocksize-2),(drawx*blocksize+blocksize,drawy*blocksize+blocksize-2),2)
            elif offset == -1:
              pygame.draw.line(screen,wall1,(drawx*blocksize,drawy*blocksize),(drawx*blocksize,drawy*blocksize+blocksize),2)
            else:
              pygame.draw.line(screen,wall2,(drawx*blocksize+blocksize-2,drawy*blocksize),(drawx*blocksize+blocksize-2,drawy*blocksize+blocksize),2)
      else:
        pygame.draw.rect(screen,floor,(drawx*blocksize,drawy*blocksize,blocksize,blocksize))
      if drawid in cheeselist:
        if drawid in endlist:
          screen.blit(cheeseSlice,(drawx*blocksize,drawy*blocksize))
        else:
          screen.blit(cheeseWhole,(drawx*blocksize,drawy*blocksize))
      elif drawid in endlist:
        screen.blit(targetRed,(drawx*blocksize,drawy*blocksize))
      if mousepos == drawid:
        if mousedir == 0:
          screen.blit(mouseUp,(drawx*blocksize,drawy*blocksize))
        elif mousedir == 1:
          screen.blit(mouseDown,(drawx*blocksize,drawy*blocksize))
        elif mousedir == 2:
          screen.blit(mouseLeft,(drawx*blocksize,drawy*blocksize))
        else:
          screen.blit(mouseRight,(drawx*blocksize,drawy*blocksize))
      drawid = drawid + 1
def drawPause(nextlevel=False):
  if not paused:
    return
  screen = pygame.display.set_mode((400,400))
  screen.fill(black)
  if nextlevel:
    next1.draw()
    next2.draw()
  elif start:
    start1.draw()
    start2.draw()
    start3.draw()
  elif reset:
    reset1.draw()
    reset2.draw()
    reset3.draw()
  elif end:
    win1.draw()
    win2.draw()
def isLegalOffset(pos,off,checkWall=True):
  newpos = pos+off
  if abs(off) == levelwidth:
    if newpos < 0 or newpos >= len(gamelist):
      return False
  elif off == -1:
    if newpos+1 % levelwidth == 0:
      return False
  elif off == 1:
    if newpos % levelwidth == 0:
      return False
  if gamelist[newpos] == 0 and checkWall:
    return False
  return True
def checkBlock(pos,dir):
  if not isLegalOffset(pos,mouseOffsets[dir]):
    return 0
  if pos+mouseOffsets[dir] in cheeselist:
    if isLegalOffset(pos,mouseOffsets[dir]*2):
      if pos+(mouseOffsets[dir]*2) in cheeselist or gamelist[pos+(mouseOffsets[dir]*2)] == 0:
        return 0
      return 2
    return 0
  return 1
def checkWon():
  q = 0
  a = 0
  while q < len(endlist):
    if endlist[q] in cheeselist:
      a = a + 1
    q = q + 1
  return a == q
#Main loop
drawPause()
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        if start or end:
          pass
        elif reset:
          reset = False
          paused = False
          screen = pygame.display.set_mode((levelwidth*blocksize,levelheight*blocksize))
        else:
          mousedir = 0
          offset = mouseOffsets[mousedir]
          blocked = checkBlock(mousepos,mousedir)
          if blocked > 0:
            mousepos = mousepos+offset
            if blocked == 2:
              cheeselist[cheeselist.index(mousepos)] += offset
      if event.key == pygame.K_DOWN:
        if start or end:
          pass
        elif reset:
          reset = False
          paused = False
          screen = pygame.display.set_mode((levelwidth*blocksize,levelheight*blocksize))
        else:
          mousedir = 1
          offset = mouseOffsets[mousedir]
          blocked = checkBlock(mousepos,mousedir)
          if blocked > 0:
            mousepos = mousepos+offset
            if blocked == 2:
              cheeselist[cheeselist.index(mousepos)] += offset
      if event.key == pygame.K_LEFT:
        if start or end:
          pass
        elif reset:
          reset = False
          paused = False
          screen = pygame.display.set_mode((levelwidth*blocksize,levelheight*blocksize))
        else:
          mousedir = 2
          offset = mouseOffsets[mousedir]
          blocked = checkBlock(mousepos,mousedir)
          if blocked > 0:
            mousepos = mousepos+offset
            if blocked == 2:
              cheeselist[cheeselist.index(mousepos)] += offset
      if event.key == pygame.K_RIGHT:
        if start or end:
          pass
        elif reset:
          reset = False
          paused = False
          screen = pygame.display.set_mode((levelwidth*blocksize,levelheight*blocksize))
        else:
          mousedir = 3
          offset = mouseOffsets[mousedir]
          blocked = checkBlock(mousepos,mousedir)
          if blocked > 0:
            mousepos = mousepos+offset
            if blocked == 2:
              cheeselist[cheeselist.index(mousepos)] += offset
      if event.key == pygame.K_RETURN:
        if paused:
          if start:
            paused = False
            start = False
            updateLevel(lvldict[level])
          if reset:
            reset = False
            paused = False
            updateLevel(lvldict[level])
          if end:
            running = False
            exit()
        else:
          reset = True
          paused = True
          drawPause()
          
      if event.key == pygame.K_SPACE and (not paused) and DEBUG:
        level += 1
        updateLevel(lvldict[level])
      if checkWon() and (not paused):
        if level == maxLevel:
          paused = True
          end = True
          drawPause()
        else:
          paused = True
          reset = True
          level += 1
          drawPause(True)
    WIDTH,HEIGHT = screen.get_size()
    drawScreen()
    pygame.display.update()