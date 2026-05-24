#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED
from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        # Lobos correm da esquerda para a direita
        self.rect.centerx += ENTITY_SPEED[self.name]

    def shoot(self):
        return None