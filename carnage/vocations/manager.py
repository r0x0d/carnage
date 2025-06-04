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
"""Module that manages all vocations available."""

from functools import cached_property
from typing import Any

from carnage.vocations.base import BaseVocation
from carnage.vocations.knight import Knight


class VocationManager:
    """Class that maps the order and the vocations."""

    @cached_property
    def _vocation_mapping(self) -> dict[str, Any]:
        """Method that maps the available vocations to their simplified name.

        :return: A dictionary with the seed name as key and a seed class
            instance as value.
        """
        # TODO(r0x0d): Change type annotation for this property in the future
        # for `BaseVocation`
        return {"knight": Knight}

    def select(self, vocation: str) -> BaseVocation | None:
        """Select an vocation out of the list of available ones and return it.

        :param vocation: The name of the vocation to be selected.
        """
        return self._vocation_mapping.get(vocation)
