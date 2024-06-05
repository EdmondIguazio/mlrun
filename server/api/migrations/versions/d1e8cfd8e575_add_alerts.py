# Copyright 2024 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Add alerts

Revision ID: d1e8cfd8e575
Revises: 3e81ad4e5ebf
Create Date: 2024-04-15 14:54:16.729553

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "d1e8cfd8e575"
down_revision = "3e81ad4e5ebf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "alert_configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255, collation="utf8_bin"), nullable=False),
        sa.Column(
            "project", sa.String(length=255, collation="utf8_bin"), nullable=False
        ),
        sa.Column("object", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project", "name", name="_alert_configs_uc"),
    )
    op.create_table(
        "alert_configs_notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "project", sa.String(length=255, collation="utf8_bin"), nullable=True
        ),
        sa.Column("name", sa.String(length=255, collation="utf8_bin"), nullable=False),
        sa.Column("kind", sa.String(length=255, collation="utf8_bin"), nullable=False),
        sa.Column(
            "message", sa.String(length=255, collation="utf8_bin"), nullable=False
        ),
        sa.Column(
            "severity", sa.String(length=255, collation="utf8_bin"), nullable=False
        ),
        sa.Column("when", sa.String(length=255, collation="utf8_bin"), nullable=False),
        sa.Column(
            "condition", sa.String(length=255, collation="utf8_bin"), nullable=False
        ),
        sa.Column("secret_params", sa.JSON(), nullable=True),
        sa.Column("params", sa.JSON(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("sent_time", mysql.TIMESTAMP(fsp=3), nullable=True),
        sa.Column(
            "status", sa.String(length=255, collation="utf8_bin"), nullable=False
        ),
        sa.Column("reason", sa.String(length=255, collation="utf8_bin"), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["alert_configs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "name", "parent_id", name="_alert_configs_notifications_uc"
        ),
    )
    op.create_table(
        "alert_states",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column("created", mysql.TIMESTAMP(fsp=3), nullable=True),
        sa.Column("last_updated", mysql.TIMESTAMP(fsp=3), nullable=True),
        sa.Column("active", sa.BOOLEAN(), nullable=True),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("object", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["parent_id"],
            ["alert_configs.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id", "parent_id", name="alert_states_uc"),
    )
    op.create_table(
        "alert_templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255, collation="utf8_bin"), nullable=False),
        sa.Column("object", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="_alert_templates_uc"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("alert_templates")
    op.drop_table("alert_states")
    op.drop_table("alert_configs_notifications")
    op.drop_table("alert_configs")
    # ### end Alembic commands ###