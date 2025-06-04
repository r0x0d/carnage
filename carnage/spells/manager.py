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
"""Modules that manages the spells available."""

from functools import cached_property
from typing import Any

from carnage.spells.base import BaseSpell
from carnage.spells.fireball import Fireball


class SpellManager:
    """Class that manages and maps the spells."""

    @cached_property
    def _spell_mapping(self) -> dict[str, Any]:
        """Method that maps the available spells to their simplified name.

        :return: A dictionary with the seed name as key and a seed class
            instance as value.
        """
        # TODO(r0x0d): Change type annotation for this property in the future
        # to `BaseSpell`
        return {"fireball": Fireball}

    def select(self, spell: str) -> BaseSpell | None:
        """Select an spell out of the list of available ones and return it.

        :param spell: The name of the spell to be selected.
        """
        return self._spell_mapping.get(spell)
