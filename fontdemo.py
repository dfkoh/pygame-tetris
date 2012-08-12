
import sys
from pprint import pprint

import pygame
from pygame.locals import *


white = pygame.Color(255, 255, 255)
black = pygame.Color(0, 0, 0)

def get_font_surf(name):
    f = pygame.font.SysFont(name, 18)
    fsurf = f.render("{}".format(name), True, black)
    return fsurf

def main():
    pygame.init()
    pygame.font.init()
    display_surf = pygame.display.set_mode((600, 600))
    surf = pygame.Surface((600, 4000))

    surf.fill(white)

    if not pygame.font.get_init():
        print("Could not initialize fonts!", file=sys.stderr)
        return

    PAD = 5
    #f = pygame.font.SysFont("timesnewroman", 18)
    #fsurf = f.render("the quick brown fox jumped over the lazy dog", True, black)
    left = PAD
    top = PAD

    movement = {
        K_DOWN : 10,
        K_UP : -10,
        K_PAGEDOWN : 100,
        K_PAGEUP : -100
    }

    print("Fonts:", len(pygame.font.get_fonts()))
    pprint(sorted(pygame.font.get_fonts()))

    for name in sorted(pygame.font.get_fonts()):
        fsurf = get_font_surf(name)
        rect = surf.blit(fsurf, (left, top))
        top = rect.top + rect.height + PAD

    print(top)

    surf_rect = surf.get_rect()
    display_rect = display_surf.get_rect()
    display_surf.blit(surf, (0,0), display_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                dy = movement.get(event.key, 0)

                display_rect = display_rect.move(0, dy).clamp(surf_rect)
        
        display_surf.blit(surf, (0,0), display_rect)
        pygame.display.update()

                

if __name__ == "__main__":
    main()