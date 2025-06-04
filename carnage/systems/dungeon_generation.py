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
"""Module that handles the generation of new dungeons."""

import logging
from functools import lru_cache
from random import choice, randint
from typing import Any

import jinja2
import yaml

from carnage.database.models.monster.monster import MonsterModel
from carnage.database.repository.dungeon import DungeonSchemaRepository
from carnage.database.repository.monster import MonsterRepository

monster_repository = MonsterRepository()
dungeon_schema_repository = DungeonSchemaRepository()

logger = logging.getLogger(__name__)


@lru_cache
def _pick_random_monster(monsters: tuple[MonsterModel]) -> tuple[str, bool]:
    """Private method to pick a random monster based on a list of monsters."""
    return choice(monsters)


def _render_jinja_template(
    schema: str,
    jinja_arguments: dict[str, Any],
) -> dict[str, Any]:
    """Private method to render jinja templates.

    :param schema: The jinja schema used.
    :param jinja_arguments: The arguments passed down to jinja rendering.
    """
    template = jinja2.Template(schema, autoescape=True)
    rendered_template = template.render(jinja_arguments)
    # We were supposed to use json.loads, but we generate an invalid json, so
    # yaml it is!.
    return yaml.safe_load(rendered_template)


def generate_dungeon(
    dungeon_difficulty_id: str,
) -> dict[str, Any]:
    """Method that handles the generation of a dungeon based on a schema.

    :param dungeon_difficulty_id: The dungeon difficulty id to be used in a
        query.
    """
    dungeon_schema = dungeon_schema_repository.select_by_dungeon_difficulty(
        dungeon_difficulty_id,
    )
    monsters = tuple(monster_repository.select())

    return _render_jinja_template(
        dungeon_schema[0].schema,
        jinja_arguments={
            "randint": randint,
            "monsters": monsters,
            "pick_random_monster": _pick_random_monster,
        },
    )
