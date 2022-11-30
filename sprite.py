import pygame as pg
from settings import *
import random

# https://www.pygame.org/wiki/Spritesheet
class SpriteSheet():
    def __init__(self, filename):
        try:
            self.sheet = pg.image.load(filename).convert()
        except pg.error:
            print('Unable to load spritesheet image:'), filename
            raise SystemExit

    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        # "Loads image from x,y,x+offset,y+offset"
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image

    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]

    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

class UISprite(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super(UISprite, self).__init__()
        self.image = pg.Surface([w, h])
        self.image.fill((0,255,0))
        self.image.set_colorkey((0,0,0))

        pg.draw.rect(self.image, (0,255,0), pg.Rect(x,y,w,h))
        self.rect = pg.Rect(x,y,w,h)



class GameSprite(pg.sprite.Sprite):
    def __init__(self, ss, which, x, y, clock):
        super(GameSprite, self).__init__()

        self.which = which
        self.ss = ss
        self.clock = clock
        self.elapsed = 0
        self.images = []

        self.target = (x, y)

        self.complete = False
        self.timer = 10
        self.points = 1

        if which == 'blob':
            self.images = self.ss.images_at(
                [(0, 64, SPRITE_SIZE, SPRITE_SIZE), 
                (16, 64, SPRITE_SIZE, SPRITE_SIZE), 
                (32, 64, SPRITE_SIZE, SPRITE_SIZE)], 
                colorkey=(255, 255, 255)
            )
        elif which == 'bat':
            self.timer = 5
            self.points = 10
            self.images = self.ss.images_at(
                [(48, 64, SPRITE_SIZE, SPRITE_SIZE), 
                (64, 64, SPRITE_SIZE, SPRITE_SIZE), 
                (80, 64, SPRITE_SIZE, SPRITE_SIZE)], 
                colorkey=(255, 255, 255)
            )
        
        elif which == 'dino':
            self.timer = 15
            self.points = 20
            self.images = self.ss.images_at(
                [
                    (0, 0, 24, 24),
                    (24, 0, 24, 24),
                    (48, 0, 24, 24),
                    (72, 0, 24, 24),
                    (96, 0, 24, 24),
                    (120, 0, 24, 24),
                    (144, 0, 24, 24),
                    (168, 0, 24, 24),
                    (192, 0, 24, 24),
                ],
                # colorkey=(0,0,0)
                colorkey=(255,255,255)
            )

        self.index = 0
        self.images = [pg.transform.scale(s, (SPRITE_SIZE*2, SPRITE_SIZE*2)) for s in self.images]
        self.image = self.images[self.index]
        self.rect = pg.Rect(x, y, SPRITE_SIZE*2, SPRITE_SIZE*2)

    def update(self):
        ticks = pg.time.get_ticks()
        if ticks - self.elapsed > SPRITE_ANIM_TICK:
            self.elapsed = ticks
            self.index += 1

            if self.index >= len(self.images):
                self.index = 0
            
            self.image = self.images[self.index]

            # movement
            if not self.complete:
                dx = self.target[0] - self.rect.x
                dy = self.target[1] - self.rect.y

                self.rect.x += dx * EASING 
                self.rect.y += dy * EASING 

                if random.random() > 0.95 or (dx < 1 and dy < 1):
                    self.target = (random.randint(0,WIDTH-SPRITE_SIZE-1), random.randint(0,HEIGHT-SPRITE_SIZE-1))

    def update_position(self, pos):
        if not self.complete:
            self.rect.x = pos[0] - SPRITE_SIZE
            self.rect.y = pos[1] - SPRITE_SIZE # was half - scaling up means this val needs to double

    def check_click(self, pos):
        if not self.complete and self.rect.collidepoint(pos):
            return True
