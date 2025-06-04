# MIT License
#
# Copyright (c) 2023, Rodolfo Olivieri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Module that represents the base of a spell."""

from random import SystemRandom

from carnage.database.models.spell import SpellModel


class BaseSpell:
    """Class that maps the essential methods and properties of a spell."""

    def __init__(self, spell: SpellModel) -> None:
        """Default constructor for a spell class mapping.

        .. seealso::
            All formulas defined in this class are based on the ORK framework:
            https://orkframework.com/guide/tutorials/status-system-setup/05-formulas/

            Another good resource for damage formula calculations are:
            https://gamedev.stackexchange.com/questions/14309/how-to-develop-rpg-damage-formulas

        :param spell: The spell attributes and data.
        """
        self.spell = spell
        self.random = SystemRandom()

    def attack(
        self,
        damage_type: int,
        attribute_modifier: int,
        player_defense: int,
    ) -> int:
        """Calculate the spell attack and return it's value.

        :param damage_type: The type of the damage to be used. Either normal
            attack (1) or critical attack (2).
        :param attribute_modifier: The attribute from either a spell or a
            player to be used in the calculation.
        :param player_defense: The amount of defense the target has.
        """
        damage = damage_type * (
            attribute_modifier * self.spell.base_damage / ((100 + player_defense) / 100)
        )

        return int(damage)

    def magical_attack(
        self,
        damage_type: int,
        attribute_modifier: int,
        player_magical_defense: int,
    ) -> int:
        """Calculate the spell magical attack and return it's value.

        :param damage_type: The type of the damage to be used. Either normal
            attack (1) or critical attack (2).
        :param attribute_modifier: The attribute from either a spell or a
            player to be used in the calculation.
        :param player_magical_defense: The amount of magical defense the target
            has.
        """
        damage = damage_type * (
            attribute_modifier
            * (self.spell.base_magical_damage * self.spell.base_magical_damage)
            / (self.spell.base_magical_damage + player_magical_defense)
        )

        return int(damage)

    def can_perform_attack(self) -> bool:
        """Handler method to define if the spell can perform an attack."""
        # TODO(r0x0d): Improve this in the future.
        random_number = self.random.randint(0, 100)
        return random_number >= self.spell.attack_threshold

    def can_perform_critical_attack(self) -> bool:
        """Handler method to define if a critical attack will be performed."""
        # TODO(r0x0d): Improve this in the future.
        random_number = self.random.randint(0, 100)
        return random_number >= self.spell.critical_attack_threshold
