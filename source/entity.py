from abc import ABC, abstractmethod
from source.const import EntityState
from source.utils import Directions
from typing import Type


class Entity:
    """
    Base class for an Entity.
    
    Attributes:
        facing_direction (Directions | None): The direction that the entity is facing.
    
    Args:
        health (int): The current health points that the entity has.
        max_health (int): The maximum health points that the entity can have.
        damage (int): The amount of damage that the entity can inflict.
    """
    facing_direction = None

    def __init__(self, health, max_health, damage: int) -> None:
        self.state = EntityState.ALIVE
        self.health = health
        self.max_health = max_health
        self.damage = damage
    
    def heal(self, value: int) -> None:
        """
        Heals the entity by a specific amount of health points.
        
        Args:
            value (int): The amount of health point to heal.
        """
        hp = self.health + value
        if self.max_health < hp:
            self.health = self.max_health
            return
        self.health = hp
    
    def take_damage(self, value: int) -> None:
        """
        Take a specific amount of damage off the entities health points.
        
        Args:
            value (int): The amount of damage to inflict.
        """
        hp = self.health - value
        if self.health <= 0:
            self.health = 0
            self.state = EntityState.DEAD
            return self.on_death()
        self.health = hp
    
    def deal_damage(self, entity) -> None:
        """
        Inflict damage to another entity.
        
        Args:
            entity (Entity): The entity to deal damage upon.
        """
        entity.take_damage(self.damage)
    
    @abstractmethod
    def on_death(self) -> None:
        """
        Sets what event happens when the entity is deceased.
        """
        pass
