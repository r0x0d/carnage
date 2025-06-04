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
"""Module that represents the Spell Duration Type seeding."""

from carnage.database.repository.spell import SpellDurationTypeRepository
from carnage.database.seeds.base import BaseSeed


class SpellDurationTypeSeed(BaseSeed):
    """Class that overrides the base seed methods."""

    name: str = "spell-duration-type"
    data: list[dict[str, str]] = [
        {
            "name": "Concentration",
            "description": "Concentration duration",
        },
        {
            "name": "Instantaneous",
            "description": "Instantaneous duration",
        },
        {
            "name": "Special",
            "description": "Special duration",
        },
        {
            "name": "Time",
            "description": "Time duration",
        },
        {
            "name": "Until Dispelled",
            "description": "Until Dispelled duration",
        },
        {
            "name": "Until Dispelled or Triggered",
            "description": "Until Dispelled or Triggered duration",
        },
    ]

    def __init__(
        self,
        repository: type[SpellDurationTypeRepository] = SpellDurationTypeRepository,
    ) -> None:
        """Default class constructor.

        :param repository: The repository used to issue queries.
        """
        super().__init__(repository=repository)
