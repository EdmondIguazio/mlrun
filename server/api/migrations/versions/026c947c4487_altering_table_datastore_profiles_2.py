# Copyright 2023 Iguazio
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

"""altering table datastore_profiles 2

Revision ID: 026c947c4487
Revises: b1d1e7ab5dec
Create Date: 2023-08-10 14:15:30.523729

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "026c947c4487"
down_revision = "b1d1e7ab5dec"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("datastore_profiles", sa.Column("object", sa.JSON(), nullable=True))
    op.drop_column("datastore_profiles", "body")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "datastore_profiles", sa.Column("body", sa.String(length=1024), nullable=True)
    )
    op.drop_column("datastore_profiles", "object")
    # ### end Alembic commands ###