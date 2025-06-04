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
"""Module that represents the Player seeding."""

from typing import Any

from carnage.database.repository.dungeon import DungeonRepository
from carnage.database.repository.player import PlayerRepository
from carnage.database.repository.vocation import VocationRepository
from carnage.database.seeds.base import BaseSeed


class PlayerSeed(BaseSeed):
    """Class that overrides the base seed methods."""

    name: str = "player"
    data: list[dict[str, Any]] = [
        {
            "name": "Test",
            "description": "Test description",
            "is_alive": True,
        },
    ]

    def __init__(
        self,
        repository: type[PlayerRepository] = PlayerRepository,
    ) -> None:
        """Default class constructor.

        :param repository: The repository used to issue queries.
        """
        super().__init__(repository=repository)
        self.dungeon_repository = DungeonRepository()
        self.vocation_repository = VocationRepository()

    def seed(self) -> None:
        """Method to seed data into the database."""
        dungeon = self.dungeon_repository.select_first()
        vocation = self.vocation_repository.select_first()

        for item in self.data:
            item.update(
                {
                    "dungeon_id": dungeon[0].id,
                    "vocation_id": vocation[0].id,
                },
            )

        super().seed()
