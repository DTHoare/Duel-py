#2 player projectile dueling game styled on 'tanks' by Daniel Hoare

#contents:
#imports
#variables
#classes
#functions
#game loop

import pygame, math, sys, random
from pygame.locals import *
pygame.mixer.pre_init(44100,-16,2,2048)
pygame.init()

#VARIABLES
windowWidth = 640
windowHeight = 480
gravity = 1
fps = 30
running = True

projectileList = pygame.sprite.Group()
playerList = pygame.sprite.Group()
obstacleList = pygame.sprite.Group()

textColour = (255, 255, 255)
black = (0, 0, 0)

largeFont = pygame.font.SysFont(None, 70)
medFont = pygame.font.SysFont(None, 30)
smallFont = pygame.font.SysFont("monospace", 12)

mainClock = pygame.time.Clock()

screen = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('duel')


hitSound = pygame.mixer.Sound('hitSound.wav')
hitSound2 = pygame.mixer.Sound('hitSound2.wav')
countDown = pygame.mixer.Sound('321go.wav')


#CLASSES
class Character(pygame.sprite.Sprite):
    def __init__(self, playerNumber):
        pygame.sprite.Sprite.__init__(self) 
        
        self.playerNumber = playerNumber        
        self.bodyImageBloodied = pygame.image.load('bodyBloodied' + str(playerNumber) + '.png').convert_alpha()
        self.bodyImageDead = pygame.image.load('bodyDead' + str(playerNumber) + '.png').convert_alpha()
        self.bodyImageOriginal = pygame.image.load('body' + str(playerNumber) + '.png').convert_alpha()
        self.armImageOriginal = pygame.image.load('arm' + str(playerNumber) + '.png').convert_alpha()                
        self.wins = 0
        
    def reset(self, angle, x, y):
        self.reloadCounter = 500        
        self.x = x
        self.y = y
        self.angle = angle
        self.angleOriginal = angle
        self.power = 0
        self.health = 100
        self.bodyImage = self.bodyImageOriginal
        self.rect = self.bodyImage.get_rect()
        self.rect.center = (x, y)
        
        self.armImage = pygame.transform.rotate(self.armImageOriginal, self.angle)
        self.armRect = self.armImage.get_rect()
        self.armRect.center = (self.x, self.y -5)        
        playerList.add(self)
        
    def createProjectile(self):
        x = self.armRect.center[0] + math.cos(math.radians(self.angle)) * 18
        y = self.armRect.center[1] - math.sin(math.radians(self.angle)) * 18
        projectile = Projectile(self.power, self.angle, x, y, self.playerNumber)
        projectileList.add(projectile)
        self.power = 0
        self.angle = self.angleOriginal
        
    def update(self, powerup, powerdown, rotateAC, rotateC, fire, moveLeft, moveRight):
        self.reloadCounter += 10        
        keys = pygame.key.get_pressed()
        x = round(self.armRect.center[0] + math.cos(math.radians(self.angle)) * 18)
        y = round(self.armRect.center[1] - math.sin(math.radians(self.angle)) * 18)
        pygame.draw.circle(screen, black, (x, y), 1 + round(self.power / 5))
        if keys[powerup] and self.power < 60:
            self.power += 1
        if keys[powerdown] and self.power > 0:
            self.power -= 1
        if keys[rotateAC] and self.angle <=180:
            self.angle += 2
            pygame.draw.rect(screen, (0,0,0), self.armRect)
        if keys[rotateC] and self.angle >= 0:
            self.angle -= 2
            pygame.draw.rect(screen, (0,0,0), self.armRect)        
        if keys[fire] and self.reloadCounter > 500:
            pygame.draw.circle(screen, black, (x, y), 2*round(self.power / 5))
            pygame.draw.rect(screen, (0,0,0), self.armRect)  
            self.createProjectile()
            self.reloadCounter = 0  
        if keys[moveLeft]:
            pygame.draw.rect(screen, (0,0,0), self.armRect)
            pygame.draw.rect(screen, (0,0,0), self.rect)
            self.x -=1
        if keys[moveRight]:
            pygame.draw.rect(screen, (0,0,0), self.armRect)
            pygame.draw.rect(screen, (0,0,0), self.rect)
            self.x += 1
        self.armImage = pygame.transform.rotate(self.armImageOriginal, self.angle)
        self.armRect = self.armImage.get_rect()
        self.armRect.center = (self.x, self.y -5)
        self.rect.center = (self.x, self.y)
        self.updateImage()
        if self.power > 0:
            pygame.draw.circle(screen, (255,255,255), (x, y), round(self.power / 5))
        
    def updateImage(self):
        if self.health <= 0:
            pygame.draw.rect(screen, (0,0,0), self.armRect)
            self.bodyImage = self.bodyImageDead
            self.rect = self.bodyImage.get_rect()
            self.rect.center = (self.x, self.y + 6)
        elif self.health <= 50:
            pygame.draw.rect(screen, (0,0,0), self.armRect)
            self.bodyImage = self.bodyImageBloodied
            self.rect = self.bodyImage.get_rect()
            self.rect.center = (self.x, self.y + 6)
            self.armRect.center = (self.x, self.y + 3)
        
     

class Projectile(pygame.sprite.Sprite):
    def __init__(self, power, angle, x, y, playerNumber = 1):
        pygame.sprite.Sprite.__init__(self)
        
        self.velocity = power
        self.xVelocity = math.cos(math.radians(angle))*self.velocity
        self.yVelocity = math.sin(math.radians(angle))*self.velocity
        self.angle = angle
        self.x = x
        self.y = y
        
        self.imageOriginal = pygame.image.load('projectile' + str(playerNumber) + '.png')
        self.image = pygame.transform.rotate(self.imageOriginal, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        
    def updatePosition(self):
        self.yVelocity -= gravity 
        self.x += self.xVelocity
        self.y -= self.yVelocity
        self.velocity = math.sqrt(self.xVelocity**2 + self.yVelocity**2)
        try:
            self.angle = math.degrees(math.acos(self.xVelocity/self.velocity))
            if self.yVelocity < 0:
                self.angle *= -1
        except:
            self.angle = -90
        pygame.draw.rect(screen, (0, 0, 0), self.rect)
        self.image = pygame.transform.rotate(self.imageOriginal, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
    
    def delete(self):
        if self.rect.top > windowHeight:
            projectileList.remove(self)
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, breakable, health = 100):
        pygame.sprite.Sprite.__init__(self)       
        self.rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, (199, 166, 189), self.rect)
        self.breakable = breakable
        obstacleList.add(self)
        self.health = health
        
    def damageCheck(self):
        if self.breakable:
            self.health -= 50
        if self.health <= 0:
            obstacleList.remove(self)
            pygame.draw.rect(screen, black, self.rect)
        
#FUNCTIONS
def terminate():
    pygame.quit()
    sys.exit()
    
def drawText(text, font, x, y, c=textColour, position='left'):
    textObj = font.render(text, 1, c)
    textRect = textObj.get_rect()
    if position == 'left':
        textRect.topleft = (x, y)
    elif position == 'center':
        textRect.midtop = (x, y)
    else:
        textRect.topright = (x, y)
    screen.blit(textObj, textRect)
    textRect.inflate(100, 0)
    return textRect
    
def createObstacles(x, y, size, width, height, breakable, health):
    for h in range(height):
        for w in range(width):
            obstacle = Obstacle(x+w*size, y+h*size, size, size, breakable, health)
        
    
    
def startScreen():
    backgroundImage = pygame.image.load('background.png').convert()
    backgroundRect = backgroundImage.get_rect()
    pygame.mixer.music.load('startScreen.wav')
    pygame.mixer.music.play(-1, 0.0)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return
        screen.blit(backgroundImage, backgroundRect)
        drawText('version 0.8 beta. Created by Daniel Hoare 2013.', smallFont, (windowWidth / 3 + 80), (windowHeight / 3) + 300)
        pygame.display.update()
        mainClock.tick(2)
        drawText('P r e s s   a n y   k e y   t o   s t a r t .', medFont, (windowWidth / 3 + 60), (windowHeight / 3) + 180)
        pygame.display.update()
        mainClock.tick(2)
               
def mainLoop():
    pygame.mixer.music.stop()    
    screen.fill(black)
    playerList.empty()
    playerOne.reset(0, 50, 400)
    playerTwo.reset(180, 590, 400)    
    screen.blit(playerOne.bodyImage, playerOne.rect)
    screen.blit(playerTwo.bodyImage, playerTwo.rect)
    
    for player in playerList:
        drawText(str(player.wins), largeFont, player.x, 20, position='center')
        
    obstacleList.empty()
    floor = Obstacle(0, 420, windowWidth, windowHeight - 420, False)
    createObstacles(windowWidth /2 - 20, random.randint(340, 380), 5, 8, 16, True, 50)
    
    countDown.play()
    for n in [3, 2, 1, 'GO']:
        textRect = drawText(str(n) + '!', largeFont, windowWidth/2, 200, position='center')
        pygame.display.update()
        mainClock.tick(1)
        pygame.draw.rect(screen, (0,0,0), textRect)
        
    
    createObstacles(windowWidth /2 - 10, random.randint(120, 260), 10, 2, random.randint(4, 16), True, 50)
       
   
    pygame.mixer.music.load('backgroundMusic.wav')
    pygame.mixer.music.play(-1, 0.0)
    mainLoop = True
    while mainLoop:     
        playerOne.update(ord('w'),ord('s'),ord('a'),ord('d'),ord(' '),ord('q'),ord('e'))
        playerTwo.update(K_KP5, K_KP2, K_KP1, K_KP3, K_KP0, K_KP4, K_KP6)
        for player in playerList:
            screen.blit(player.armImage, player.armRect)
            screen.blit(player.bodyImage, player.rect)
            
        for p in projectileList:
            p.delete()
            p.updatePosition()
            screen.blit(p.image, p.rect)
            
        #projectile collision and damage    
        for player in playerList:
            collisionList = pygame.sprite.spritecollide(player, projectileList, True)
            for c in collisionList:
                hitSound.play()
                pygame.draw.rect(screen, (0,0,0), player.rect)
                pygame.draw.rect(screen, (0,0,0), c.rect)
                player.health -= 50
                player.updateImage()                
            if player.health <= 0 and len(playerList) == 2:
                pygame.mixer.music.stop() 
                screen.blit(player.bodyImage, player.rect)
                pygame.display.update()
                mainClock.tick(1)
                playerList.remove(player)                
                victoryRect = drawText('PLAYER ' + str(player.playerNumber) + ' IS DEAD!', largeFont, windowWidth/2, 200, position='center')                        
                pygame.display.update()                
                mainClock.tick(0.4)
                pygame.draw.rect(screen, (0,0,0), victoryRect)
                victoryRect = drawText('PLAYER ' + str(3-player.playerNumber) + ' IS VICTORIOUS!', largeFont, windowWidth/2, 200, position='center')
                pygame.display.update()
                for p in playerList:
                    p.wins += 1  
            elif player.health <= 0:
                playerList.remove(player)
                screen.blit(player.bodyImage, player.rect)                
                drawText('but also dead.', smallFont, windowWidth/2, 250, position='center')
                pygame.display.update()
                mainClock.tick(0.5)
                mainLoop = False
        if len(playerList) < 2 and len(projectileList) == 0:
            pygame.display.update()
            mainClock.tick(0.4)            
            mainLoop = False
                
                                
        for obstacle in obstacleList:
            collisionList = pygame.sprite.spritecollide(obstacle, projectileList, True)           
            if collisionList:
                hitSound2.play()
                obstacle.damageCheck()
        
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
        pygame.display.update()
        mainClock.tick(fps)


#GAME LOOP
startScreen()
playerOne = Character(1)
playerTwo = Character(2)
while True:    
    mainLoop()




