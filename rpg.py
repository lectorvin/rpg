import pygame
import pyganim

from pygame import *
from pyganim import *

pygame.init()
RUNNING = LEVEL = 1
WIDTH = 95
HEIGHT = 100
SCREENWIDTH = 900
SCREENHEIGHT = 600
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BACKGROUND = (239, 228, 176)
PLATWIDTH = PLATHEIGHT = 50
inventary = []
LEVUP = False
LEVDOWN = False
LIFE = 20
MONEY = 0


def say(title, path):
    """if you want to say something to user, like advice from npc;
    path - path of image with text, title - title of window"""
    root = tkinter.Tk()
    root.geometry('+500+300')
    root.title(title)
    img = tkinter.PhotoImage(file=path)
    button1 = tkinter.Button(root, image=img, command=root.destroy)
    button1.pack()
    root.mainloop()


def collide_the_wall(smbd, wall, xvel, yvel):
    """function for check, if smbd collide the wall(or other object);
    xvel, yvel = direction of moving"""
    if xvel > 0:
        smbd.rect.right = wall.rect.left
        if isinstance(smbd, Monster):
            smbd.yvel = smbd.speed
            smbd.xvel = 0
    elif xvel < 0:
        smbd.rect.left = wall.rect.right
        if isinstance(smbd, Monster):
            smbd.yvel = -smbd.speed
            smbd.xvel = 0
    if yvel > 0:
        smbd.rect.bottom = wall.rect.top
        if isinstance(smbd, Monster):
            smbd.xvel = -smbd.speed
            smbd.yvel = 0
    elif yvel < 0:
        smbd.rect.top = wall.rect.bottom
        if isinstance(smbd, Monster):
            smbd.xvel = smbd.speed
            smbd.yvel = 0


def smth_in_inventary(type2):
    """check if some object is in inventary"""
    r = False
    for i in inventary:
        if i.type1 == type2:
            r = True
    return r


class SolidObject(sprite.Sprite):
    """parent class for all fixed objects"""
    def __init__(self, x, y, path):
        sprite.Sprite.__init__(self)
        self.rect = pygame.rect.Rect(x, y, PLATWIDTH, PLATHEIGHT)
        self.image = pygame.image.load(path)

    def action(self):
        pass


"""all fixed objects. begin"""
class Wall(SolidObject):
    pass


class Tree(SolidObject):
    pass


class LifeBlock(SolidObject):
    def action(self):
        if LIFE < 20:
            LIFE += 1
            self.kill()


class Coin(SolidObject):
    def action(self):
        global MONEY
        MONEY += 1
        self.kill()


class Bed(SolidObject):
    def action(self):
        global LIFE, sleep
        if sleep:
            print('sleep...')
            pygame.time.delay(200)
            imga = pygame.image.load('img/sleep.png')
            imgarect = imga.get_rect()
            screen.blit(imga, imgarect)
            pygame.display.flip()
            pygame.time.delay(4000)
            LIFE = 20
            sleep = False


class PlatExit(SolidObject):
    def action(self):
        if smth_in_inventary('sword'):
            global LEVUP, LEVEL
            pygame.time.delay(300)
            LEVUP = True
            LEVEL += 1
        else:
            say('Dangerous', 'img/text/dangerous.gif')


class PlatLevelDown(SolidObject):
    def action(self):
        global LEVDOWN, LEVEL
        LEVEL -= 1
        LEVDOWN = True


class NPC(SolidObject):
    def action(self):
        global talk
        if talk:
            global LEVEL
            say('advice', 'img/text/text' + str(LEVEL) + '.gif')
            talk = False
"""solid objects. end"""


class Monster(sprite.Sprite):
    """very peaceful monster, just RUNNING. attack, only if was attacked"""
    def __init__(self, x, y, path):
        sprite.Sprite.__init__(self)
        self.StartX = x
        self.StartY = y
        self.speed = 3
        self.life = 6
        self.power = 1
        self.xvel = 0
        self.yvel = -2
        self.image = pygame.image.load(path)
        self.rect = pygame.rect.Rect(x, y, PLATWIDTH, PLATHEIGHT)

    def move(self, ENTITIES):
        global LIFE
        for f in ENTITIES:
            if ((sprite.collide_rect(self, f))
                and isinstance(f, Player) and attack):
                if attack:
                    print('Monster hits player: ', self.power)
                    pygame.time.delay(50)
                    self.xvel = 0
                    self.yvel = 0
                    LIFE -= self.power
        self.collide(self.xvel, 0, ENTITIES)
        self.rect.x += self.xvel
        self.collide(0, self.yvel, ENTITIES)
        self.rect.y += self.yvel

    def collide(self, xvel, yvel, ENTITIES):
        for f in ENTITIES:
            if (sprite.collide_rect(self, f)) and not(isinstance(f, Player))\
                                            and not(isinstance(f, LifeBlock)):
                collide_the_wall(self, f, xvel, yvel)


class RealObject(sprite.Sprite):
    """things, that will be in hero's inventary"""
    def __init__(self, x, y, path, type1):
        sprite.Sprite.__init__(self)
        self.type1 = type1
        self.image = pygame.image.load(path)
        self.rect = pygame.rect.Rect(x, y, PLATWIDTH, PLATHEIGHT)

    def invent_append(self, type1):
        if not(smth_in_inventary(type1)):
            print(self)
            inventary.append(self)
            self.kill()


class CAMERA(object):
    def __init__(self, CAMERA_func, width, height):
        self.CAMERA_func = CAMERA_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self,target):
        self.state = self.CAMERA_func(self.state, target.rect)


def CAMERA_configure(CAMERA, target_rect):
    left, t, _, _ = target_rect
    _, _, w, h = CAMERA
    left, t = -left + SCREENWIDTH / 2, -t + SCREENHEIGHT/2
    left = min(0, left)
    left = max(-(CAMERA.width - SCREENWIDTH), left)
    t = min(0, t)
    t = max(-(CAMERA.height - SCREENHEIGHT), t)
    return Rect(left, t, w, h)


#define pictures of hero
Animation_Delay = 0.1
Animation_Attack = [('img/startHero/heroW1.png'),
                    ('img/startHero/heroAtt.png')]
Animation_Down = [('img/startHero/heroW2.png'),
                  ('img/startHero/heroW3.png')]
Animation_Stay = [('img/startHero/heroW1.png', Animation_Delay)]
Animation_Right = [('img/startHero/heroR1.png'),
                   ('img/startHero/heroR2.png'),
                   ('img/startHero/heroR3.png')]
Animation_Left = [('img/startHero/heroL1.png'),
                   ('img/startHero/heroL2.png'),
                   ('img/startHero/heroL3.png')]


class Player(sprite.Sprite):
    def __init__(self, x, y, power):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.speed = 4
        selfStartX = x
        selfStartY = y
        self.power = power
        self.image = Surface((WIDTH, HEIGHT))
        self.rect = pygame.rect.Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(BACKGROUND)

        #define animation of player; use pyganim
        boltAnim = []
        for anim in Animation_Down:
            boltAnim.append((anim, Animation_Delay))
        self.boltAnimDown = pyganim.PygAnimation(boltAnim)
        self.boltAnimDown.play()

        boltAnim = []
        self.boltAnimStay = pyganim.PygAnimation(Animation_Stay)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))

        boltAnim = []
        for anim in Animation_Right:
            boltAnim.append((anim, Animation_Delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()

        boltAnim = []
        for anim in Animation_Left:
            boltAnim.append((anim,Animation_Delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        self.image.fill(BACKGROUND)

        boltAnim = []
        for anim in Animation_Attack:
            boltAnim.append((anim,Animation_Delay * 5))
        self.boltAnimAttack = pyganim.PygAnimation(boltAnim)
        self.boltAnimAttack.play()
        self.image.fill(BACKGROUND)

    def update(self, left, right, up, down, PLATFORMS):
        self.image.fill(BACKGROUND)
        for m in MONSTERS:
            if sprite.collide_rect(self, m) and attack:
                print('Player hits monster: ', self.power)
                m.life -= self.power
                pygame.time.delay(50)
                if m.life < 1:
                    m.kill()
                    pf = Coin(m.rect.x-15, m.rect.y-15, 'img/coin.png')
                    ENTITIES.add(pf)

        if left:
            self.xvel = -self.speed
            self.boltAnimLeft.blit(self.image, (0, 0))
        elif right:
            self.xvel = self.speed
            self.boltAnimRight.blit(self.image, (0, 0))
        elif up:
            self.yvel = -self.speed
            self.boltAnimDown.blit(self.image, (0, 0))
        elif down:
            self.yvel = self.speed
            self.boltAnimDown.blit(self.image, (0, 0))
        if attack:
            self.xvel = 0
            self.boltAnimAttack.blit(self.image, (0, 0))
        if not(left or right or up or down or attack):
            self.xvel = 0
            self.yvel = 0
            self.boltAnimStay.blit(self.image, (0, 0))

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, PLATFORMS)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, PLATFORMS)

    def collide(self, xvel, yvel, PLATFORMS):
        for e in ENTITIES:
            if sprite.collide_rect(self, e):
                """special collides, not tree and wall"""
                if isinstance(e, SolidObject):
                    e.action()
                elif isinstance(e, RealObject):
                    e.invent_append(e.type1)
                if not(isinstance(e, Player)):
                    collide_the_wall(self, e, xvel,yvel)


def generateHero(x, y):
    """this function generate hero near door to previous or next LEVEL
    door to previous LEVEL has x == 0
    door to next LEVEL has x == SreenWidth
    if y is too big (bigger than 300) hero can spawn on tree"""
    global hero
    if x == 0:
        x1 = 100
    else:
        x1 = x - 100

    if y > 300:
        y1 = y - 10
    else:
        y1 = y + 10

    if smth_in_inventary('sword'):
        hero = Player(x1, y1, 4)
    else:
        hero = Player(x1, y1, 2)
    ENTITIES.add(hero)


def generate():
    global MONSTERS, ENTITIES, PLATFORMS, CAMERA
    MONSTERS = pygame.sprite.Group()
    ENTITIES = pygame.sprite.Group()
    PLATFORMS = []
    x = y = 0
    """ open file with next or previous LEVEL, initial all object;
    add them in ENTITIES; objects, that will be on map whole of
    game, will be pushed in PLATFORMS to check if hero collide them"""
    with open('levels\level' + str(LEVEL) + '.txt') as f:
        for row in f:
            for col in row:
                if col == '&': # sword
                    pf = RealObject(x, y, 'img/sword1.png', 'sword')
                    ENTITIES.add(pf)
                elif col == 'P': # npc
                    pf = NPC(x, y, 'img/npc/npc' + str(LEVEL) + '.png')
                    ENTITIES.add(pf)
                    PLATFORMS.append(pf)
                elif col == 'S': # bed
                    pf = Bed(x, y, 'img/bed.png')
                    ENTITIES.add(pf)
                    PLATFORMS.append(pf)
                elif col == '%': # life
                    pf = LifeBlock(x+10, y+10, 'img/life.png')
                    ENTITIES.add(pf)
                elif col == '-': # tree
                    pf = Tree(x, y, 'img/tree.png')
                    PLATFORMS.append(pf)
                    ENTITIES.add(pf)
                elif col == '/':  # levelUp, door to next LEVEL
                    pf = PlatExit(x, y, 'img/exit.png')
                    PLATFORMS.append(pf)
                    ENTITIES.add(pf)
                    if LEVDOWN:
                    # if we return from previous LEVEL,
                    # we spawn near door to next LEVEL
                        generateHero(x,y)
                elif col == '!':  #levelDown, door to previous LEVEL
                    # on first LEVEL there isn't door on previous
                    # LEVEL so we need add 2 trees instead of it
                    if LEVEL != 1:
                        pf = PlatLevelDown(x, y, 'img/exit.png')
                        PLATFORMS.append(pf)
                        ENTITIES.add(pf)
                    else:
                        pf = Tree(x, y, 'img/tree.png')
                        PLATFORMS.append(pf)
                        ENTITIES.add(pf)
                        pf = Tree(x, y+50, 'img/tree.png')
                        PLATFORMS.append(pf)
                        ENTITIES.add(pf)
                    if LEVUP:
                        # if we goint to next LEVEL,
                        # we spawn near door to previous LEVEL
                        generateHero(x, y)
                elif col == 'D':  # walls of house
                    pf = Wall(x, y, 'img/wall.png')
                    PLATFORMS.append(pf)
                    ENTITIES.add(pf)
                elif col == '*': # mobs
                    pf = Monster(x, y, 'img/monster.png')
                    MONSTERS.add(pf)
                x += PLATWIDTH
            y += PLATHEIGHT
            x = 0

    CAMERA = CAMERA(CAMERA_configure, len(row) * PLATWIDTH, y)


LEVUP = True
generate()
LEVUP = False
timer = pygame.time.Clock()
left = right = up = down = attack = sleep = talk = False
say('advice', 'img/text/text0.gif')

while RUNNING:
# right now, while window isn't closed
    if LEVUP or LEVDOWN:
        generate()
        LEVUP = LEVDOWN = False
        print('------------------')
    for m in MONSTERS:
        m.move(ENTITIES)
    if Animation_Down[1] != 'img/swordHero/heroW3.png':
        if smth_in_inventary('sword'):
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
            hero.__init__(hero.rect.x, hero.rect.y, 4)

    timer.tick(60)
    screen.fill(BACKGROUND)
    CAMERA.update(hero)
    hero.update(left, right, up, down, PLATFORMS)
    for e in ENTITIES:
        screen.blit(e.image, CAMERA.apply(e))
    for m in MONSTERS:
        screen.blit(m.image, CAMERA.apply(m))
    pygame.display.set_caption('Level ' + str(LEVEL) +\
                            ' life ' + str(LIFE) + ' money ' + str(MONEY))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
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
                elif event.key == K_F1:
                    say('Pause', 'img/text/pause.gif')

        if event.type == KEYUP:
            if event.key == K_UP:
                up = False
            elif event.key == K_DOWN:
                down = False
            elif event.key == K_LEFT:
                left = False
            elif event.key == K_RIGHT:
                right = False
            elif event.key == K_a:
                attack = False
    pygame.display.flip()
pygame.display.quit()
