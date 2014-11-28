# ! - do in right now; P - programming; L - logic
#P TODO: module solid object, monsters, hero etc
#P TODO: like tkinter.Tk() but without interruption
#! TODO: hero's name
#! TODO: basic attributes (strength, fallout system?) and make them better (strength-ups)
#! TODO: quests!!!!11!1
#! TODO: door with key, npc sell key; puzzles; button whick opens door(?)
#  TODO: dragon-boss
#  TODO: graphics like Starcraft
#  TODO: not only sword
#  TODO: different classes
#L TODO: not only peaceful mobs
#PL FIXED: battles like normal battles
#L TODO: random mobs' bites; random hit...
#L TODO: good dialogs with npc, make your choice
#P TODO: new program for generating pixel text
#  TODO: mobs spawner
#  TODO: use tactics
#! TODO: make you character by yourself; fallout system?
#  TODO: levels not in line (bonus levels?); make your choice
#  TODO: more things in inventary
#  TODO: chest with...
#  TODO: traps, poison...
#  TODO: moar information
#  TODO: make wiki choice: narrative RPG or Dungeon crawler; mass effect of diablo
import tkinter

import pygame
import pyganim

import camera

from pygame import *

pygame.init()
WIDTH = 95
HEIGHT = 100
SCREENWIDTH = 900
SCREENHEIGHT = 600
PLATWIDTH = PLATHEIGHT = 50
BACKGROUND = ((250,250,250)) 
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
inventary = []
level_up = False
level_down = False
running = level = 1


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


def main_attr(hero):
    def strength(root):
        hero.strength += 1
    def agility(root):
        hero.agility += 1
    def intelligence(root):
        hero.intelligence += 1
    def luck(root):
        hero.luck += 1
    root = tkinter.Tk()
    root.geometry('+500+300')
    root.title('Choose')
    label1 = tkinter.Label(root, text='Choose your main attribute')
    button1 = tkinter.Button(root, text='strength', command=root.destroy)
    button2 = tkinter.Button(root, text='agility', command=root.destroy)
    button3 = tkinter.Button(root, text='intelligence', command=root.destroy)
    button4 = tkinter.Button(root, text='luck', command=root.destroy)
    label1.pack()
    button1.pack()
    button1.bind('<Button-1>',strength)
    button2.pack()
    button2.bind('<Button-1>',agility)
    button3.pack()
    button3.bind('<Button-1>',intelligence)
    button4.pack()
    button4.bind('<Button-1>',luck)
    root.mainloop()


def collide_the_wall(smbd, wall, xvel, yvel):
    """function for check, if smbd collide the wall(or other object);
    xvel, yvel - direction of moving"""
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
class LifeBlock(SolidObject):
    def action(self):
        global hero
        if hero.life < 20:
            hero.life += 1
            self.kill()


class Coin(SolidObject):
    def action(self):
        global hero
        hero.money += 10
        self.kill()


class Bed(SolidObject):
    def action(self):
        global hero, doing
        if doing:
            print('sleep...')
            pygame.time.delay(200)
            imga = pygame.image.load('img/text/sleep.png')
            imgarect = imga.get_rect()
            screen.blit(imga, imgarect)
            pygame.display.flip()
            pygame.time.delay(4000)
            hero.life = 20
            doing = False


class PlatExit(SolidObject):
    def action(self):
        if smth_in_inventary('sword'):
            global level_up, level
            pygame.time.delay(300)
            level_up = True
            level += 1
        else:
            say('Dangerous', 'img/text/dangerous.gif')


class PlatLevelDown(SolidObject):
    def action(self):
        global level_down, level
        level -= 1
        level_down = True


class NPC(SolidObject):
    def action(self):
        global doing
        if doing:
            global level
            say('advice', 'img/text/text' + str(level) + '.gif')
            doing = False
"""solid objects. end"""


class Monster(sprite.Sprite):
    """very peaceful monster, just running. attack, only if was attacked"""
    def __init__(self, x, y, path):
        sprite.Sprite.__init__(self)
        self.StartX = x
        self.StartY = y
        self.speed = 3
        self.life = 6
        self.strength = 1
        self.xvel = 0
        self.yvel = -2
        self.image = pygame.image.load(path)
        self.rect = pygame.rect.Rect(x, y, PLATWIDTH, PLATHEIGHT)

    def move(self, entities):
        global hero
        for f in entities:
            if ((sprite.collide_rect(self, f))
                and isinstance(f, Player) and attack):
                if attack:
                    print('Monster hits player: ', self.strength)
                    pygame.time.delay(50)
                    self.xvel = 0
                    self.yvel = 0
                    hero.life -= self.strength
        self.collide(self.xvel, 0, entities)
        self.rect.x += self.xvel
        self.collide(0, self.yvel, entities)
        self.rect.y += self.yvel

    def collide(self, xvel, yvel, entities):
        for f in entities:
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
            inventary.append(self)
            self.kill()
            global hero
            hero.strength += 2
            hero.anim()


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0
        self.yvel = 0
        selfStartX = x
        selfStartY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.rect = pygame.rect.Rect(x, y, WIDTH, HEIGHT)
        self.image.set_colorkey(BACKGROUND)

    def define(self,strength,agility,intelligence,luck):
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.luck = luck
        self.speed = 4
        self.xp = 0
        self.level = 1
        self.life = 20
        self.money = 0

    def hero_level(self):
        if self.xp >= self.level*20:
            self.level += 1
            self.xp = 0

    def anim(self):
        Animation_Delay = 0.1
        if not(smth_in_inventary('sword')):
            Animation_Down = [('img/startHero/heroW2.png'),
                              ('img/startHero/heroW3.png')]
            Animation_Stay = [('img/startHero/heroW1.png', Animation_Delay)]
            Animation_Right = [('img/startHero/heroR1.png'),
                               ('img/startHero/heroR2.png'),
                               ('img/startHero/heroR3.png')]
            Animation_Left = [('img/startHero/heroL1.png'),
                               ('img/startHero/heroL2.png'),
                               ('img/startHero/heroL3.png')]
            Animation_Attack = [('img/startHero/heroW1.png'),
                                ('img/startHero/heroAtt.png')]
        else:
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

    def update(self, left, right, up, down, platforms):
        self.hero_level()
        self.image.fill(BACKGROUND)
        for m in monsters:
            if sprite.collide_rect(self, m) and attack:
                print('Player hits monster: ', self.strength)
                m.life -= self.strength
                pygame.time.delay(50)
                if m.life < 1:
                    m.kill()
                    self.xp += 10
                    pf = Coin(m.rect.x-15, m.rect.y-15,
                              'img/SolidObjects/coin.png')
                    entities.add(pf)

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
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for e in entities:
            if sprite.collide_rect(self, e):
                """special collides, not tree and wall"""
                if isinstance(e, SolidObject):
                    e.action()
                elif isinstance(e, RealObject):
                    e.invent_append(e.type1)
                if not(isinstance(e, Player)):
                    collide_the_wall(self, e, xvel,yvel)


def generate_hero(x, y):
    """this function generate hero near door to previous or next level
    door to previous level has x == 0
    door to next level has x == SreenWidth
    if y is too big (bigger than 300) hero can spawn on tree"""
    global hero
    if x == 0:
        x1 = 100
    else:
        x1 = x - 100

    if y > 300: #FIXEDME: wrong logic?
        y1 = y - 10
    else:
        y1 = y + 10

    if level == 1 and level_up:
        hero = Player(x1, y1)
    else:
        hero.selfStartX = x1
        hero.selfStartY = y1
        hero.xvel = 0
        hero.yvel = 0
        hero.rect = pygame.rect.Rect(x1, y1, WIDTH, HEIGHT)
    entities.add(hero)
    hero.anim()


def generate():
    global monsters, entities, platforms, camera_, back_image
    monsters = pygame.sprite.Group()
    entities = pygame.sprite.Group()
    platforms = []
    x = y = 0
    """ open file with next or previous level, initial all object;
    add them in entities; objects, that will be on map whole of
    game, will be pushed in platforms to check if hero collide them"""
    with open('levels\level' + str(level) + '.txt') as f:
        for row in f:
            for col in row:
                if col == '&': # sword
                    pf = RealObject(x, y, 'img/RealObjects/sword1.png', 'sword')
                    entities.add(pf)
                elif col == 'P': # npc
                    pf = NPC(x, y, 'img/npc/npc' + str(level) + '.png')
                    entities.add(pf)
                    platforms.append(pf)
                elif col == 'S': # bed
                    pf = Bed(x, y, 'img/SolidObjects/bed.png')
                    entities.add(pf)
                    platforms.append(pf)
                elif col == '%': # life
                    pf = LifeBlock(x+10, y+10, 'img/SolidObjects/life.png')
                    entities.add(pf)
                elif col == '-': # tree
                    pf = SolidObject(x, y, 'img/SolidObjects/tree.png')
                    platforms.append(pf)
                    entities.add(pf)
                elif col == '/':  # level_up, door to next level
                    pf = PlatExit(x, y, 'img/SolidObjects/exit.png')
                    platforms.append(pf)
                    entities.add(pf)
                    if level_down:
                    # if we return from previous level,
                    # we spawn near door to next level
                        generate_hero(x,y)
                elif col == '!':  #level_down, door to previous level
                    # on first level there isn't door on previous
                    # level so we need add 2 trees instead of it
                    if level != 1:
                        pf = PlatLevelDown(x, y, 'img/SolidObjects/exit.png')
                        platforms.append(pf)
                        entities.add(pf)
                    else:
                        pf = SolidObject(x, y, 'img/SolidObjects/tree.png')
                        platforms.append(pf)
                        entities.add(pf)
                        pf = SolidObject(x, y+50, 'img/SolidObjects/tree.png')
                        platforms.append(pf)
                        entities.add(pf)
                    if level_up or level == 1:
                        # if we goint to next level,
                        # we spawn near door to previous level
                        generate_hero(x, y)
                elif col == 'D':  # walls of house
                    pf = SolidObject(x, y, 'img/SolidObjects/wall.png')
                    platforms.append(pf)
                    entities.add(pf)
                elif col == '#': #water
                    pf = SolidObject(x, y, 'img/SolidObjects/water.png')
                    platforms.append(pf)
                    entities.add(pf)
                elif col == '*': # mobs
                    pf = Monster(x, y, 'img/monsters/monster.png')
                    monsters.add(pf)
                x += PLATWIDTH
            y += PLATHEIGHT
            x = 0

    camera_ = camera.Camera(camera.camera_configure, len(row) * PLATWIDTH, y)
    path = "img/background/img" + str(level) + ".png"
    back_image = camera.BackImage(path)


level_up = True
generate()
timer = pygame.time.Clock()
level_up = left = right = up = down = attack = doing = False
say('advice', 'img/text/text0.gif')
hero.define(2,5,5,5)
main_attr(hero)

while running:
# right now, while window isn't closed
    if level_up or level_down:
        generate()
        level_up = level_down = False
        print('------------------')
    if not(hero.life):
        say('Dead','img/text/dead.gif')
        level = 2
        generate()
    for m in monsters:
        m.move(entities)
    timer.tick(60)
    hero.update(left, right, up, down, platforms)
    camera_.update(hero)
    back_image.show(camera_, screen)
    for e in entities:
        screen.blit(e.image, camera_.apply(e))
    for m in monsters:
        screen.blit(m.image, camera_.apply(m))
    pygame.display.set_caption('Level ' + str(level) +\
                            ' life ' + str(hero.life) + ' money ' +\
                            str(hero.money) + ', level: '+ str(hero.level) +\
                            ', xp: ' + str(hero.xp) +\
                            ', Attributes: strength - ' + str(hero.strength) +\
                            ', agility - ' + str(hero.agility) + ', luck - ' +\
                            str(hero.luck) + ', intelligence - ' +\
                            str(hero.intelligence) )

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = 0
        if not(up or down or right or left or attack):
            if event.type == KEYDOWN:
                if event.key == K_UP  or event.key == K_w:
                    up = True
                elif event.key == K_LEFT or event.key == K_a:
                    left = True
                elif event.key == K_DOWN or event.key == K_s:
                    down = True
                elif event.key == K_RIGHT or event.key == K_d:
                    right = True
                elif event.key == K_f:
                    attack = True
                elif event.key == K_e:
                    doing = True
                elif event.key == K_F1:
                    say('Pause', 'img/text/pause.gif')

        if event.type == KEYUP:
            if event.key == K_UP or event.key == K_w:
                up = False
            elif event.key == K_LEFT or event.key == K_a:
                left = False
            elif event.key == K_DOWN or event.key == K_s:
                down = False
            elif event.key == K_RIGHT or event.key == K_d:
                right = False
            elif event.key == K_f:
                attack = False
    pygame.display.flip()
pygame.display.quit()
