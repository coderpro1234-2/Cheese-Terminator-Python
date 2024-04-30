import pygame
#Import all of the level data
from gamedata import *
#Start
pygame.init()
lvldict = {0:lv1,1:lv2,2:lv3,3:lv4,4:lv5,5:lv6,6:lv7,7:lv8,8:lv9,9:lv10,10:lv11,11:lv12,12:lv13,13:lv14,14:lv15,15:lv16,16:lv17,17:lv18,18:lv19,19:lv20,20:lv21,21:lv22,22:lv23,23:lv24,24:lv25,25:lv26,26:lv27,27:lv28,28:lv29,29:lv30,30:lv31,31:lv32,32:lv33,33:lv34,34:lv35,35:lv36,36:lv37,37:lv38,38:lv39,39:lv40,40:lv41,41:lv42,42:lv43,43:lv44,44:lv45,45:lv46,46:lv47,47:lv48,48:lv49,49:lv50}
ldv = list(lvldict.values())
#Position/Game variables
X = 400
Y = 400
cheeselist = []
endlist = []
mousepos = 0
mousedir = 0
levelwidth = 0
levelheight = 0
blocksize = 40
gamelist = []
#level you want -2
level = -1
emptyblock = [1,2,3,4,5]
paused = True
started = True
reset = False
#Colo(u)r variables
yellow = (255,255,0)
black = (0,0,0)
#Loop variables
running = True
#Screen variables
display_surface = pygame.display.set_mode((X,Y))
main_font = pygame.font.Font('assets/fonts/DOS-FONT.ttf', 32)
start_text = main_font.render("Cheese Terminator",True,yellow,black)
next_text = main_font.render("Well Done!",True,yellow,black)
win_text = main_font.render("You Won!!! :D",True,yellow,black)
main_font = pygame.font.Font('assets/fonts/DOS-FONT.ttf', 20)
start_text2 = main_font.render("Press Enter To Start",True,yellow,black)
start_text3 = main_font.render("Use Arrow Keys To Move",True,yellow,black)
next_text2 = main_font.render("Press Enter To Continue",True,yellow,black)
win_text2 = main_font.render("Press Enter To Play Again",True,yellow,black)
reset_text = main_font.render("Are You Shure You Want To Restart?",True,yellow,black)
reset_text2 = main_font.render("Press Enter To Continue",True,yellow,black)
reset_text3 = main_font.render("Press The Arrow Keys To Cancel",True,yellow,black)
textRect = start_text.get_rect()
textRect.center = (X // 2, ((Y // 2)-30))
textRect2 = start_text2.get_rect()
textRect2.center = (X // 2, ((Y // 2)-3))
textRect3 = start_text3.get_rect()
textRect3.center = (X // 2, ((Y // 2)+18))
textRectn = next_text.get_rect()
textRectn.center = (X // 2, ((Y // 2)-15))
textRectn2 = next_text2.get_rect()
textRectn2.center = (X // 2, ((Y // 2)+15))
textRectw = win_text.get_rect()
textRectw.center = (X // 2, ((Y // 2)-15))
textRectnw = win_text2.get_rect()
textRectnw.center = (X // 2, ((Y // 2)+15))
textRectr = reset_text.get_rect()
textRectr.center = (X // 2, ((Y // 2)-15))
textRectr2 = reset_text2.get_rect()
textRectr2.center = (X // 2, ((Y // 2)))
textRectr3 = reset_text3.get_rect()
textRectr3.center = (X // 2, ((Y // 2)+15))
M_0 = pygame.image.load("assets/textures/PNG_M_0.png")
M_0 = pygame.transform.scale(M_0,(blocksize,blocksize))
M_1 = pygame.image.load("assets/textures/PNG_M_1.png")
M_1 = pygame.transform.scale(M_1,(blocksize,blocksize))
M_2 = pygame.image.load("assets/textures/PNG_M_2.png")
M_2 = pygame.transform.scale(M_2,(blocksize,blocksize))
M_3 = pygame.image.load("assets/textures/PNG_M_3.png")
M_3 = pygame.transform.scale(M_3,(blocksize,blocksize))
C_0 = pygame.image.load("assets/textures/PNG_C_0.png")
C_0 = pygame.transform.scale(C_0,(blocksize,blocksize))
C_1 = pygame.image.load("assets/textures/PNG_C_1.png")
C_1 = pygame.transform.scale(C_1,(blocksize,blocksize))
P_0 = pygame.image.load("assets/textures/PNG_0.png")
P_0 = pygame.transform.scale(P_0,(blocksize,blocksize))
P_1 = pygame.image.load("assets/textures/PNG_1.png")
P_1 = pygame.transform.scale(P_1,(blocksize,blocksize))
P_2 = pygame.image.load("assets/textures/PNG_2.png")
P_2 = pygame.transform.scale(P_2,(blocksize,blocksize))
ICON = pygame.image.load("assets/icon.png")
#Screen display
pygame.display.set_caption("Cheese Terminator")
pygame.display.set_icon(ICON)
pygame.display.update()
#Functions
def setnewlevel(lvl):
  global endlist, cheeselist, mousepos, display_surface, levelwidth, levelheight, gamelist, mousedir, started
  started = False
  pygame.display.set_caption("Cheese Terminator - Level "+str(ldv.index(lvl)+1))
  level = lvl[1:]
  endlist = []
  cheeselist = []
  drawx = 0
  drawy = 0
  drawid = 0
  mousedir = 0
  width = lvl[0]
  height = len(level) / width
  display_surface = pygame.display.set_mode((round(width*blocksize),round(height*blocksize)))
  levelwidth = width
  levelheight = height
  i = 0
  while i < height:
    drawx = 0
    e = 0
    while e < width:
      if level[drawid] == 2:
        endlist.append(drawid)
      elif level[drawid] == 3:
        cheeselist.append(drawid)
      elif level[drawid] == 4:
        mousepos = drawid
      elif level[drawid] == 5:
        cheeselist.append(drawid)
        endlist.append(drawid)
      drawx = drawx + 30
      drawid = drawid + 1
      e = e + 1
    i = i + 1
    drawy = drawy + 30
  gamelist = level
def drawscreen():
  global levelwidth, levelheight, cheeselist, endlist, display_surface, gamelist
  if paused or reset:
    return
  cheese = [2,5]
  drawx = 0
  drawy = 0
  drawid = 0
  i = 0
  while i < levelheight:
    e = 0
    drawx = 0
    while e < levelwidth:
      w = 0
      if gamelist[drawid] == 0:
        w = 1
        display_surface.blit(P_1,(drawx*blocksize,drawy*blocksize))
      if gamelist[drawid] == 1:
        w = 1
        display_surface.blit(P_0,(drawx*blocksize,drawy*blocksize))
      if gamelist[drawid] in cheese:
        w = 1
        if drawid in cheeselist:
          display_surface.blit(C_1,(drawx*blocksize,drawy*blocksize))
        else:
          display_surface.blit(P_2,(drawx*blocksize,drawy*blocksize))
      if drawid in cheeselist:
        w = 1
        if gamelist[drawid] in cheese:
          display_surface.blit(C_1,(drawx*blocksize,drawy*blocksize))
        else:
          display_surface.blit(C_0,(drawx*blocksize,drawy*blocksize))
      if mousepos == drawid:
        w = 1
        if mousedir == 0:
          display_surface.blit(M_0,(drawx*blocksize,drawy*blocksize))
        elif mousedir == 1:
          display_surface.blit(M_1,(drawx*blocksize,drawy*blocksize))
        elif mousedir == 2:
          display_surface.blit(M_2,(drawx*blocksize,drawy*blocksize))
        elif mousedir == 3:
          display_surface.blit(M_3,(drawx*blocksize,drawy*blocksize))
        else:
          display_surface.blit(M_0,(drawx*blocksize,drawy*blocksize))
      if w == 0:
        display_surface.blit(P_0,(drawx*blocksize,drawy*blocksize))
      drawid = drawid + 1
      e = e + 1
      drawx = drawx + 1
    i = i + 1
    drawy = drawy + 1
def checblock(dir,pos):
  if dir == "u":
    try:
      return gamelist[pos-levelwidth]
    except:
      return "error"
  elif dir == "d":
    try:
      return gamelist[pos+levelwidth]
    except:
      return "error"
  elif dir == "l":
    if pos % levelwidth == 0:
      return "error"
    else:
      return gamelist[pos-1]
  elif dir == "r":
    if pos % levelwidth == (levelwidth-1):
      return "error"
    else:
      return gamelist[pos+1]
def checkifwon():
  q = 0
  a = 0
  while q < len(endlist):
    if endlist[q] in cheeselist:
      a = a + 1
    q = q + 1
  return a == q
#Main loop
display_surface.blit(start_text, textRect)
display_surface.blit(start_text2, textRect2)
display_surface.blit(start_text3, textRect3)
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        mousedir = 3
        if not checblock("u",mousepos) == "error":
          if checblock("u",mousepos) in emptyblock:
            if mousepos-levelwidth in cheeselist:
              if checblock("u",mousepos-levelwidth) in emptyblock:
                if not (mousepos-levelwidth-levelwidth in cheeselist):
                  cheeselist[cheeselist.index(mousepos-levelwidth)] = cheeselist[cheeselist.index(mousepos-levelwidth)]-levelwidth
                  mousepos = mousepos-levelwidth
            else:
              mousepos = mousepos-levelwidth
          elif mousepos-levelwidth in cheeselist:
            if checblock("u",mousepos-levelwidth) in emptyblock:
              if not (mousepos-levelwidth-levelwidth in cheeselist):
                cheeselist[cheeselist.index(mousepos-levelwidth)] = cheeselist[cheeselist.index(mousepos-levelwidth)]-levelwidth
                mousepos = mousepos-levelwidth
      if event.key == pygame.K_DOWN:
        mousedir = 1
        if not checblock("d",mousepos) == "error":
          if checblock("d",mousepos) in emptyblock:
            if mousepos+levelwidth in cheeselist:
              if checblock("d",mousepos+levelwidth) in emptyblock:
                if not (mousepos+levelwidth+levelwidth in cheeselist):
                  cheeselist[cheeselist.index(mousepos+levelwidth)] = cheeselist[cheeselist.index(mousepos+levelwidth)]+levelwidth
                  mousepos = mousepos+levelwidth
            else:
              mousepos = mousepos+levelwidth
          elif mousepos+levelwidth in cheeselist:
            if checblock("d",mousepos+levelwidth) in emptyblock:
              if not (mousepos+levelwidth+levelwidth in cheeselist):
                cheeselist[cheeselist.index(mousepos+levelwidth)] = cheeselist[cheeselist.index(mousepos+levelwidth)]+levelwidth
                mousepos = mousepos+levelwidth
      if event.key == pygame.K_LEFT:
        mousedir = 2
        if not checblock("l",mousepos) == "error":
          if checblock("l",mousepos) in emptyblock:
            if mousepos-1 in cheeselist:
              if checblock("l",mousepos-1) in emptyblock:
                if not (mousepos-2 in cheeselist):
                  cheeselist[cheeselist.index(mousepos-1)] = cheeselist[cheeselist.index(mousepos-1)]-1
                  mousepos = mousepos-1
            else:
              mousepos = mousepos-1
          elif mousepos-1 in cheeselist:
            if checblock("l",mousepos-1) in emptyblock:
              if not (mousepos-2 in cheeselist):
                cheeselist[cheeselist.index(mousepos-1)] = cheeselist[cheeselist.index(mousepos-1)]-1
                mousepos = mousepos-1
      if event.key == pygame.K_RIGHT:
        if reset:
          reset = False
          paused = False
          started = False
          display_surface = pygame.display.set_mode((levelwidth*30,levelheight*30))
        else:
          mousedir = 0
          if not checblock("r",mousepos) == "error":
            if checblock("r",mousepos) in emptyblock:
              if mousepos+1 in cheeselist:
                if checblock("r",mousepos+1) in emptyblock:
                  if not (mousepos+2 in cheeselist):
                    cheeselist[cheeselist.index(mousepos+1)] = cheeselist[cheeselist.index(mousepos+1)]+1
                    mousepos = mousepos+1
              else:
                mousepos = mousepos+1
            elif mousepos+1 in cheeselist:
              if checblock("r",mousepos+1) in emptyblock:
                if not (mousepos+2 in cheeselist):
                  cheeselist[cheeselist.index(mousepos+1)] = cheeselist[cheeselist.index(mousepos+1)]+1
                  mousepos = mousepos+1
      if event.key == pygame.K_RETURN:
        paused = not paused
        if started:
          started = False
          level += 1
          setnewlevel(lvldict[level])
        else:
          if paused:
            reset = True
            X = 400
            Y = 400
            display_surface = pygame.display.set_mode((X,Y))
            display_surface.fill(black)
            display_surface.blit(reset_text, textRectr)
            display_surface.blit(reset_text2, textRectr2)
            display_surface.blit(reset_text3, textRectr3)
          else:
            if reset:
              reset = False
              paused = False
              started = False
            setnewlevel(lvldict[level])
      if event.key == pygame.K_SPACE:
        started = False
        level += 1
        print("level "+str(level+1)+" len = "+str(len(lvldict[level])))
        setnewlevel(lvldict[level])
      if checkifwon():
        reset = False
        paused = True
        started = True
        X = 400
        Y = 400
        display_surface = pygame.display.set_mode((X,Y))
        display_surface.fill(black)
        display_surface.blit(next_text, textRectn)
        display_surface.blit(next_text2, textRectn2)
    X,Y = display_surface.get_size()
    drawscreen()
    pygame.display.update()