import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Make sure `app` package is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import settings
from app.database import Base

# Import all models so Alembic can detect them
import app.models.user  # noqa: F401
import app.models.song  # noqa: F401
import app.models.playlist  # noqa: F401
import app.models.radio_station  # noqa: F401
import app.models.pitch_submission  # noqa: F401
import app.models.generated_content  # noqa: F401
import app.models.campaign  # noqa: F401
import app.models.submithub  # noqa: F401
import app.models.dashboard  # noqa: F401
import app.models.post_opportunity  # noqa: F401

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
