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

class Panel(pygame.sprite.Sprite):
    def __init__(self, val, pos, colour, groups):
        super(Panel, self).__init__(groups)
        self.font = pygame.font.Font("jGara2.ttf", 20)
        self.image = pygame.Surface((50,25)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midtop = pos
        self.val = val
        self.colour = colour

    def update(self):
        info = self.font.render(self.val, True,(20,200,20))
        self.image.fill(self.colour)
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
    parser.add_argument("--iters", dest = "iters", action = "store", type = int, default = 0,
                        help = "Number of iterations to plot")

    args = parser.parse_args()
    args.winsize = [int(x) for x in args.winsize.split("x")]
    args.min = [float(x) for x in args.min.split("x")]
    args.max = [float(x) for x in args.max.split("x")]
    return args

def plot_orbit(fn, c, count, points):
    plot_after = count * 0.6
    y = 0
    # print "For {}".format(c)
    for i in range(count):
        if i > plot_after:
            y = fn(y)
            # print "   {:5.4}, {:5.4} -- {}, {}".format(c, y, *math2pygame(c, y))
            Point(c, y, (0,255,0), points)

def draw_marker(x, surface, group, pos, colour = (100,0,0,255)):
    pygame.draw.line(surface, colour, math2pygame(x,YMIN), math2pygame(x,YMAX), 1)
    if pos == 0:
        u, v = math2pygame(x, YMAX)
        p = Panel(str(x), (u, v+20), colour, group)
    elif pos == 1:
        u, v = math2pygame(x, YMIN)
        p = Panel(str(x), (u ,v-20), colour, group)
    
    

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
    print "{} - {}".format((XMIN, YMIN), math2pygame(XMIN, YMIN))
    print ""
    print "{} - {}".format((XMAX, YMAX), math2pygame(XMAX, YMAX))
    # assert math2pygame(XMIN, YMIN) == 0,SDL_YMAX
    # sys.exit()

    
    screen = pygame.display.set_mode((SDL_XMAX, SDL_YMAX), DOUBLEBUF)
    pygame.font.init()
    screen.fill((0,10,0))
    empty = pygame.Surface((SDL_XMAX, SDL_YMAX))
    points = pygame.sprite.Group()
    clock = pygame.time.Clock() 
    

    current = args.start
    increment = (args.stop - args.start)/SDL_XMAX
    # increment = 0.00625
    nmarkers = 20
    c = (args.stop - args.start) / nmarkers
    markers = [args.start+c*i for i in range(nmarkers)]
    pos = 0
    draw_marker(-2.0, screen, points, 0, (100,0,255,255))
    draw_marker(0.25, screen, points, 1, (100,0,255,255))
    while True:
        if current <= args.stop:
            for i in markers:
                if abs(current - i) < 0.0001:
                    draw_marker(i, screen, points, pos)
                    if pos == 0:
                        pos = 1
                    else:
                        pos = 0
            current += increment
            fn_text = args.function.replace("c", str(current))
            function = eval("lambda x :{}".format(fn_text))
            # print current
            try:
                plot_orbit(function, current, args.iters, points)
            except TypeError:
                pass

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
