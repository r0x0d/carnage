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
"""Module that represents the Dungeon History repository."""

from functools import lru_cache

from sqlalchemy import select

from carnage.database.models.dungeon import DungeonHistoryModel
from carnage.database.repository.base import BaseRepository


class DungeonHistoryRepository(BaseRepository):
    """Class that overrides the base repository methods."""

    def __init__(
        self,
        model: type[DungeonHistoryModel] = DungeonHistoryModel,
    ) -> None:
        """Default constructor for repository.

        :param model: The model used in the repository.
        """
        super().__init__(model)

    @lru_cache
    def select_by_player_id(self, player_id: str) -> DungeonHistoryModel:
        """Get results from database filtering by player id.

        :param player_id: Player id to be used in the filter.
        """
        statement = select(self.model).where(
            self.model.player_id == player_id and self.deleted_at == None,  # type: ignore # noqa
        )

        with self.session() as session:
            return session.execute(statement=statement).first()

    @lru_cache
    def select_by_dungeon_id(self, dungeon_id: str) -> DungeonHistoryModel:
        """Get results from database filtering by dungeon id.

        :param dungeon_id: Dungeon id to be used in the filter.
        """
        statement = select(self.model).where(
            self.model.dungeon_id == dungeon_id and self.deleted_at == None,  # type: ignore # noqa
        )

        with self.session() as session:
            return session.execute(statement=statement).first()

    @lru_cache
    def select_by_player_and_dungeon_id(
        self,
        player_id: str,
        dungeon_id: str,
    ) -> DungeonHistoryModel:
        """Get results from database filtering by player and level id.

        :param player_id: Player id to be used in the filter.
        :param dungeon_id: Dungeon id to be used in the filter.
        """
        statement = select(self.model).where(
            self.model.player_id == player_id
            and self.model.dungeon_id == dungeon_id
            and self.deleted_at == None,  # type: ignore # noqa
        )

        with self.session() as session:
            return session.execute(statement=statement).first()
