import pygame

from pygame import *


pygame.init()
SCREENWIDTH = 900
SCREENHEIGHT = 600

class Camera(object):
    def __init__(self, CAMERA_func, width, height):
        self.CAMERA_func = CAMERA_func
        self.state = Rect(0, 0, width, height)
        
    def apply(self,target):
        try:
            return target.rect.move(self.state.topleft)
        except:
            return tuple(map(sum, zip(target, self.state.topleft)))

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
