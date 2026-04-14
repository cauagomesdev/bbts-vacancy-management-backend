"""sprint2 - candidates + integration_log
Revision ID: 002
Revises: 001
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("headline", sa.String(300), nullable=False, server_default=""),
        sa.Column("email", sa.String(200), nullable=True, unique=True),
        sa.Column("location", sa.String(200), nullable=False, server_default=""),
        sa.Column("linkedin_url", sa.String(400), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_table("candidate_skills",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("level", sa.String(100), nullable=True),
        sa.Column("years_experience", sa.Float(), nullable=True),
    )
    op.create_table("candidate_experiences",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("company", sa.String(200), nullable=False),
        sa.Column("role", sa.String(200), nullable=False),
        sa.Column("start_year", sa.Integer(), nullable=True),
        sa.Column("end_year", sa.Integer(), nullable=True),
        sa.Column("current", sa.Boolean(), nullable=False, server_default="false"),
    )
    op.create_table("candidate_educations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("institution", sa.String(200), nullable=False),
        sa.Column("course", sa.String(200), nullable=False),
        sa.Column("degree", sa.String(100), nullable=True),
        sa.Column("graduation_year", sa.Integer(), nullable=True),
    )
    op.create_table("candidate_languages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("level", sa.String(100), nullable=True),
    )
    op.create_table("candidate_certifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("issuer", sa.String(200), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
    )
    op.drop_table("candidate_suggestions")
    op.create_table("candidate_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id"), nullable=False),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidates.id"), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("explanation_json", postgresql.JSON(), nullable=False),
    )
    op.create_table("integration_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("filename", sa.String(300), nullable=True),
        sa.Column("status", sa.Enum("SUCCESS","PARTIAL","FAILED", name="integrationstatus"), nullable=False),
        sa.Column("total_records", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("errors_json", postgresql.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table("integration_logs")
    op.drop_table("candidate_suggestions")
    for t in ["candidate_certifications","candidate_languages","candidate_educations","candidate_experiences","candidate_skills","candidates"]:
        op.drop_table(t)
    op.execute("DROP TYPE IF EXISTS integrationstatus")
    op.create_table("candidate_suggestions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("vacancy_id", sa.Integer(), sa.ForeignKey("vacancies.id"), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("headline", sa.String(300), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("explanation_json", postgresql.JSON(), nullable=False),
    )
