# Tower Defense, update 2.0

import pygame
import random
import math

pygame.init()

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption("TOWER DEFENSE")
gameIcon = pygame.image.load('Icon.png')
pygame.display.set_icon(gameIcon)

# more dots
# main menu
# more maps/ map control
# Create limit to # of towers
# upgrades!

class MovingTurret(object):
    def __init__(self, kind):
        self.pos = (0,0)
        self.kind = kind
        if kind == "basic": self.color = (255,0,0)
        elif kind == "machineGun": self.color = (255,165,0)
        elif kind == "destroyer": self.color = (18,77,141)
        elif kind == "sniper": self.color = (9,98,20)
        elif kind == "EMP": self.color = (94,43,136)
        else: self.color = (126,126,126)
        
    def display(self,pos):
        self.pos = pygame.mouse.get_pos()
        pygame.draw.rect(gameDisplay,self.color, (pos[0],pos[1],30,30))

##### TURRET #####

class Turret(object):
    def __init__(self, game, pos=(0,0), cost=100, speed=3, damage=6, color=(255,0,0), killCount=0):
        self.pos = pos
        self.cost = cost
        self.speed = speed
        self.damage = damage
        self.game = game
        self.color = color
        self.radius = 200
        self.killCount = killCount
        self.bList = []
        self.reloadTime = 100
        self.time = self.game.time % self.reloadTime
        self.born = self.game.time
        
    def display(self):
        pygame.draw.rect(gameDisplay,self.color, (self.pos[0],self.pos[1],30,30))

    def fire(self):
        b = Bullet((self.pos[0]+15,self.pos[1]+15), 0, 3, self,self.damage)
        if b.findTarget() != None: self.bList.append(b)
        else: b = None

    def deleteBullet(self, bullet):
        try:
            self.bList.remove(bullet)
        except ValueError:
                pass
        
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
    def __init__(self,game, pos):
        self.pos = pos
        self.game = game
        self.speed = 10
        self.cost = 150
        self.damage = 3
        self.color = (255,165,0)
        self.radius = 175
        self.killCount = 0
        self.bList = []
        self.reloadTime = 25
        self.time = self.game.time % self.reloadTime
        self.born = self.game.time

class Destroyer(Turret):
    def __init__(self,game, pos):
        self.pos = pos
        self.game = game
        self.speed = 2
        self.cost = 200
        self.damage = 21
        self.color = (18,77,141)
        self.radius = 300
        self.killCount = 0
        self.bList = []
        self.reloadTime = 250
        self.time = self.game.time % self.reloadTime
        self.born = self.game.time

class Sniper(Turret):
    def __init__(self,game, pos):
        self.pos = pos
        self.game = game
        self.speed = 4
        self.cost = 150
        self.damage = 6
        self.color = (9,98,20)
        self.radius = 1000
        self.killCount = 0
        self.bList = []
        self.reloadTime = 175
        self.time = self.game.time % self.reloadTime
        self.born = self.game.time

class EMP(Turret):
    def __init__(self,game, pos):
        self.pos = pos
        self.game = game
        self.speed = 1
        self.cost = 300
        self.damage = 0
        self.color = (94,43,136)
        self.radius = 200
        self.killCount = 0
        self.bList = []
        self.dList = []
        self.reloadTime = 300
        self.time = self.game.time % self.reloadTime
        self.born = self.game.time

    def fire(self):
        pygame.draw.circle(gameDisplay, (160,200,240), (self.pos[0]+15,self.pos[1]+15), 50)
        pygame.draw.circle(gameDisplay, (160,200,240), (self.pos[0]+15,self.pos[1]+15), 50)
        pygame.draw.circle(gameDisplay, (160,200,240), (self.pos[0]+15,self.pos[1]+15), 50)
        for dot in self.game.dList:
            if ((dot.getPos()[0]-self.pos[0])**2) + ((dot.getPos()[1]-self.pos[1])**2) < self.radius**2:
                dot.frozen = True
                self.dList.append((self.game.time + 150, dot))

##### BULLET #####

class Bullet(object):
    def __init__(self, pos=(0,0), direction = 0, speed = 2, turret=None, damage=3):
        self.pos = pos
        self.speed = speed
        self.turret = turret
        self.direction = direction
        self.damage = damage

    def findTarget(self):
        target = None
        dist = 1000
        for dot in self.turret.game.dList:
            d = math.sqrt(((dot.pos[0]-self.turret.getPos()[0]) ** 2) + ((dot.pos[1]-self.turret.getPos()[1]) ** 2))
            if  d < dist:
                target = dot
                dist = d
        if dist > self.turret.radius:
            self.turret.deleteBullet(self)
            return None
        return target

    def updatePos(self):
        dot = self.findTarget()
        if dot is not None:
            if (dot.pos[0]-self.pos[0]) != 0: self.direction = math.atan((dot.pos[1]-self.pos[1])/(dot.pos[0]-self.pos[0]))
            elif (dot.pos[1]-self.pos[1]) > 0: self.direction = math.radians(90)
            else: self.direction = math.radians(270)
            if (dot.pos[0]-self.pos[0]) < 0: self.direction += math.pi
        else:
            self.turret.deleteBullet(self)
            return
        y = self.speed * math.sin(self.direction)
        x = self.speed * math.cos(self.direction)
        self.pos = (self.pos[0] + x, self.pos[1] + y)
        if (((self.turret.pos[0]-self.pos[0])**2) + ((self.turret.pos[1]-self.pos[1])**2)) >= self.turret.radius ** 2: self.turret.deleteBullet(self)
        if dot is not None and ((self.pos[0]-dot.pos[0])**2) + ((self.pos[1]-dot.pos[1])**2) <= dot.radius ** 2:
            dot.radius -= self.damage
            self.turret.deleteBullet(self)

    def display(self):
        self.updatePos()
        if 0 < self.pos[0] < 800 and 0 < self.pos[1] < 600: pygame.draw.circle(gameDisplay, (200,200,0), (round(self.pos[0]), round(self.pos[1])), 5)
        else: self.turret.deleteBullet(self)

    def getPos(self):
        return self.pos
    def getSpeed(self):
        return self.speed
    def getDirection(self):
        return self.direction
    def getTurret(self):
        return self.turret

##### DOT ######
                         
class Dot(object):
    def __init__(self,game, points):
        self.points = points
        self.game = game
        self.point = 0
        self.radius = 15
        self.pos = list(self.points[self.point])
        self.speed = 2
        self.color = (0,255,0)
        self.frozen = False
        

    def updatePos(self):
        if self.radius < 6:
            self.game.deleteDot(self)
            return
        if self.point == len(self.points)-1:
            self.game.lives -= 1
            self.game.deleteDot(self)
            return
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
        xNow = round(self.pos[0])
        xGoal = self.points[self.point + 1][0]
        yNow = round(self.pos[1])
        yGoal = self.points[self.point + 1][1]
        if (xNow ==  xGoal and  yNow == yGoal) or (self.pos[0] > self.points[self.point +1][0] and x > 0) or (self.pos[0] < self.points[self.point +1][0] and x < 0) or (self.pos[1] < self.points[self.point +1][1] and y < 0) or (self.pos[1] > self.points[self.point +1][1] and y > 0):
            self.point += 1
            self.pos = list(self.points[self.point])

    def display(self):
        if self.radius < 6:
            self.game.deleteDot(self)
            return
        pygame.draw.circle(gameDisplay, self.color, [int(round(self.pos[0])),int(round(self.pos[1]))],self.radius)

    def getSpeed(self):
        return self.speed
    def getRadius(self):
        return self.radius
    def getPos(self):
        return self.pos
    def getMove(self):
        return not self.frozen

class FastDot(Dot):
    def __init__(self,game, points):
        self.points = points
        self.game = game
        self.point = 0
        self.radius = 12
        self.pos = list(self.points[self.point])
        self.speed = 4
        self.color = (240,33,245)
        self.frozen = False
class StrongDot(Dot):
    def __init__(self,game, points):
        self.points = points
        self.game = game
        self.point = 0
        self.radius = 21
        self.pos = list(self.points[self.point])
        self.speed = .5
        self.color = (37,119,146)
        self.frozen = False

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

def displayWallet(text):
    font = pygame.font.Font('freesansbold.ttf',20)
    TextSurf = font.render(text,True,(127,127,127))
    TextRect = TextSurf.get_rect()
    TextRect.center = ((740),(50))
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

def shoot(turrets):
    for turret in turrets:
        turret.fire()

##### ROUND #####

class RoundList(object):
    def __init__(self):
        self.length = 20

    def getList(self, num):
        x = 'self.getRound' + str(num)
        list1 = eval(x + "()")
        return list1

    def f(self,start,num,step=20):
        list1 = []
        for i in range(num):
            list1.append(("f",(i*step) + start))
        return list1
    def s(self,start,num,step=30):
        list1 = []
        for i in range(num):
            list1.append(("s",(i*step) + start))
        return list1
    def r(self,start,num,step=25):
        list1 = []
        for i in range(num):
            list1.append(("r",(i*step) + start))
        return list1
             
    def getRound1(self):
        return self.r(100,1)
    def getRound2(self):
        listy = self.r(100,15)
        listy.append(("s", 600))
        return  listy
    def getRound3(self):
        listy = self.f(100,15)
        listy += self.r(400, 10)
        return  listy
    def getRound4(self):
        listy = self.s(100, 5)
        listy += self.r(300, 15, 15)
        return  listy
    def getRound5(self):
        listy = self.s(100, 10, 10)
        listy += self.r(300, 15, 15)
        return []
    def getRound6(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound7(self):
        listy = self.s(100, 40, 10)
        listy += self.r(500, 15, 15)
        return listy
    def getRound8(self):
        listy = self.r(100, 40, 5)
        listy += self.f(350, 15, 15)
        return listy
    def getRound9(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound10(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound11(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound12(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound13(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound14(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound15(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound16(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound17(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound18(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound19(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
    def getRound20(self):
        listy = self.r(100, 40, 10)
        listy += self.f(500, 15, 15)
        return listy
                              
                              
                              
        
        
    

class Game(object):

    def __init__(self):
        self.lives = 100
        self.points =((10,50),(600,50),(600,550),(100,550),(100,150),(400,150),(400,450),(200,450),(200,300),(300,300))
        self.roundList = RoundList()
        self.round = 1
        self._rawQueue = self.roundList.getList(self.round)
        self.dotQueue = [x for x,y in self._rawQueue]
        self.timeQueue = [y for x,y in self._rawQueue]
        self.queueI = 0
        self.dList = []
        self.tList = []
        self.wallet = 1000
        self.inflation = 1
        self.time = 0

    def deleteDot(self, dot):
        if dot in self.dList: self.dList.remove(dot)
        if isinstance(dot, StrongDot): cost = 50
        elif isinstance(dot, FastDot): cost = 30
        else: cost = 20
        self.wallet += cost

    def displayWin(self):
        c = 0
        gameDisplay.fill((0,0,0))
        while c < 1000:
            font = pygame.font.Font('freesansbold.ttf',80)
            TextSurf = font.render("YOU WIN!",True,(127,127,127))
            TextRect = TextSurf.get_rect()
            TextRect.center = ((400),(300))
            gameDisplay.blit(TextSurf, TextRect)
            pygame.display.update()
            c += 1
        pygame.quit()
        quit()
        

    def pauseRound(self, end=False):
        done = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < 30 and event.pos[1] < 30:
                done = True
        while not done:
            pygame.draw.rect(gameDisplay,(255,255,0), (770,285,30,30))
            pygame.draw.rect(gameDisplay,(255,0,255), (770,315,30,30))
            pygame.draw.rect(gameDisplay,(0,0,255), (770,345,30,30))
            pygame.draw.rect(gameDisplay,(0,255,0), (770,375,30,30))
            pygame.draw.rect(gameDisplay,(94,43,136), (770,405,30,30))
            pygame.draw.rect(gameDisplay,(0,0,0), (0,0,30,30))
            pygame.draw.polygon(gameDisplay, (126,126,126), ((0,0),(30,15),(0,30)))
            for thing in self.tList:
                    thing.display()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0] < 30 and event.pos[1] < 30:
                    done = True
    
    def gameLoop(self):
        done = False
        clock = pygame.time.Clock()
        parameter = list(self.points)
        turret = False
        pointList = self.points[:]
        for round in range(1,21):
            self.startRound(done,clock,parameter,turret,pointList)
            self.pauseRound(True)
            self.round += 1
            self.queueI = 0
            if self.round == 21: self.displayWin()
            self._rawQueue = self.roundList.getList(self.round)
            self.dotQueue = [x for x,y in self._rawQueue]
            self.timeQueue = [y for x,y in self._rawQueue]
            self.time = 0
            
        

    def startRound(self,done,clock,parameter,turret,pointList):
        while done == False:
            print(str(clock.get_fps()))
            clock.tick()
            gameDisplay.fill((0,0,0))
            self.inflation = (len(self.tList) // 3)  + 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if turret == True:
                        turret = False
                        kind = t1.kind
                        if kind == "basic": t1 = Turret(self, pygame.mouse.get_pos())
                        elif kind == "machineGun":  t1 = MachineGun(self, pygame.mouse.get_pos())
                        elif kind == "destroyer": t1 = Destroyer(self, pygame.mouse.get_pos())
                        elif kind == "sniper": t1 = Sniper(self, pygame.mouse.get_pos())
                        elif kind == "EMP": t1 = EMP(self, pygame.mouse.get_pos())
                        self.tList.append(t1)
                        self.wallet -= t1.getCost() * self.inflation
                    if 800 > event.pos[0] > 770 and 285 < event.pos[1] < 315 and self.wallet >= 100 * self.inflation:
                        t1 = MovingTurret("basic")
                        turret = True
                    elif 800 > event.pos[0] > 770 and 315 < event.pos[1] < 345 and self.wallet >= 150 * self.inflation:
                        t1 = MovingTurret("machineGun")
                        turret = True
                    elif 800 > event.pos[0] > 770 and 345 < event.pos[1] < 375 and self.wallet >= 200 * self.inflation:
                        t1 = MovingTurret("destroyer")
                        turret = True
                    elif 800 > event.pos[0] > 770 and 375 < event.pos[1] < 405 and self.wallet >= 150 * self.inflation:
                        t1 = MovingTurret("sniper")
                        turret = True
                    elif 800 > event.pos[0] > 770 and 405 < event.pos[1] < 435 and self.wallet >= 300 * self.inflation:
                        t1 = MovingTurret("EMP")
                        turret = True
                    elif 30 > event.pos[0] > 0 and 30 > event.pos[1] > 0:
                        self.pauseRound(False)
            while self.queueI != len(self.timeQueue) and self.time == self.timeQueue[self.queueI]:
                if self.dotQueue[self.queueI] == "r": self.dList.append(Dot(self, parameter))
                elif self.dotQueue[self.queueI] == "f": self.dList.append(FastDot(self, parameter))
                elif self.dotQueue[self.queueI] == "s": self.dList.append(StrongDot(self, parameter))
                self.queueI += 1
            if self.queueI == len(self.timeQueue) and len(self.dList) == 0:
                    done = True
            pygame.draw.lines(gameDisplay, (0,255,255), False, pointList, 6)
            for point in self.points:
                pygame.draw.circle(gameDisplay, (0,255,255), (point[0]+1,point[1]+1), 3)
            if turret == True: t1.display(pygame.mouse.get_pos())
            for thing in self.tList:
                thing.display()
                if self.time % thing.reloadTime == thing.time: thing.fire()
                for bullet in thing.bList:
                    bullet.display()
                if isinstance(thing, EMP):
                    for pair in thing.dList:
                        if pair[0] == self.time:
                            pair[1].frozen = False
                            thing.dList.remove(pair)
            for dot in self.dList:
                if dot is not None:
                    if dot.getMove(): dot.updatePos()
                    dot.display()
            displayScore(str(self.lives) + " lives")
            displayWallet("$" + str(self.wallet))
            pygame.draw.rect(gameDisplay,(255,255,0), (770,285,30,30))
            pygame.draw.rect(gameDisplay,(255,0,255), (770,315,30,30))
            pygame.draw.rect(gameDisplay,(0,0,255), (770,345,30,30))
            pygame.draw.rect(gameDisplay,(0,255,0), (770,375,30,30))
            pygame.draw.rect(gameDisplay,(94,43,136), (770,405,30,30))
            pygame.draw.rect(gameDisplay,(126,126,126), (0,0,10,30))
            pygame.draw.rect(gameDisplay,(126,126,126), (20,0,10,30))
            pygame.display.update()
            self.time += 1
            if self.time == 25200: time = 0
            if self.lives == 0: displayLoss()

    
## Main ##

intro()
g = Game()
g.gameLoop()
    

pygame.quit()
quit()
