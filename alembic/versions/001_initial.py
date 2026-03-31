"""initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(200), unique=True, nullable=False),
        sa.Column(
            "role",
            sa.Enum("REQUESTER", "RH", name="roleenum"),
            nullable=False,
        ),
    )

    # vacancies
    op.create_table(
        "vacancies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column(
            "priority",
            sa.Enum("LOW", "MEDIUM", "HIGH", "CRITICAL", name="priorityenum"),
            nullable=False,
            server_default="MEDIUM",
        ),
        sa.Column(
            "status",
            sa.Enum(
                "DRAFT", "PENDING_APPROVAL", "APPROVED", "REJECTED",
                "IN_PROGRESS", "FINALIZED",
                name="vacancystatus",
            ),
            nullable=False,
            server_default="DRAFT",
        ),
        sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_vacancies_id", "vacancies", ["id"])

    # requirements
    op.create_table(
        "requirements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id"), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "SKILL", "LANGUAGE", "CERTIFICATION", "EDUCATION", "COMPANY", "LOCATION",
                name="requirementtype",
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("level", sa.String(100), nullable=True),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("mandatory", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # approval_decisions
    op.create_table(
        "approval_decisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id"), nullable=False),
        sa.Column("rh_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column(
            "decision",
            sa.Enum("APPROVED", "REJECTED", name="decisionenum"),
            nullable=False,
        ),
        sa.Column("justification", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # audit_events
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor_user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("metadata_json", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    # candidate_suggestions
    op.create_table(
        "candidate_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id"), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("headline", sa.String(300), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("explanation_json", postgresql.JSON(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("candidate_suggestions")
    op.drop_table("audit_events")
    op.drop_table("approval_decisions")
    op.drop_table("requirements")
    op.drop_table("vacancies")
    op.drop_table("users")

    for enum_name in [
        "roleenum", "priorityenum", "vacancystatus",
        "requirementtype", "decisionenum",
    ]:
        op.execute(f"DROP TYPE IF EXISTS {enum_name}")
