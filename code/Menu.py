#!/usr/bin/python
# -*- coding: utf-8 -*-

import pygame.image
import pygame.transform
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import WIN_WIDTH, WIN_HEIGHT, MENU_OPTION, C_WHITE, C_YELLOW


C_GHOST = (180, 255, 180)
C_DARK = (20, 30, 20)


class Menu:
    def __init__(self, window):
        self.window = window
        self.surf = pygame.image.load('./asset/MenuBg.png').convert()
        self.surf = pygame.transform.scale(self.surf, (WIN_WIDTH, WIN_HEIGHT))
        self.rect = self.surf.get_rect(left=0, top=0)

    def run(self):
        menu_option = 0
        pygame.mixer_music.load('./asset/Menu.mp3')
        pygame.mixer_music.play(-1)

        while True:
            self.window.blit(source=self.surf, dest=self.rect)

            self.menu_text(52, "Princess", C_GHOST, ((WIN_WIDTH / 2), 45))
            self.menu_text(52, "Escape", C_GHOST, ((WIN_WIDTH / 2), 95))

            self.menu_text(18, "Setas - Mover a princesa", C_WHITE, ((WIN_WIDTH / 2), 145))
            self.menu_text(18, "Desvie dos lobos zumbis", C_WHITE, ((WIN_WIDTH / 2), 170))
            self.menu_text(18, "Sobreviva ate o tempo acabar", C_WHITE, ((WIN_WIDTH / 2), 195))

            for i in range(len(MENU_OPTION)):
                color = C_YELLOW if i == menu_option else C_WHITE
                self.menu_text(20, MENU_OPTION[i], color, ((WIN_WIDTH / 2), 250 + 28 * i))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_option = (menu_option + 1) % len(MENU_OPTION)

                    if event.key == pygame.K_UP:
                        menu_option = (menu_option - 1) % len(MENU_OPTION)

                    if event.key == pygame.K_RETURN:
                        return MENU_OPTION[menu_option]

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size, bold=True)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(center=text_center_pos)
        self.window.blit(source=text_surf, dest=text_rect)
        