import pygame, pyganim, tkinter, math

from tkinter import *
from math import *

from pygame import *
from pyganim import *

pygame.init()
running = level = 1
speed = 4
width = 95
height = 100
Screen_Width = 900
Screen_Height = 600
screen=pygame.display.set_mode((Screen_Width, Screen_Height))
background = (239, 228, 176)
platWidth = platHeight = 50
inventary = []
newLev = False
coins = pygame.sprite.Group()
life = 20
money = 0
real_objects = pygame.sprite.Group()

class Monster(sprite.Sprite):
    def __init__(self, x, y, path,selfWidth, selfHeight):
        sprite.Sprite.__init__(self)
        self.StartX = x
        self.speed = 3
        self.StartY = y
        self.image = pygame.image.load(path)
        self.rect = pygame.rect.Rect(x, y, selfWidth, selfHeight)
        self.life = 6
        self.power = 1
        self.xvel = 0
        self.yvel = -2

    def move(self, entities):
        global attack, life
        for f in entities:
            if (sprite.collide_rect(self, f)) and isinstance(f, Player) and attack:
                if attack:
                    print('Monster hits player: ', self.power)
                    pygame.time.delay(50)
                    self.xvel = 0
                    self.yvel = 0
                    life -= self.power
        self.collide(self.xvel, 0, entities)
        self.rect.x += self.xvel
        self.collide(0, self.yvel, entities)
        self.rect.y += self.yvel

    def collide(self,xvel,yvel,entities):
        for f in entities:
            if (sprite.collide_rect(self,f)) and not(isinstance(f,Player)): 
                if xvel>0:
                    self.rect.right = f.rect.left
                    self.xvel = 0
                    self.yvel = self.speed
                if xvel<0:
                    self.rect.left = f.rect.right
                    self.xvel = 0
                    self.yvel = -self.speed
                if yvel>0:
                    self.rect.bottom = f.rect.top
                    self.xvel = -self.speed
                    self.yvel = 0
                if yvel<0:
                    self.rect.top = f.rect.bottom
                    self.xvel = self.speed
                    self.yvel = 0
        
class Real_Object(sprite.Sprite):  #будущий инвентарь героя, лежащий на карте
    def __init__(self,x,y,path,type1,selfWidth,selfHeight):
        sprite.Sprite.__init__(self)
        self.type1 = type1
        self.image = pygame.image.load(path)
        self.rect = pygame.rect.Rect(x,y,selfWidth,selfHeight)
        
    def collide(self,smbd):
        if sprite.collide_rect(self,smbd):
            global real_objects
            o = True
            for i in inventary:
                if i.type1 == 'sword':
                    o = False
            if o:
                inventary.append(self)
                self.kill()


class LifeBlock(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.image = pygame.image.load('img/life.png')

    def collide(self, smth):
        global life
        if sprite.collide_rect(self, smth):
            if life < 20:
                life += 1
                self.kill()
            

class Platform(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/tree.png')


class Coin(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/coin.png')


class Wall(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/wall.png')


class Bed(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/bed.png')

        
class PlatExit(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/exit.png')


class PlatLevelDown(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/exit.png')


class PlatLevel(sprite.Sprite):
    def __init__(self,x,y):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load('img/exit.png')


class NPC(sprite.Sprite):
    def __init__(self,x,y,text,path):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x,y,platWidth,platHeight)
        self.image = pygame.image.load(path)
        self.text = text

        
class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self,target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    global Screen_Height,Screen_Width
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+Screen_Width / 2, -t+Screen_Height / 2
    l = min(0,l)
    l = max(-(camera.width-Screen_Width),l)
    t = min(0,t)
    t = max(-(camera.height-Screen_Height),t)
    return Rect(l,t,w,h)


Animation_Delay = 0.1
Animation_Attack = [('img/startHero/heroW1.png'),
                    ('img/startHero/heroAtt.png')]
Animation_Down = [('img/startHero/heroW2.png'),
                  ('img/startHero/heroW3.png')]
Animation_Stay = [('img/startHero/heroW1.png',0.1)]
Animation_Right = [('img/startHero/heroR1.png'),
                   ('img/startHero/heroR2.png'),
                   ('img/startHero/heroR3.png')]
Animation_Left = [('img/startHero/heroL1.png'),
                   ('img/startHero/heroL2.png'),
                   ('img/startHero/heroL3.png')]


class Player(sprite.Sprite):
    def __init__(self,x,y,power):
        sprite.Sprite.__init__(self)
        self.xvel=0
        self.yvel=0
        selfStartX=x
        self.power=power
        global inventary
        for i in inventary:
            if i.type1=='sword' and self.power==3:
                self.power+=2
        selfStartY=y
        self.image = Surface((width,height))
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.image.set_colorkey(background)
        

        boltAnim = []
        for anim in Animation_Down:
            boltAnim.append((anim,Animation_Delay))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()
        
        boltAnim = []
        self.boltAnimStay = pyganim.PygAnimation(Animation_Stay)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        
        boltAnim = []
        for anim in Animation_Right:
            boltAnim.append((anim,Animation_Delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        
        boltAnim = []
        for anim in Animation_Left:
            boltAnim.append((anim,Animation_Delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.image.fill(background)

        boltAnim = []
        for anim in Animation_Attack:
            boltAnim.append((anim,Animation_Delay*5))
        self.boltAnimAttack = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttack.play()
        self.image.fill(background)

    def update(self,left,right,up,down,platforms):
        global attack, life, monsters, coins, entities, money
        
        self.image.fill(background)
        for m in monsters:
            if sprite.collide_rect(self,m) and attack:
                print('Player hits monster: ',self.power)
                m.life-=self.power
                pygame.time.delay(50)
                if m.life<1:
                    m.kill()
                    pf = Coin(m.rect.x,m.rect.y)
                    pf.__init__(m.rect.x,m.rect.y)
                    entities.add(pf)
                    coins.add(pf)
                    
        if coins:
            for  c in coins:
                if sprite.collide_rect(self,c):
                    c.kill()
                    money += 1
                    
        if left:
            self.xvel=-speed
            self.boltAnimLeft.blit(self.image, (0, 0))
            
        elif right:
            self.xvel=speed
            self.boltAnimRight.blit(self.image, (0, 0))
            
        elif up:
            self.yvel=-speed
            self.boltAnimDown.blit(self.image, (0, 0))
            
        elif down:
            self.yvel=speed
            self.boltAnimDown.blit(self.image, (0, 0))
            
        if attack:
            self.xvel=0
            self.boltAnimAttack.blit(self.image, (0, 0))
        if not(left or right or up or down or attack):
            self.xvel=0
            self.yvel=0
            self.boltAnimStay.blit(self.image, (0, 0))
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            global talk
            if sprite.collide_rect(self, p):
                if isinstance(p, PlatExit):
                    for i in inventary:
                        if i.type1=='sword':
                            pygame.time.delay(300)
                            global newLev, level
                            newLev = True
                            level += 1
                    if not(len(inventary)):
                        root = Tk()
                        root.geometry('+500+300')
                        root.title('Warning')
                        img = tkinter.PhotoImage(file='img/text/dangerous.gif')
                        button1 = tkinter.Button(root, image = img, command=root.destroy)
                        button1.pack()
                        root.mainloop()
                elif isinstance(p, PlatLevelDown):
                    global level, newLev
                    level -= 1
                    newLev = True
                elif isinstance(p, Bed):
                    global life, sleep
                    if sleep:
                        print('sleep...')
                        pygame.time.delay(200)
                        imga = pygame.image.load('img/sleep.png')
                        imgarect = imga.get_rect()
                        screen.blit(imga, imgarect)
                        pygame.display.flip()
                        pygame.time.delay(5000)
                        life = 20
                        sleep = False
                elif isinstance(p,NPC) and talk:
                    root = Tk()
                    root.geometry('+500+300')
                    root.title('Advice')
                    imga = tkinter.PhotoImage(file='img/text/text'+str(level)+'.gif')
                    button1 = tkinter.Button(root, image = imga, command=root.destroy)
                    button1.pack()
                    root.mainloop()
                if xvel > 0:
                    self.rect.right = p.rect.left
                elif xvel < 0:
                    self.rect.left = p.rect.right
                elif yvel > 0:
                    self.rect.bottom = p.rect.top
                elif yvel < 0:
                    self.rect.top = p.rect.bottom
                

def generate():
    global entities, hero, platforms, camera, monsters, lifes
    monsters = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    lifes =  pygame.sprite.Group()
    platforms = []
    x = strk = y = 0
    f=open ('levels\level' + str(level) + '.txt')
    
    for row in f:
        for col in row:
            if col == '&': #sword
                pf = Real_Object(x, y, 'img/sword1.png', 'sword', platWidth, platHeight)
                pf.__init__(x, y, 'img/sword1.png', 'sword', platWidth, platHeight)
                real_objects.add(pf)
                entities.add(pf)
            elif col == 'H': #hero
                if level == 1:
                    hero=Player(x, y, 2)
                    hero.__init__(x, y, 2)
                else:
                    hero=Player(x, y, 4)
                    hero.__init__(x, y, 4)
                entities.add(hero)
            elif col == 'P': # npc
                fText = open('text.txt')
                i = 0
                for t in fText:
                    i += 1
                    if i == level:
                        pf = NPC(x, y, t, 'img/npc/npc' + str(level) + '.png')
                        pf.__init__(x, y, t, 'img/npc/npc' + str(level) + '.png')
                        entities.add(pf)
                        platforms.append(pf)
            elif col == 'S': #bed
                pf = Bed(x, y)
                pf.__init__(x, y)
                entities.add(pf)
                platforms.append(pf)
            elif col == '%': #life
                pf = LifeBlock(x+10, y+10)
                pf.__init__(x+10, y+10)
                lifes.add(pf)
            elif col == '-':  #блок
                pf=Platform(x, y)
                platforms.append(pf)
                entities.add(pf)
            elif col == '/':  #levelUp
                pf = PlatExit(x, y)
                platforms.append(pf)
                entities.add(pf)
            elif col == '!':  #levelDown
                pf = PlatLevelDown(x, y)
                platforms.append(pf)
                entities.add(pf)    
            elif col == '=': #переход на уровень
                pf = PlatLevel(x, y)
                platforms.append(pf)
                entities.add(pf)
            elif col == 'D':  #walls of house
                pf = Wall(x, y) 
                platforms.append(pf)
                entities.add(pf)
            elif col == '*': #мобы
                pf = Monster(x, y, 'img/monster.png', platWidth, platHeight)
                pf.__init__(x, y, 'img/monster.png', platWidth, platHeight)
                monsters.add(pf)
            x += platWidth
        strk += 1
        y += platHeight
        x = 0
        
    levelWidth = len(row) * platWidth
    levelHeight= strk * platHeight
    camera = Camera(camera_configure, levelWidth, levelHeight)
    f.close()

generate()

timer = pygame.time.Clock()
left = right = up = down = attack = sleep = talk = False

root = Tk()
root.geometry('+500+300')
root.title('Advice')
imga = tkinter.PhotoImage(file='img/text/text0.gif')
button1 = tkinter.Button(root, image = imga, command=root.destroy)
button1.pack()
root.mainloop()

while running:
    if newLev:
        newLev = False
        generate()
        print('------------------')
    for m in monsters:
        m.move(entities)
    for RO in real_objects:
        RO.collide(hero)
    for l in lifes:
        l.collide(hero)
    if Animation_Down[1] != 'img/swordHero/heroW3.png':
        for i in inventary:
            if i.type1 == 'sword':
                Animation_Down = [('img/swordHero/heroW2.png'),
                                  ('img/swordHero/heroW3.png')]
                Animation_Stay = [('img/swordHero/heroW1.png',0.1)]
                Animation_Right = [('img/swordHero/heroR1.png'),
                                   ('img/swordHero/heroR2.png'),
                                   ('img/swordHero/heroR3.png')]
                Animation_Left = [('img/swordHero/heroL1.png'),
                                ('img/swordHero/heroL2.png'),
                                ('img/swordHero/heroL3.png')]
                Animation_Attack = [('img/swordHero/heroW1.png'),
                                    ('img/swordHero/heroAtt.png')]
                hero.__init__(hero.rect.x, hero.rect.y,4)
                
    timer.tick(60)
    screen.fill(background)
    camera.update(hero)
    hero.update(left, right, up, down, platforms)
    
    for e in entities:
        screen.blit(e.image, camera.apply(e))
    for m in monsters:
        screen.blit(m.image, camera.apply(m))
    for l in lifes:
        screen.blit(l.image, camera.apply(l))
    pygame.display.set_caption('Level '+str(level)+' life '+str(trunc(life))+' money '+str(money))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not(up or down or right or left or attack):
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up = True
                elif event.key == K_DOWN:
                    down = True
                elif event.key == K_LEFT:
                    left = True
                elif event.key == K_RIGHT:
                    right = True
                elif event.key == K_a:
                    attack = True
                elif event.key == K_s:
                    sleep = True
                elif event.key == K_t:
                    talk = True
                
        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            elif event.key==K_DOWN:
                down = False
            elif event.key==K_LEFT:
                left = False
            elif event.key==K_RIGHT:
                right = False
            elif event.key==K_a:
                attack = False
            elif event.key==K_s:
                sleep = False
            elif event.key == K_t:
                talk = False
    pygame.display.flip()

pygame.display.quit()
