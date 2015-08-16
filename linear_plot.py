# Copyright 2015 Noufal Ibrahim <noufal@nibrahim.net.in>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import math
import sys
from math import *


import pygame
from pygame.locals import DOUBLEBUF, K_ESCAPE, KEYDOWN, QUIT


SDL_XMAX, SDL_YMAX = 700, 700
XMIN, YMIN, XMAX, YMAX = -100, -100, 100, 100

def math2pygame(x, y):
    scalex = SDL_XMAX/float(XMAX - XMIN)
    scaley = SDL_YMAX/float(YMAX - YMIN)
    gx = scalex*x + SDL_XMAX/2
    gy = SDL_YMAX/2 - scaley*y
    return gx, gy


class Panel(pygame.sprite.Sprite):
    def __init__(self, val, groups):
        super(Panel, self).__init__(groups)
        self.font = pygame.font.Font("jGara2.ttf", 20)
        self.image = pygame.Surface((100,25)).convert_alpha()
        self.image.fill((0,10,0))
        self.rect = self.image.get_rect()
        self.rect.bottomright = (SDL_XMAX, SDL_YMAX)
        self.val = val
        info = self.font.render("({},{})".format(val[0], val[1]), True,(20,200,20))
        self.image.fill((0,10,0,0))
        self.image.blit(info,(0,0))

    def update(self):
        info = self.font.render("({}  ,  {})".format(self.val[0], self.val[1]), True,(20,200,20))
        self.image.fill((0,10,0,0))
        self.image.blit(info,(0,0))




class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, colour, dies_in, panel, groups):
        super(Point,self).__init__(groups)
        self.image = pygame.Surface((8,8))
        pygame.draw.circle(self.image, 
                           (colour, colour, colour),
                           (4,4),
                           4,
                           0)
        self.rect = self.image.get_rect()
        self.rect.center = math2pygame(x, y)
        self.life = dies_in
        self.c = colour
        self.dec = colour/dies_in
        self.panel = panel
        self.x, self.y = x, y

    def update(self):
        self.life -= 1
        self.c -= self.dec
        self.c = int(self.c)
        pygame.draw.circle(self.image, (self.c, self.c, self.c), (4,4), 4, 0)
        x, y = pygame.mouse.get_pos()
        x0, y0, x1, y1 = self.rect
        if x0 < x < x0+x1 and y0 < y < y0+y1:
            self.panel.val = ["{:.3}".format(float(self.x)), "{:.3}".format(float(self.y))]
        if not self.life:
            self.kill()
            
def draw_axes(surface, interval):
    s1, s2 = math2pygame(-100, 0), math2pygame(0, -100)
    e1, e2 = math2pygame(100, 0), math2pygame(0, 100)
    pygame.draw.line(surface, (0, 200, 0), s1, e1, 1)
    pygame.draw.line(surface, (0, 200, 0), s2, e2, 1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--winsize", dest = "winsize", default = "600x600", help = "Size of window")
    parser.add_argument("--min", dest = "min", default = "-1x-1", help = "Min point of grid")
    parser.add_argument("--max", dest = "max", default = "1x1", help = "Max point of grid")
    parser.add_argument("--function", dest = "function", help = "Function to plot")
    parser.add_argument("--start", dest = "start", action = "store", type = float, 
                        help = "Number whose orbit to plot")
    args = parser.parse_args()
    args.winsize = [int(x) for x in args.winsize.split("x")]
    args.min = [int(x) for x in args.min.split("x")]
    args.max = [int(x) for x in args.max.split("x")]
    if args.function in globals():
        args.function = globals()[args.function]
    else:
        print "Here lambda x : {}".format(args.function)
        args.function = eval("lambda x : {}".format(args.function)) 
    return args

def linear_plot(function, start, iters = False):
    "Generates orbit of `start` with `function`. Stops  at `iters`"
    if iters:
        for i in range(iters):
            start = function(start)
            print start
            yield start
    else:
        while True:
            start = function(start)
            print start
            yield start
    
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

    screen = pygame.display.set_mode((SDL_XMAX, SDL_YMAX), DOUBLEBUF)
    screen.fill((0,10,0))
    pygame.font.init()
    empty = pygame.Surface((SDL_XMAX, SDL_YMAX))
    draw_axes(screen, 1)
    points = pygame.sprite.Group()
    clock = pygame.time.Clock() 
    panel = Panel(("",""), points)

    orbit = linear_plot(args.function, args.start)
    
    while True:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                sys.exit()

        Point(next(orbit), 0, 100, 100, panel, points)

        # Update sprites
        points.clear(screen, empty)
        points.update()
        points.draw(screen)
        pygame.display.flip()




if __name__ == '__main__':
    main()

