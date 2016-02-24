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


def math2pygame(x, y):
    scalex = SDL_XMAX/float(XMAX - XMIN)
    scaley = SDL_YMAX/float(YMAX - YMIN)
    gx = scalex*x + SDL_XMAX/2
    gy = SDL_YMAX/2 - scaley*y
    return gx, gy


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
        self.rect.center = math2pygame(x, y)
        
        # print "{:.04},{:.04} :: {:.04},{:.04}".format(x,y, *math2pygame(x, y))
        self.c = colour
    def update(self):
        pass

def draw_axes(surface, xmin, xmax, ymin, ymax):
    s1, s2 = math2pygame(xmin, 0), math2pygame(0, ymin)
    e1, e2 = math2pygame(xmax, 0), math2pygame(0, ymax)
    pygame.draw.line(surface, (0, 100, 0), s1, e1, 1)
    pygame.draw.line(surface, (0, 100, 0), s2, e2, 1)
    # pygame.draw.line(surface, (0, 255, 0), math2pygame(xmin, ymin), math2pygame(xmax, ymax), 1)

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
    parser.add_argument("--seed", dest = "seed", action = "store", type = float,
                        help = "Point whose orbit to plot")
    parser.add_argument("--iters", dest = "iters", action = "store", type = int, default = 0,
                        help = "Number of iterations to plot")

    args = parser.parse_args()
    args.winsize = [int(x) for x in args.winsize.split("x")]
    args.min = [float(x) for x in args.min.split("x")]
    args.max = [float(x) for x in args.max.split("x")]
    args.function = eval("lambda x : {}".format(args.function)) 
    return args

def graphical_plot(function, start, end, increment):
    """Generates y values for given function starting from `start` and
    ending at `end`. x values are incremented by increment.""" 
    while start < end:
        yield start, function(start)
        start += increment
    

def graphical_analysis(seed, function, iterations):
    for i in range(iterations):
        t = function(seed)
        start = seed, t
        end = t, t
        seed = t
        yield start, end
        
        u = function(seed)
        start = t, t
        end = t, u
        yield start, end

    
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

    per_xpixel = float(XMAX - XMIN)/SDL_XMAX
    per_ypixel = float(YMAX - YMIN)/SDL_YMAX


    screen = pygame.display.set_mode((SDL_XMAX, SDL_YMAX), DOUBLEBUF)
    screen.fill((0,10,0))
    empty = pygame.Surface((SDL_XMAX, SDL_YMAX))
    draw_axes(screen, XMIN, XMAX, YMIN, YMAX)
    points = pygame.sprite.Group()
    clock = pygame.time.Clock() 


    for x, y in graphical_plot(args.function, args.start, args.stop, per_xpixel):
        Point(x, y, (255,255,0), points)

    for x, y in graphical_plot(lambda x: x, args.start, args.stop, per_xpixel):
        Point(x, y, (125,125,125), points)


    lines = graphical_analysis(args.seed, args.function, args.iters)
    
    col = 20
    while True:
        clock.tick(30)

        if args.iters:
            try:
                start,stop = next(lines)
                if start < stop:
                    start, stop = stop, start
                pygame.draw.line(screen, (100, 0, col), math2pygame(*start), math2pygame(*stop), 2)
                print stop[1]
                start,stop = next(lines)
                if start < stop:
                    start, stop = stop, start

                pygame.draw.line(screen, (100, 0, col), math2pygame(*start), math2pygame(*stop), 2)

            except StopIteration:
                pass
            except TypeError:
                pass
            # except OverflowError:
            #     pass

            col = (col + 50)%255


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

