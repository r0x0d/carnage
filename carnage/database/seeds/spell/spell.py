# MIT License
#
# Copyright (c) 2022, Rodolfo Olivieri
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
"""Module that represents the Spell seeding."""

from typing import Any

from carnage.database.repository.spell import (
    SpellDurationTypeRepository,
    SpellRangeTypeRepository,
    SpellRepository,
    SpellSchoolRepository,
)
from carnage.database.seeds.base import BaseSeed


class SpellSeed(BaseSeed):
    """Class that overrides the base seed methods."""

    name: str = "spell"
    data: list[dict[str, Any]] = [
        {
            "name": "Fireball",
            "description": "An powerfull fire ball.",
            "base_magical_damage": 10,
            "attack_threshold": 70.0,
            "critical_attack_threshold": 90.0,
        },
    ]

    def __init__(
        self,
        repository: type[SpellRepository] = SpellRepository,
    ) -> None:
        """Default class constructor.

        :param repository: The repository used to issue queries.
        """
        super().__init__(repository=repository)
        self.spell_school_repository = SpellSchoolRepository()
        self.spell_duration_type_repository = SpellDurationTypeRepository()
        self.spell_range_type_repository = SpellRangeTypeRepository()

    def seed(self) -> None:
        """Method to seed data into the database."""
        spell_school = self.spell_school_repository.select_first()
        spell_duration_type = self.spell_duration_type_repository.select_first()
        spell_range_type = self.spell_range_type_repository.select_first()

        for item in self.data:
            item.update(
                {
                    "spell_school_id": spell_school[0].id,
                    "spell_duration_type_id": spell_duration_type[0].id,
                    "spell_range_type_id": spell_range_type[0].id,
                },
            )

        super().seed()
