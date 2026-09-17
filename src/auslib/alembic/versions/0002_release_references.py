"""release references reverse index

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-03 00:00:00.000000

Adds the release_references table, a reverse index of the Releases each Release
serves in place of itself (a systemaddons SuperBlob's "blobs" entries), and
backfills it from the existing release data.
"""

import sqlalchemy as sa
from alembic import op

from auslib.blobs.base import createBlob
from auslib.errors import BlobValidationError

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def _backfill(conn, ref_table):
    for source in ("releases_json", "releases"):
        rows = conn.execute(sa.text(f"SELECT name, data FROM {source}")).fetchall()  # noqa: S608 (fixed table names)
        edges = []
        for name, data in rows:
            if data is None:
                continue
            try:
                # getResponseBlobs(), not getReferencedReleases(): only Releases that
                # are served in place of this one need its Required Signoffs. Matches
                # auslib.db._blob_references.
                served = createBlob(data).getResponseBlobs()
            except (BlobValidationError, ValueError, TypeError):
                continue
            if not isinstance(served, (list, tuple)):
                continue
            edges.extend({"name": name, "referenced": ref} for ref in set(served) if ref)
        # Insert in chunks to avoid oversized statements on large databases.
        for i in range(0, len(edges), 1000):
            conn.execute(ref_table.insert().values(edges[i : i + 1000]))


def upgrade() -> None:
    op.create_table(
        "release_references",
        sa.Column("name", sa.String(100), primary_key=True, nullable=False),
        sa.Column("referenced", sa.String(100), primary_key=True, nullable=False),
    )
    op.create_index("release_references_referenced_idx", "release_references", ["referenced"])

    ref_table = sa.table("release_references", sa.column("name", sa.String), sa.column("referenced", sa.String))
    _backfill(op.get_bind(), ref_table)


def downgrade() -> None:
    op.drop_index("release_references_referenced_idx", table_name="release_references")
    op.drop_table("release_references")
