#!/usr/bin/python
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

import pygame.image
import pygame.transform

from code.Const import ENTITY_HEALTH, ENTITY_DAMAGE, ENTITY_SCORE


class Entity(ABC):
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = pygame.image.load('./asset/' + name + '.png').convert_alpha()

        # Ajusta o tamanho das imagens novas
        if name in ['Player1', 'Player2']:
            self.surf = pygame.transform.scale(self.surf, (70, 90))

        elif name in ['Enemy1', 'Enemy2']:
            self.surf = pygame.transform.scale(self.surf, (65, 85))

        elif name in ['Player1Shot', 'Player2Shot']:
            self.surf = pygame.transform.scale(self.surf, (32, 16))

        elif name in ['Enemy1Shot', 'Enemy2Shot']:
            self.surf = pygame.transform.scale(self.surf, (28, 14))

        self.rect = self.surf.get_rect(left=position[0], top=position[1])
        self.speed = 0
        self.health = ENTITY_HEALTH[self.name]
        self.damage = ENTITY_DAMAGE[self.name]
        self.score = ENTITY_SCORE[self.name]
        self.last_dmg = 'None'

    @abstractmethod
    def move(self):
        pass