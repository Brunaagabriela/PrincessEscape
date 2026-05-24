#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

import pygame
from pygame import Surface, Rect
from pygame.font import Font

from code.Const import (
    C_WHITE,
    WIN_HEIGHT,
    WIN_WIDTH,
    MENU_OPTION,
    EVENT_ENEMY,
    SPAWN_TIME,
    C_GREEN,
    C_CYAN,
    EVENT_TIMEOUT,
    TIMEOUT_STEP,
    TIMEOUT_LEVEL,
    C_YELLOW
)
from code.Enemy import Enemy
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.EntityMediator import EntityMediator
from code.Player import Player


class Level:
    def __init__(self, window: Surface, name: str, game_mode: str, player_score: list[int]):
        self.timeout = TIMEOUT_LEVEL
        self.window = window
        self.name = name
        self.game_mode = game_mode
        self.entity_list: list[Entity] = []
        self.font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=14)

        self.entity_list.extend(EntityFactory.get_entity(self.name + 'Bg'))

        player = EntityFactory.get_entity('Player1')
        player.score = player_score[0]
        self.entity_list.append(player)

        if game_mode in [MENU_OPTION[1], MENU_OPTION[2]]:
            player = EntityFactory.get_entity('Player2')
            player.score = player_score[1]
            self.entity_list.append(player)

        pygame.time.set_timer(EVENT_ENEMY, SPAWN_TIME)
        pygame.time.set_timer(EVENT_TIMEOUT, TIMEOUT_STEP)

    def run(self, player_score: list[int]):
        pygame.mixer_music.load(f'./asset/{self.name}.mp3')
        pygame.mixer_music.set_volume(0.3)
        pygame.mixer_music.play(-1)

        clock = pygame.time.Clock()

        while True:
            self.window.fill((0, 0, 0))
            clock.tick(60)

            for ent in self.entity_list:
                self.window.blit(source=ent.surf, dest=ent.rect)
                ent.move()

                if isinstance(ent, (Player, Enemy)):
                    shoot = ent.shoot()
                    if shoot is not None:
                        self.entity_list.append(shoot)

                if ent.name == 'Player1':
                    self.level_text(
                        14,
                        f'Vida: {ent.health} | Pontos: {ent.score}',
                        C_GREEN,
                        (10, 25)
                    )

                if ent.name == 'Player2':
                    self.level_text(
                        14,
                        f'Player2 - Vida: {ent.health} | Pontos: {ent.score}',
                        C_CYAN,
                        (10, 45)
                    )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == EVENT_ENEMY:
                    choice = random.choice(('Enemy1', 'Enemy2'))
                    self.entity_list.append(EntityFactory.get_entity(choice))

                if event.type == EVENT_TIMEOUT:
                    self.timeout -= TIMEOUT_STEP

                    if self.timeout <= 0:
                        for ent in self.entity_list:
                            if isinstance(ent, Player) and ent.name == 'Player1':
                                player_score[0] = ent.score
                            if isinstance(ent, Player) and ent.name == 'Player2':
                                player_score[1] = ent.score

                        self.show_message(
                            "VOCE ESCAPOU!",
                            "A princesa fugiu dos lobos zumbis."
                        )
                        return True

            found_player = False

            for ent in self.entity_list:
                if isinstance(ent, Player):
                    found_player = True

            if not found_player:
                self.show_message(
                    "FIM DE JOGO",
                    "A princesa foi capturada pelos lobos!"
                )
                return False

            self.level_text(
                14,
                f'Tempo: {self.timeout / 1000:.1f}s',
                C_WHITE,
                (10, 5)
            )

            pygame.display.flip()

            EntityMediator.verify_collision(entity_list=self.entity_list)
            EntityMediator.verify_health(entity_list=self.entity_list)

    def show_message(self, title: str, subtitle: str):
        pygame.mixer_music.stop()

        # escolhe imagem
        if "ESCAPOU" in title:
            image_path = "./asset/Victory.png"
        else:
            image_path = "./asset/GameOver.png"

        background = pygame.image.load(image_path).convert()
        background = pygame.transform.scale(
            background,
            (WIN_WIDTH, WIN_HEIGHT)
        )

        waiting = True

        while waiting:

            self.window.blit(background, (0, 0))

            self.message_text(
                16,
                "Pressione ENTER para voltar ao menu",
                (0, 0, 0),
                (WIN_WIDTH / 2 + 2, WIN_HEIGHT - 28)
            )

            self.message_text(
                16,
                "Pressione ENTER para voltar ao menu",
                (255, 255, 255),
                (WIN_WIDTH / 2, WIN_HEIGHT - 30)
            )

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(
            name="Lucida Sans Typewriter",
            size=text_size
        )

        text_surf: Surface = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        text_rect: Rect = text_surf.get_rect(
            left=text_pos[0],
            top=text_pos[1]
        )

        self.window.blit(
            source=text_surf,
            dest=text_rect
        )

    def message_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        text_font: Font = pygame.font.SysFont(
            name="Lucida Sans Typewriter",
            size=text_size,
            bold=True
        )

        text_surf: Surface = text_font.render(
            text,
            True,
            text_color
        ).convert_alpha()

        text_rect: Rect = text_surf.get_rect(
            center=text_center_pos
        )

        self.window.blit(
            source=text_surf,
            dest=text_rect
        )