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
"""Add monsters table.

Revision ID: 1e5ec8a69d2a
Revises: faffe495bb96
Create Date: 2022-10-12 02:29:14.502293

"""

from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision = "1e5ec8a69d2a"
down_revision = "faffe495bb96"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = [
        sa.Column(
            "id",
            UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("hitpoints", sa.Integer(), nullable=False),
        sa.Column("strength", sa.Integer()),
        sa.Column("dexterity", sa.Integer()),
        sa.Column("intelligence", sa.Integer()),
        sa.Column("luck", sa.Integer()),
        sa.Column("base_damage", sa.Integer()),
        sa.Column("base_magical_damage", sa.Integer()),
        sa.Column("base_armor_resistance", sa.Integer()),
        sa.Column("base_magical_resistance", sa.Integer()),
        sa.Column("is_boss", sa.Boolean(), nullable=False, default=False),
        sa.Column("attack_threshold", sa.Float(), nullable=False),
        sa.Column("critical_attack_threshold", sa.Float(), nullable=False),
        sa.Column(
            "monster_type_id",
            UUID(as_uuid=True),
            sa.ForeignKey("monster_types.id"),
            nullable=False,
        ),
        sa.Column(
            "size_id",
            UUID(as_uuid=True),
            sa.ForeignKey("sizes.id"),
            nullable=False,
        ),
        sa.Column(
            "aligment_id",
            UUID(as_uuid=True),
            sa.ForeignKey("aligments.id"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            default=datetime.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            default=datetime.now(),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.DateTime(), default=None, nullable=True),
    ]
    op.create_table("monsters", *columns)


def downgrade() -> None:
    op.drop_table("monsters")
