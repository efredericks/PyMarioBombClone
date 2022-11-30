# kenney.nl assets: https://kenney.nl/assets/jumper-pack
# tiny 16 assets: https://opengameart.org/content/tiny-16-basic
# dino: https://arks.itch.io/dino-characters
# sprite animation: https://www.simplifiedpython.net/pygame-sprite-animation-tutorial/

import pygame as pg
from sprite import *
from settings import *
import random
import pytmx


mouseDown = False
mousePos = None
dragActive = False
movingSprite = None
paused = False
font = None
level = 1
score = 0

def exit():
    pg.quit()
    quit()

def drawUI(screen, font, level, score):
    # pg.draw.rect(screen, (20,20,20,20), pg.Rect(0,0,WIDTH,FONT_SIZE))

    top_bar = font.render("Level: {0} // Score: {1}".format(level, score), True, (220, 220, 220))
    top_bar_rect = top_bar.get_rect()#center=(WIDTH/2, FONT_SIZE/2))
    top_bar_rect.x += 10 
    top_bar_rect.y += 5
    screen.blit(top_bar, top_bar_rect)



if __name__ == "__main__":
    pg.init()
    screen = pg.display.set_mode(SIZE, pg.HWSURFACE | pg.DOUBLEBUF)# | pg.RESIZABLE)
    clock = pg.time.Clock()

    # font
    font = pg.font.Font("./assets/nokiafc22.ttf", FONT_SIZE)

    # spritesheet
    ss = SpriteSheet('./assets/characters.png')
    blobs = [GameSprite(ss, 'blob', random.randint(0,WIDTH-SPRITE_SIZE-1), random.randint(0,HEIGHT-SPRITE_SIZE-1), clock) for _ in range(10)]
    bat = GameSprite(ss, 'bat', 32, 32, clock)
    win = UISprite(WIDTH-100,HEIGHT-100,100,100)

    ss2 = SpriteSheet('./assets/dinoCharactersVersion1.1/sheets/DinoSprites - doux.png')
    dino = GameSprite(ss2, 'dino', 64, 64, clock)

    sprite_group = pg.sprite.Group(blobs, bat, dino)
    ui_sprite_group = pg.sprite.Group(win)

    # map
    map_ss = SpriteSheet('./assets/roguelike-pack-kenney/Spritesheet/roguelikeSheet_transparent.png')

    map_imgs = map_ss.images_at(
        [(170, 119, 16, 16), #tl
         (187, 119, 16, 16), #t
         (204, 119, 16, 16), #tr
         (170, 136, 16, 16), #l
         (187, 136, 16, 16), #m
         (204, 136, 16, 16), #r
         (170, 153, 16, 16), #bl
         (187, 153, 16, 16), #bm
         (204, 153, 16, 16), #br
        ],
    ) 
    gameMap = [[4 for c in range(NUM_COLS)] for r in range(NUM_ROWS)] 
    for r in range(NUM_ROWS):
        for c in range(NUM_COLS):
            val = 4
            if r == 0 and c == 0: val = 0
            elif r == 0 and c == NUM_COLS-1: val = 2
            elif r == 0: val = 1
            elif r == NUM_ROWS-1 and c == 0: val = 6
            elif r == NUM_ROWS-1 and c == NUM_COLS-1: val = 8
            elif c == 0: val = 3
            elif c == NUM_COLS-1: val = 5
            elif r == NUM_ROWS-1: val = 7
#            else:
#                if random.randint() > 0.7:
#                    val = 
            gameMap[r][c] = val

    while True:
        pg.display.set_caption("PyBomb - FPS: {0}".format(int(clock.get_fps())))

        scr_width, scr_height = screen.get_size()

        mousePos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            # if event.type == pg.VIDEORESIZE:
            #     screen = pg.display.set_mode(event.dict['size'], pg.HWSURFACE | pg.DOUBLEBUF | pg.RESIZABLE)
            #     new_scr_width, new_scr_height = screen.get_size()
            #     print(scr_width, scr_height, new_scr_width, new_scr_height)


            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    paused = not paused
                if event.key == pg.K_ESCAPE:
                    exit()


            if event.type == pg.MOUSEBUTTONDOWN:
                mp = pg.mouse.get_pressed()
                if mp[0]:
                    mouseDown = True
                # debug
                if mp[1]:
                    exit()

            if not paused: 
                if event.type == pg.MOUSEBUTTONUP:
                    mouseDown = False
                    dragActive = False
                    movingSprite = None

                    # check for collision with a UI element
                    #for s in sprite_group:
                    for s in ui_sprite_group:
                        hit_list = pg.sprite.spritecollide(s, sprite_group, True)
                        if hit_list:
                        #if pg.sprite.spritecollide(s, ui_sprite_group, False):
                            hit_list[0].complete = True
                            score += hit_list[0].points
                            #s.complete = True
                            #score += s.points

        if mouseDown and not paused:
            # print("Mouse: {0}".format(mousePos))
            if not dragActive:
                for s in sprite_group:
                    dragActive = s.check_click(mousePos)
                    if dragActive:
                        movingSprite = s
                        break


        if dragActive and not paused:
            movingSprite.update_position(mousePos)


        if not paused:
            for s in sprite_group:
                if movingSprite is not s:
                    s.update()
            # screen.fill(BACKGROUND)

            for r in range(NUM_ROWS):
                for c in range(NUM_COLS):
                    screen.blit(map_imgs[gameMap[r][c]], pg.Rect(c*SPRITE_SIZE, r*SPRITE_SIZE, SPRITE_SIZE, SPRITE_SIZE))


            drawUI(screen, font, level, score)
            ui_sprite_group.draw(screen)
            sprite_group.draw(screen)
            pg.display.update()

        clock.tick(FPS)

        if len(sprite_group) == 0:
            exit()


