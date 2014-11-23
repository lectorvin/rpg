"""This module descibe camera as class Camera. Camera is used 
for showing world around hero, if this world is larger, than
(SCREENWIDHT, SCREENHEIGHT). Also, here you can find class BackImage,
which is used for showing background image
"""

import pygame

pygame.init()
SCREENWIDTH = 900
SCREENHEIGHT = 600


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
        
    def apply(self, target):
        try:
            return target.rect.move(self.state.topleft)
        except AttributeError:
            return tuple(map(sum, zip(target, self.state.topleft)))

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


class BackImage(object):
    def __init__(self, path):
        self.image = pygame.image.load(path).convert()

    def show(self, camera, screen):
        screen.blit(self.image, camera.apply((0,0)))


def camera_configure(camera, target_rect):
    left, t, _, _ = target_rect
    _, _, w, h = camera
    left, t = -left + SCREENWIDTH/2, -t + SCREENHEIGHT/2
    left = min(0, left)
    left = max(-(camera.width - SCREENWIDTH), left)
    t = min(0, t)
    t = max(-(camera.height - SCREENHEIGHT), t)
    return pygame.Rect(left, t, w, h)
