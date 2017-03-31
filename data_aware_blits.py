""" Just a demo to prove that data aware blit can improve performance.

This only shows off the case where there is a transparent image.

Instead of using a single blitter for the whole image,
we use a specialised one for each piece of the data.

I call this data aware blit/JIT.


There are other options as well.

Including:
    * 8 bit RLE encoded sub surfaces
    * pure fill colours.

Additionally this could test which types of blit routines are
quicker on the particular hardware being used. What is the fast path?
"""

from io import BytesIO
from urllib.request import urlopen
import pygame
from pygame.locals import *
import time


pygame.init()


screen = pygame.display.set_mode((800, 600))
url = 'http://pygame-zero.readthedocs.io/en/latest/_images/alien.png'
# surf = pygame.image.load(BytesIO(urlopen(url).read())).convert_alpha()
orig_surf = pygame.image.load(BytesIO(urlopen(url).read()))


def optimize(surf):
    """ create a series of surfaces optimized based on their image data.

    Note: this one just manually creates a middle surface without transparency.
    """
    # 12, 32  12, 72  52, 32  52, 73
    middle_surf = surf.subsurface((12, 32, 40, 41))
    new_middle = middle_surf.convert()
    new_middle.blit(middle_surf, (0, 0))

    surfaces = [(surf.subsurface((0, 0, 66, 32)).convert_alpha(), (0, 0)),
                (surf.subsurface((0, 32, 12, 40)).convert_alpha(), (0, 32)),
                (new_middle, (12, 32)),
                (surf.subsurface((52, 32, 14, 40)).convert_alpha(), (52, 32)),
                (surf.subsurface((0, 73, 66, 19)).convert_alpha(), (0, 73))]
    return surfaces


surf = orig_surf.convert_alpha()
surfaces = optimize(orig_surf)

going = True
i = 0
while going:
    if i > 255:
        i = 0
    screen.fill((i, 0, 0), screen.get_rect())

    events = pygame.event.get()

    for e in events:
        if e.type == QUIT:
            going = False
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            going = False

    t0 = time.time()
    for x in range(110):
        for y in range(110):
            screen.blit(surf, (100, 0))
    t1 = time.time()
    # print(t1 - t0)

    t00 = time.time()
    for x in range(110):
        for y in range(110):
            # screen.blit(surf, (400, 400))
            for subsurf, rect in surfaces:
                screen.blit(subsurf, rect)
    t11 = time.time()

    print(f'optimized:{t11 - t00}  unoptimized: {t1 - t0}')

    pygame.display.flip()
    i += 1
