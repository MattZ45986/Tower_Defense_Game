import pygame
import random
import math

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("TOWER DEFENSE")
gameIcon = pygame.image.load('Icon.png')
pygame.display.set_icon(gameIcon)

class MovingTurret(object):
    def __init__(self):
        self.pos = (0,0)
        
    def display(self,pos):
        self.pos = pygame.mouse.get_pos()
        pygame.draw.rect(gameDisplay,(255,0,0), (pos[0],pos[1],30,30))

class Turret(object):
    def __init__(self, pos=(0,0), cost=100, speed=3, damage=8, color=(255,0,0), killCount=0):
        self.pos = pos
        self.cost = cost
        self.speed = speed
        self.damage = damage
        self.color = color
        self.killCount = killCount
        self.bList = []
        
    def display(self,pos):
        pygame.draw.rect(gameDisplay,(255,0,0), (pos[0],pos[1],30,30))

    def fire(self):
        b = Bullet(self.pos, 0, 3, self)
        self.bList.append(b)
        
    def getPos(self):
        return self.pos
    def getCost(self):
        return self.cost
    def getSpeed(self):
        return self.speed
    def getDamage(self):
        return self.damage
    def getColor(self):
        return self.color
    def getKillCount(self):
        return self.killCount

class MachineGun(Turret):
    def __init__(self, pos=(0,0), cost=100, speed=10, damage=3, color=(255,0,0), killCount=0):
        self.pos = pos
        self.cost = cost
        self.speed = speed
        self.damage = damage
        self.color = color
        self.killCount = killCount

class Bullet(object):
    def __init__(self, pos=(0,0), direction = 0, speed = 1, turret=None):
        self.pos = pos
        self.speed = speed
        self.turret = turret
        self.direction = direction

    def updatePos(self):
        y = self.speed * math.sin(math.radians(self.direction))
        x = self.speed * math.cos(math.radians(self.direction))
        self.pos = (self.pos[0] + x, self.pos[1] + y)

    def display(self):
        if 0 < self.pos[0] < 800:
            pygame.draw.circle(gameDisplay, (200,200,0), (round(self.pos[0]), round(self.pos[1])), 5)

    def getPos(self):
        return self.pos
    def getSpeed(self):
        return self.speed
    def getTureet(self):
        return self.turret
        
                         
class Dot(object):
    def __init__(self,points,speed=1):
        self.points = points
        self.point = 0
        self.pos = list(self.points[self.point])
        self.speed = speed
        

    def display(self):
        if self.point == len(self.points)-1:
            return True
        else:
            yD = self.points[self.point + 1][1] - self.points[self.point][1]
            xD = self.points[self.point + 1][0] - self.points[self.point][0]
            if xD == 0:
                x = 0
                if yD < 0: y = -1 * self.speed
                elif yD > 0: y = 1 * self.speed
                else: y = 0
            else:
                y = self.speed * yD * (1/math.sqrt(yD ** 2 + xD ** 2))
                x = self.speed * xD * (1/math.sqrt(yD ** 2 + xD ** 2))
            self.pos[0] += x
            self.pos[1] += y
        pygame.draw.circle(gameDisplay, (0,255,0), [int(round(self.pos[0])),int(round(self.pos[1]))],15)
        xNow = round(self.pos[0])
        xGoal = self.points[self.point + 1][0]
        yNow = round(self.pos[1])
        yGoal = self.points[self.point + 1][1]
        if (xNow ==  xGoal and  yNow == yGoal) or (self.pos[0] > self.points[self.point +1][0] and x > 0) or (self.pos[0] < self.points[self.point +1][0] and x < 0) or (self.pos[1] < self.points[self.point +1][1] and y < 0) or (self.pos[1] > self.points[self.point +1][1] and y > 0):
            self.point += 1
            self.pos = list(self.points[self.point])
        return False

def intro():
    done = False
    while not done:
        gameDisplay.fill((0,0,0))
        mouse = pygame.mouse.get_pos()
        if 330 < mouse[0] < 470 and 250 < mouse[1] < 350:  
            pygame.draw.rect(gameDisplay,(0,255,0), (330,250,140,100))
        else:
            pygame.draw.rect(gameDisplay,(255,0,0), (330,250,140,100))
        font = pygame.font.Font('freesansbold.ttf',50)
        TextSurf = font.render("Start",True,(127,127,127))
        TextRect = TextSurf.get_rect()
        TextRect.center = ((400),(300))
        gameDisplay.blit(TextSurf, TextRect)
        font = pygame.font.Font('freesansbold.ttf',80)
        TextSurf = font.render("TOWER DEFENSE",True,(127,127,127))
        TextRect = TextSurf.get_rect()
        TextRect.center = ((400),(150))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 330 < event.pos[0] < 470 and 250 < event.pos[1] < 350: done = True

def displayScore(text):
    font = pygame.font.Font('freesansbold.ttf',20)
    TextSurf = font.render(text,True,(127,127,127))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((740),(25))
    gameDisplay.blit(TextSurf, TextRect)

def displayLoss():
    c = 0
    gameDisplay.fill((0,0,0))
    while c < 1000:
        font = pygame.font.Font('freesansbold.ttf',80)
        TextSurf = font.render("YOU LOSE",True,(127,127,127))
        TextRect = TextSurf.get_rect()
        TextRect.center = ((400),(300))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        c += 1

def shoot(tlist):
    for turret in tlist:
        turret.fire()

def gameLoop():
    c = 0
    lives = 100
    done = False
    points =((10,50),(600,50),(600,550),(100,550),(100,150),(400,150),(400,400),(200,400),(200,200),(300,300),(500,300),(300,100),(700,100),(700,570),(50,570),(320,345))
    parameter = list(points)
    listy = []
    tlist = []
    turret = False
    pointList = points[:]
    while done == False:
        gameDisplay.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                parameter = list(points)
                if event.key == pygame.K_1: listy.append(Dot(parameter,.1))
                elif event.key == pygame.K_2: listy.append(Dot(parameter,.2))
                elif event.key == pygame.K_3: listy.append(Dot(parameter,.3))
                elif event.key == pygame.K_4: listy.append(Dot(parameter,.4))
                elif event.key == pygame.K_5: listy.append(Dot(parameter,.5))
                elif event.key == pygame.K_6: listy.append(Dot(parameter,.6))
                elif event.key == pygame.K_7: listy.append(Dot(parameter,.7))
                elif event.key == pygame.K_8: listy.append(Dot(parameter,.8))
                elif event.key == pygame.K_9: listy.append(Dot(parameter,.9))
                elif event.key == pygame.K_b: shoot(tlist)
                else: listy.append(Dot(parameter,3))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if turret == True:
                    turret = False
                    t1 = Turret(pygame.mouse.get_pos())
                    tlist.append(t1)
                if 800 > event.pos[0] > 770 and 285 < event.pos[1] < 315:
                    t1 = MovingTurret()
                    turret = True
        for thing in tlist:
            thing.display(thing.pos)
            for bullet in thing.bList:
                bullet.updatePos()
                bullet.display()
        if turret == True:
            t1.display(pygame.mouse.get_pos())
                
        pygame.draw.lines(gameDisplay,(255,153,51),False,pointList,10)
        for dot in listy:
            if dot is not None:
                if dot.display():
                    listy.remove(dot)
                    lives -= 1
        displayScore(str(lives) + " lives")
        pygame.draw.rect(gameDisplay,(255,255,0), (770,285,30,30))
        pygame.display.update()
        if lives == 0: return
## Main ##

intro()
gameLoop()
displayLoss()
    

pygame.quit()
quit()

