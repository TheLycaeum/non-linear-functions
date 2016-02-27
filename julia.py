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
        self.font = pygame.font.Font("jGara2.ttf", 25)
        self.image = pygame.Surface((SDL_XMAX,100)).convert_alpha()
        self.image.fill((0,10,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, SDL_YMAX)
        self.val = val
        info = self.font.render(val, True,(200,200,20))
        self.image.fill((0,10,0,0))
        self.image.blit(info,(0,0))

    def update(self):
        info = self.font.render(self.val, True,(200,200,20))
        self.image.fill((0,10,0,0))
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
        # print "{}, {} - {},{}".format(x, y, u, v)
        self.rect.center = (u,v)
        
        # print "{:.04},{:.04} :: {:.04},{:.04}".format(x,y, *math2pygame(x, y))
        self.c = colour
    def update(self):
        pass


def parse_args():
    global check
    global C
    parser = argparse.ArgumentParser()
    parser.add_argument("--winsize", dest = "winsize", default = "600x600", help = "Size of window")
    parser.add_argument("--min", dest = "min", default = "-1x-1", help = "Min point of grid")
    parser.add_argument("--max", dest = "max", default = "1x1", help = "Max point of grid")
    parser.add_argument("--function", dest = "function", help = "Function to plot")
    parser.add_argument("--live", dest = "live", default = False, help = "Show colours as they're being plotted")
    parser.add_argument("--iters", dest = "iters", default = 20, help = "Number of iterations to check for each point", type =int)
    parser.add_argument("--multi", dest = "multi", default = False, action = "store_true", help = "Use shades depending on number of iterations")
    args = parser.parse_args()
    args.winsize = [int(x) for x in args.winsize.split("x")]
    args.min = [float(x) for x in args.min.split("x")]
    args.max = [float(x) for x in args.max.split("x")]
    C = args.function
    args.function = eval("lambda x : {}".format(args.function))
    if args.multi:
        check = check_colour
    else:
        check = check_mono
    return args

def check_mono(x, y, fn, iters):
    c = complex(x, y)
    for _ in range(iters):
        if abs(c) > 2:
            return 255
        c = fn(c)
    return 100
        
def check_colour(x, y, fn, iters):
    c = complex(x, y)
    for i in range(iters):
        if abs(c) > 2:
            return int(255 * float(i)/iters)
        c = fn(c)
    return 100
        

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

    per_xpixel = float(XMAX - XMIN)/SDL_XMAX
    per_ypixel = float(YMAX - YMIN)/SDL_YMAX
    
    screen = pygame.display.set_mode((SDL_XMAX, SDL_YMAX+50), DOUBLEBUF)
    pygame.font.init()
    screen.fill((0,10,0))
    empty = pygame.Surface((SDL_XMAX, SDL_YMAX))
    points = pygame.sprite.Group()
    clock = pygame.time.Clock() 
    Panel(C, points)
    
    draw_axes(screen, XMIN, XMAX, YMIN, YMAX)
    x = XMIN
    y = YMIN
    while True:
        # Update sprites
        points.clear(screen, empty)
        points.update()
        points.draw(screen)
        pygame.display.flip()

        for _1 in range(SDL_XMAX):
            x += per_xpixel
            y = YMIN
            for _2 in range(SDL_YMAX):
                y += per_ypixel
                colour = check(x, y, args.function, args.iters)
                Point(x, y, (colour, colour, 0), points)
                for event in pygame.event.get():
                    if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        sys.exit()
                
            if args.live:
                # Update sprites
                points.clear(screen, empty)
                points.update()
                points.draw(screen)
                pygame.display.flip()





        


if __name__ == '__main__':
    main()
