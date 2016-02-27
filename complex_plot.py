import argparse
import sys
from math import *

import pygame
from pygame.locals import DOUBLEBUF, K_ESCAPE, KEYDOWN, QUIT


def math2pygame(x, y):
    scalex = SDL_XMAX/float(XMAX - XMIN)
    scaley = SDL_YMAX/float(YMAX - YMIN)
    minx = scalex*XMIN
    miny = scaley*YMAX

    # print "Point : ",x, y
    # print "Mins : ", minx, miny
    # print "Scale : ", scalex, scaley
    # print "Scaled points ", scalex*x, scaley*y
    # print "Mins ", minx, miny


    gx = scalex*x - minx
    gy = miny - scaley*y
    # print "Adjusted scaled points ", gx, gy
    # print "---"*20
    return gx, gy


def draw_axes(surface, xmin, xmax, ymin, ymax):
    s1, s2 = math2pygame(xmin, 0), math2pygame(0, ymin)
    e1, e2 = math2pygame(xmax, 0), math2pygame(0, ymax)
    pygame.draw.line(surface, (0, 100, 0), s1, e1, 1)
    pygame.draw.line(surface, (0, 100, 0), s2, e2, 1)
    # pygame.draw.line(surface, (0, 255, 0), math2pygame(xmin, ymin), math2pygame(xmax, ymax), 1)

class Panel(pygame.sprite.Sprite):
    def __init__(self, val, groups):
        super(Panel, self).__init__(groups)
        self.font = pygame.font.Font("jGara2.ttf", 20)
        self.image = pygame.Surface((100,25)).convert_alpha()
        self.image.fill((0,10,0))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (SDL_XMAX, SDL_YMAX)
        self.val = val
        info = self.font.render(val, True,(20,200,20))
        self.image.fill((0,10,0,255))
        self.image.blit(info,(0,0))

    def update(self):
        info = self.font.render(self.val, True,(20,200,20))
        self.image.fill((0,10,0,255))
        self.image.blit(info,(0,0))


class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, groups):
        super(Point,self).__init__(groups)
        self.image = pygame.Surface((1,1))
        pygame.draw.circle(self.image, 
                           colour,
                           (1,1),
                           1,
                           1)
        self.rect = self.image.get_rect()
        u,v = math2pygame(x, y)
        self.rect.center = (u,v)
        
        # print "{:.04},{:.04} :: {:.04},{:.04}".format(x,y, *math2pygame(x, y))
        self.c = colour
    def update(self):
        pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--winsize", dest = "winsize", default = "600x600", help = "Size of window")
    parser.add_argument("--min", dest = "min", default = "-1x-1", help = "Min point of grid")
    parser.add_argument("--max", dest = "max", default = "1x1", help = "Max point of grid")
    parser.add_argument("--function", dest = "function", help = "Function to plot")
    parser.add_argument("--start", dest = "start", action = "store", type = float, 
                        help = "Start plotting from")
    parser.add_argument("--stop", dest = "stop", action = "store", type = float, 
                        help = "Stop plotting at")
    parser.add_argument("--seed", dest = "seed", action = "store", type = str,
                        help = "Point whose orbit to plot")

    args = parser.parse_args()
    args.winsize = [int(x) for x in args.winsize.split("x")]
    args.min = [float(x) for x in args.min.split("x")]
    args.max = [float(x) for x in args.max.split("x")]
    args.function = eval("lambda x : {}".format(args.function)) 
    return args


def main():
    global SDL_XMAX
    global SDL_YMAX
    global XMIN
    global YMIN
    global XMAX
    global YMAX

    args = parse_args()
    SDL_XMAX, SDL_YMAX = args.winsize
    XMIN, YMIN = args.min
    XMAX, YMAX = args.max

    # math2pygame(-2,0)
    # math2pygame(0,0)
    # print "{} - {}".format((XMIN, YMIN), math2pygame(XMIN, YMIN))
    # print ""
    # print "{} - {}".format((XMAX, YMAX), math2pygame(XMAX, YMAX))
    # assert math2pygame(XMIN, YMIN) == 0,SDL_YMAX
    # sys.exit()

    
    screen = pygame.display.set_mode((SDL_XMAX, SDL_YMAX), DOUBLEBUF)
    pygame.font.init()
    screen.fill((0,10,0))
    empty = pygame.Surface((SDL_XMAX, SDL_YMAX))
    points = pygame.sprite.Group()
    clock = pygame.time.Clock() 
    panel = Panel("", points)
    
    draw_axes(screen, XMIN, XMAX, YMIN, YMAX)
    overflow = False
    current = complex(args.seed)
    while True:
        if not overflow:
            current = args.function(current)
            x,y = current.real, current.imag
            try:
                Point(x, y, (0,255,0), points)
                print x,y
            except TypeError:
                print "Overflow"
                panel.val = "Overflow"
                overflow = True


        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        # Update sprites
        points.clear(screen, empty)
        points.update()
        points.draw(screen)
        pygame.display.flip()

        


if __name__ == '__main__':
    main()
