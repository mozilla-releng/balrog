"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-02-17 00:00:00.000000

Creates all initial database tables.
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all database tables."""
    op.create_table(
        "dockerflow",
        sa.Column("watchdog", sa.Integer(), nullable=False),
    )
    op.create_table(
        "emergency_shutoffs",
        sa.Column("product", sa.String(15), primary_key=True, nullable=False),
        sa.Column("channel", sa.String(75), primary_key=True, nullable=False),
        sa.Column("comment", sa.String(500)),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "emergency_shutoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("channel", sa.String(75), nullable=False),
        sa.Column("comment", sa.String(500)),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_product", sa.String(15), nullable=False),
        sa.Column("base_channel", sa.String(75), nullable=False),
        sa.Column("base_comment", sa.String(500)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_channel", sa.String(75)),
        sa.Column("base_comment", sa.String(500)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "emergency_shutoffs_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "permissions",
        sa.Column("permission", sa.String(50), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("options", sa.Text()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("permission", sa.String(50), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("options", sa.Text()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_req_signoffs",
        sa.Column("product", sa.String(15), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), primary_key=True, nullable=False),
        sa.Column("signoffs_required", sa.Integer(), nullable=False),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_req_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("signoffs_required", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_product", sa.String(15), nullable=False),
        sa.Column("base_role", sa.String(50), nullable=False),
        sa.Column("base_signoffs_required", sa.Integer()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_role", sa.String(50)),
        sa.Column("base_signoffs_required", sa.Integer()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "permissions_req_signoffs_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "permissions_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_permission", sa.String(50), nullable=False),
        sa.Column("base_username", sa.String(100), nullable=False),
        sa.Column("base_options", sa.Text()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "permissions_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_permission", sa.String(50)),
        sa.Column("base_username", sa.String(100)),
        sa.Column("base_options", sa.Text()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "permissions_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "permissions_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "pinnable_releases",
        sa.Column("product", sa.String(15), primary_key=True, nullable=False),
        sa.Column("version", sa.String(75), primary_key=True, nullable=False),
        sa.Column("channel", sa.String(75), primary_key=True, nullable=False),
        sa.Column("mapping", sa.String(100), nullable=False),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "pinnable_releases_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("version", sa.String(75), nullable=False),
        sa.Column("channel", sa.String(75), nullable=False),
        sa.Column("mapping", sa.String(100)),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_product", sa.String(15), nullable=False),
        sa.Column("base_version", sa.String(75), nullable=False),
        sa.Column("base_channel", sa.String(75), nullable=False),
        sa.Column("base_mapping", sa.String(100)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_version", sa.String(75)),
        sa.Column("base_channel", sa.String(75)),
        sa.Column("base_mapping", sa.String(100)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "pinnable_releases_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "product_req_signoffs",
        sa.Column("product", sa.String(15), primary_key=True, nullable=False),
        sa.Column("channel", sa.String(75), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), primary_key=True, nullable=False),
        sa.Column("signoffs_required", sa.Integer(), nullable=False),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "product_req_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("channel", sa.String(75), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("signoffs_required", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_product", sa.String(15), nullable=False),
        sa.Column("base_channel", sa.String(75), nullable=False),
        sa.Column("base_role", sa.String(50), nullable=False),
        sa.Column("base_signoffs_required", sa.Integer()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_channel", sa.String(75)),
        sa.Column("base_role", sa.String(50)),
        sa.Column("base_signoffs_required", sa.Integer()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "product_req_signoffs_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "release_assets",
        sa.Column("name", sa.String(100), primary_key=True, nullable=False),
        sa.Column("path", sa.String(200), primary_key=True, nullable=False),
        sa.Column("data", sa.JSON()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "release_assets_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_name", sa.String(100), nullable=False),
        sa.Column("base_path", sa.String(200), nullable=False),
        sa.Column("base_data", sa.JSON()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "release_assets_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "release_assets_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "release_assets_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_name", sa.String(100)),
        sa.Column("base_path", sa.String(200)),
        sa.Column("base_data", sa.JSON()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "release_assets_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "release_assets_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "releases",
        sa.Column("name", sa.String(100), primary_key=True, nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("read_only", sa.Boolean()),
        sa.Column("data", sa.Text(), nullable=False),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_json",
        sa.Column("name", sa.String(100), primary_key=True, nullable=False),
        sa.Column("product", sa.String(15), nullable=False),
        sa.Column("read_only", sa.Boolean()),
        sa.Column("data", sa.JSON()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_json_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_name", sa.String(100), nullable=False),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_read_only", sa.Boolean()),
        sa.Column("base_data", sa.JSON()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_json_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_json_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "releases_json_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_name", sa.String(100)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_read_only", sa.Boolean()),
        sa.Column("base_data", sa.JSON()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "releases_json_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "releases_json_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "releases_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_name", sa.String(100), nullable=False),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_read_only", sa.Boolean()),
        sa.Column("base_data", sa.Text()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "releases_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "releases_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_name", sa.String(100)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_read_only", sa.Boolean()),
        sa.Column("base_data", sa.Text()),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "releases_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "releases_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "rules",
        sa.Column("rule_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("alias", sa.String(50)),
        sa.Column("priority", sa.Integer()),
        sa.Column("mapping", sa.String(100)),
        sa.Column("fallbackMapping", sa.String(100)),
        sa.Column("backgroundRate", sa.Integer()),
        sa.Column("update_type", sa.String(15), nullable=False),
        sa.Column("product", sa.String(15)),
        sa.Column("version", sa.String(75)),
        sa.Column("channel", sa.String(75)),
        sa.Column("buildTarget", sa.String(75)),
        sa.Column("buildID", sa.String(20)),
        sa.Column("locale", sa.String(200)),
        sa.Column("osVersion", sa.String(1000)),
        sa.Column("memory", sa.String(100)),
        sa.Column("instructionSet", sa.String(1000)),
        sa.Column("jaws", sa.Integer()),
        sa.Column("mig64", sa.Integer()),
        sa.Column("distribution", sa.String(2000)),
        sa.Column("distVersion", sa.String(100)),
        sa.Column("headerArchitecture", sa.String(10)),
        sa.Column("comment", sa.String(500)),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "rules_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("rule_id", sa.Integer(), nullable=False),
        sa.Column("alias", sa.String(50)),
        sa.Column("priority", sa.Integer()),
        sa.Column("mapping", sa.String(100)),
        sa.Column("fallbackMapping", sa.String(100)),
        sa.Column("backgroundRate", sa.Integer()),
        sa.Column("update_type", sa.String(15)),
        sa.Column("product", sa.String(15)),
        sa.Column("version", sa.String(75)),
        sa.Column("channel", sa.String(75)),
        sa.Column("buildTarget", sa.String(75)),
        sa.Column("buildID", sa.String(20)),
        sa.Column("locale", sa.String(200)),
        sa.Column("osVersion", sa.String(1000)),
        sa.Column("memory", sa.String(100)),
        sa.Column("instructionSet", sa.String(1000)),
        sa.Column("jaws", sa.Integer()),
        sa.Column("mig64", sa.Integer()),
        sa.Column("distribution", sa.String(2000)),
        sa.Column("distVersion", sa.String(100)),
        sa.Column("headerArchitecture", sa.String(10)),
        sa.Column("comment", sa.String(500)),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "rules_scheduled_changes",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("scheduled_by", sa.String(100), nullable=False),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("base_rule_id", sa.Integer()),
        sa.Column("base_alias", sa.String(50)),
        sa.Column("base_priority", sa.Integer()),
        sa.Column("base_mapping", sa.String(100)),
        sa.Column("base_fallbackMapping", sa.String(100)),
        sa.Column("base_backgroundRate", sa.Integer()),
        sa.Column("base_update_type", sa.String(15)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_version", sa.String(75)),
        sa.Column("base_channel", sa.String(75)),
        sa.Column("base_buildTarget", sa.String(75)),
        sa.Column("base_buildID", sa.String(20)),
        sa.Column("base_locale", sa.String(200)),
        sa.Column("base_osVersion", sa.String(1000)),
        sa.Column("base_memory", sa.String(100)),
        sa.Column("base_instructionSet", sa.String(1000)),
        sa.Column("base_jaws", sa.Integer()),
        sa.Column("base_mig64", sa.Integer()),
        sa.Column("base_distribution", sa.String(2000)),
        sa.Column("base_distVersion", sa.String(100)),
        sa.Column("base_headerArchitecture", sa.String(10)),
        sa.Column("base_comment", sa.String(500)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "rules_scheduled_changes_conditions",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("telemetry_product", sa.String(15)),
        sa.Column("telemetry_channel", sa.String(75)),
        sa.Column("telemetry_uptake", sa.Integer()),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "rules_scheduled_changes_conditions_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("telemetry_product", sa.String(15)),
        sa.Column("telemetry_channel", sa.String(75)),
        sa.Column("telemetry_uptake", sa.Integer()),
        sa.Column("when", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "rules_scheduled_changes_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("scheduled_by", sa.String(100)),
        sa.Column("complete", sa.Boolean()),
        sa.Column("change_type", sa.String(50)),
        sa.Column("base_rule_id", sa.Integer()),
        sa.Column("base_alias", sa.String(50)),
        sa.Column("base_priority", sa.Integer()),
        sa.Column("base_mapping", sa.String(100)),
        sa.Column("base_fallbackMapping", sa.String(100)),
        sa.Column("base_backgroundRate", sa.Integer()),
        sa.Column("base_update_type", sa.String(15)),
        sa.Column("base_product", sa.String(15)),
        sa.Column("base_version", sa.String(75)),
        sa.Column("base_channel", sa.String(75)),
        sa.Column("base_buildTarget", sa.String(75)),
        sa.Column("base_buildID", sa.String(20)),
        sa.Column("base_locale", sa.String(200)),
        sa.Column("base_osVersion", sa.String(1000)),
        sa.Column("base_memory", sa.String(100)),
        sa.Column("base_instructionSet", sa.String(1000)),
        sa.Column("base_jaws", sa.Integer()),
        sa.Column("base_mig64", sa.Integer()),
        sa.Column("base_distribution", sa.String(2000)),
        sa.Column("base_distVersion", sa.String(100)),
        sa.Column("base_headerArchitecture", sa.String(10)),
        sa.Column("base_comment", sa.String(500)),
        sa.Column("base_data_version", sa.Integer()),
        sa.Column("data_version", sa.Integer()),
    )
    op.create_table(
        "rules_scheduled_changes_signoffs",
        sa.Column("sc_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
    )
    op.create_table(
        "rules_scheduled_changes_signoffs_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("sc_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50)),
    )
    op.create_table(
        "user_roles",
        sa.Column("username", sa.String(100), primary_key=True, nullable=False),
        sa.Column("role", sa.String(50), primary_key=True, nullable=False),
        sa.Column("data_version", sa.Integer(), nullable=False),
    )
    op.create_table(
        "user_roles_history",
        sa.Column("change_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("changed_by", sa.String(100), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("data_version", sa.Integer()),
    )


def downgrade() -> None:
    """Drop all database tables."""
    op.drop_table("user_roles_history")
    op.drop_table("user_roles")
    op.drop_table("rules_scheduled_changes_signoffs_history")
    op.drop_table("rules_scheduled_changes_signoffs")
    op.drop_table("rules_scheduled_changes_history")
    op.drop_table("rules_scheduled_changes_conditions_history")
    op.drop_table("rules_scheduled_changes_conditions")
    op.drop_table("rules_scheduled_changes")
    op.drop_table("rules_history")
    op.drop_table("rules")
    op.drop_table("releases_scheduled_changes_signoffs_history")
    op.drop_table("releases_scheduled_changes_signoffs")
    op.drop_table("releases_scheduled_changes_history")
    op.drop_table("releases_scheduled_changes_conditions_history")
    op.drop_table("releases_scheduled_changes_conditions")
    op.drop_table("releases_scheduled_changes")
    op.drop_table("releases_json_scheduled_changes_signoffs_history")
    op.drop_table("releases_json_scheduled_changes_signoffs")
    op.drop_table("releases_json_scheduled_changes_history")
    op.drop_table("releases_json_scheduled_changes_conditions_history")
    op.drop_table("releases_json_scheduled_changes_conditions")
    op.drop_table("releases_json_scheduled_changes")
    op.drop_table("releases_json")
    op.drop_table("releases")
    op.drop_table("release_assets_scheduled_changes_signoffs_history")
    op.drop_table("release_assets_scheduled_changes_signoffs")
    op.drop_table("release_assets_scheduled_changes_history")
    op.drop_table("release_assets_scheduled_changes_conditions_history")
    op.drop_table("release_assets_scheduled_changes_conditions")
    op.drop_table("release_assets_scheduled_changes")
    op.drop_table("release_assets")
    op.drop_table("product_req_signoffs_scheduled_changes_signoffs_history")
    op.drop_table("product_req_signoffs_scheduled_changes_signoffs")
    op.drop_table("product_req_signoffs_scheduled_changes_history")
    op.drop_table("product_req_signoffs_scheduled_changes_conditions_history")
    op.drop_table("product_req_signoffs_scheduled_changes_conditions")
    op.drop_table("product_req_signoffs_scheduled_changes")
    op.drop_table("product_req_signoffs_history")
    op.drop_table("product_req_signoffs")
    op.drop_table("pinnable_releases_scheduled_changes_signoffs_history")
    op.drop_table("pinnable_releases_scheduled_changes_signoffs")
    op.drop_table("pinnable_releases_scheduled_changes_history")
    op.drop_table("pinnable_releases_scheduled_changes_conditions_history")
    op.drop_table("pinnable_releases_scheduled_changes_conditions")
    op.drop_table("pinnable_releases_scheduled_changes")
    op.drop_table("pinnable_releases_history")
    op.drop_table("pinnable_releases")
    op.drop_table("permissions_scheduled_changes_signoffs_history")
    op.drop_table("permissions_scheduled_changes_signoffs")
    op.drop_table("permissions_scheduled_changes_history")
    op.drop_table("permissions_scheduled_changes_conditions_history")
    op.drop_table("permissions_scheduled_changes_conditions")
    op.drop_table("permissions_scheduled_changes")
    op.drop_table("permissions_req_signoffs_scheduled_changes_signoffs_history")
    op.drop_table("permissions_req_signoffs_scheduled_changes_signoffs")
    op.drop_table("permissions_req_signoffs_scheduled_changes_history")
    op.drop_table("permissions_req_signoffs_scheduled_changes_conditions_history")
    op.drop_table("permissions_req_signoffs_scheduled_changes_conditions")
    op.drop_table("permissions_req_signoffs_scheduled_changes")
    op.drop_table("permissions_req_signoffs_history")
    op.drop_table("permissions_req_signoffs")
    op.drop_table("permissions_history")
    op.drop_table("permissions")
    op.drop_table("emergency_shutoffs_scheduled_changes_signoffs_history")
    op.drop_table("emergency_shutoffs_scheduled_changes_signoffs")
    op.drop_table("emergency_shutoffs_scheduled_changes_history")
    op.drop_table("emergency_shutoffs_scheduled_changes_conditions_history")
    op.drop_table("emergency_shutoffs_scheduled_changes_conditions")
    op.drop_table("emergency_shutoffs_scheduled_changes")
    op.drop_table("emergency_shutoffs_history")
    op.drop_table("emergency_shutoffs")
    op.drop_table("dockerflow")
