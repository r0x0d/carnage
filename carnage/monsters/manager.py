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
"""Modules that manages the monsters available."""

from functools import cached_property
from typing import Any

from carnage.monsters.base import BaseMonster
from carnage.monsters.dragon import Dragon


class MonsterManager:
    """Class that manages and maps the monsters."""

    @cached_property
    def _monster_mapping(self) -> dict[str, Any]:
        """Method that maps the available monsters to their simplified name.

        :return: A dictionary with the seed name as key and a seed class
            instance as value.
        """
        # TODO(r0x0d): Change type annotation for this property in the future
        # to `BaseMonster`
        return {"dragon": Dragon}

    def select(self, monster: str) -> BaseMonster | None:
        """Select an monster out of the list of available ones and return it.

        :param monster: The name of the monster to be selected.
        """
        return self._monster_mapping.get(monster)
