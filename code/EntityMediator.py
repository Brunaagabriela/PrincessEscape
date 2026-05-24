from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        # Lobo saiu pela direita = princesa desviou = ganha ponto
        if isinstance(ent, Enemy) and ent.rect.left >= WIN_WIDTH:
            ent.health = 0

        if isinstance(ent, PlayerShot) and ent.rect.left >= WIN_WIDTH:
            ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        # Só queremos colisão entre princesa e lobo
        if isinstance(ent1, Player) and isinstance(ent2, Enemy):
            player = ent1
            enemy = ent2
        elif isinstance(ent1, Enemy) and isinstance(ent2, Player):
            player = ent2
            enemy = ent1
        else:
            return

        # Hitbox menor para ignorar área transparente dos sprites
        player_hitbox = player.rect.inflate(-35, -25)
        enemy_hitbox = enemy.rect.inflate(-35, -25)

        if player_hitbox.colliderect(enemy_hitbox):
            player.health = 0
            player.last_dmg = enemy.name

    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        for ent in entity_list:
            if ent.name == 'Player1':
                ent.score += enemy.score

    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)

            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list[:]:
            if ent.health <= 0:
                # Só dá ponto quando o lobo saiu da tela sem tocar na princesa
                if isinstance(ent, Enemy) and ent.last_dmg == 'None':
                    EntityMediator.__give_score(ent, entity_list)

                entity_list.remove(ent)