from abc import ABC, abstractmethod
from typing import Type


class Entity:
    def __init__(self, health, max_health, damage: int) -> None:
        self.health = health
        self.max_health = max_health
        self.damage = damage
    
    def heal(self, value: int) -> None:
        hp = self.health + value
        if self.max_health < hp:
            self.health = self.max_health
            return
        self.health = hp
    
    def take_damage(self, value: int) -> None:
        hp = self.health - value
        if self.health <= 0:
            self.health = 0
            return self.on_death()
        self.health = hp
    
    def deal_damage(self, entity) -> None:
        entity.take_damage(self.damage)
    
    @abstractmethod
    def on_death(self) -> None:
        pass
