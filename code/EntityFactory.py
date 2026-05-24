#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

from code.Background import Background
from code.Const import WIN_WIDTH, WIN_HEIGHT
from code.Enemy import Enemy
from code.Player import Player


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str):
        match entity_name:

            # ===== FUNDOS =====
            case 'Level1Bg':
                list_bg = []
                for i in range(5):
                    list_bg.append(Background(f'Level1Bg{i}', (0, 0)))
                    list_bg.append(Background(f'Level1Bg{i}', (WIN_WIDTH, 0)))
                return list_bg

            case 'Level2Bg':
                list_bg = []
                for i in range(5):
                    list_bg.append(Background(f'Level2Bg{i}', (0, 0)))
                    list_bg.append(Background(f'Level2Bg{i}', (WIN_WIDTH, 0)))
                return list_bg

            # ===== PRINCESA =====
            case 'Player1':
                return Player(
                    'Player1',
                    (WIN_WIDTH - 90, WIN_HEIGHT - 95)
                )

            case 'Player2':
                return Player(
                    'Player2',
                    (WIN_WIDTH - 90, WIN_HEIGHT - 95)
                )

            # ===== LOBOS =====
            case 'Enemy1':
                y_positions = [
                    WIN_HEIGHT - 95,   # chão
                    WIN_HEIGHT - 140,  # médio
                    WIN_HEIGHT - 185,  # alto
                ]

                return Enemy(
                    'Enemy1',
                    (-20, random.choice(y_positions))
                )

            case 'Enemy2':
                y_positions = [
                    WIN_HEIGHT - 110,
                    WIN_HEIGHT - 160,
                    WIN_HEIGHT - 210,
                ]

                return Enemy(
                    'Enemy2',
                    (-40, random.choice(y_positions))
                )