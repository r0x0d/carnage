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
"""Module that represents the Dungeon seeding."""

from typing import Any

from carnage.database.repository.dungeon import (
    DungeonDifficultyRepository,
    DungeonRepository,
    DungeonSchemaRepository,
)
from carnage.database.seeds.base import BaseSeed
from carnage.systems.dungeon_generation import generate_dungeon


class DungeonSeed(BaseSeed):
    """Class that overrides the base seed methods."""

    name: str = "dungeon"
    data: list[dict[str, Any]] = [
        {
            "_dungeon_difficulty": "Easy",
            "name": "Easy dungeon",
            "description": "Easy dungeon",
        },
    ]

    def __init__(
        self,
        repository: type[DungeonRepository] = DungeonRepository,
    ) -> None:
        """Default class constructor.

        :param repository: The repository used to issue queries.
        """
        super().__init__(repository=repository)
        self.dungeon_schema_repository = DungeonSchemaRepository()
        self.dungeon_difficulty_repository = DungeonDifficultyRepository()

    def seed(self) -> None:
        """Method to seed data into the database."""
        for item in self.data:
            dungeon_difficulty = self.dungeon_difficulty_repository.select_by_level(
                level=item["_dungeon_difficulty"],
            )
            dungeon_schema = (
                self.dungeon_schema_repository.select_by_dungeon_difficulty(
                    dungeon_difficulty[0].id,
                )
            )
            plot = generate_dungeon(dungeon_difficulty[0].id)
            item.pop("_dungeon_difficulty")
            item.update(
                {"dungeon_schema_id": dungeon_schema[0].id, "plot": plot},
            )

        super().seed()
