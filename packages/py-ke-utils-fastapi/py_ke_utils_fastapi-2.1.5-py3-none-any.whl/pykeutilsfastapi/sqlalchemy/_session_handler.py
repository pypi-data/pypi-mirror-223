import logging
from typing import Annotated

from alembic import command
from alembic.config import Config
from fastapi import Header, HTTPException, status
from sqlalchemy import inspect, text, Engine
from sqlalchemy.orm import Session, sessionmaker

from ..tenant import tenant_extractor


class SessionHandler:
    """
    Dependency class for FastAPI. It handles the sessions for API.
    :param session_local: The SessionMaker of the API.
    :param engine: The SQLAlchemy Database engine.
    :param alembic_config: Alembic config.
    :param default_tenant: Default tenant.
    """

    def __init__(
            self,
            session_local: sessionmaker,
            engine: Engine,
            alembic_config: Config,
            default_tenant: str = 'public'
    ):
        self.session_local = session_local
        self.engine = engine
        self.alembic_config = alembic_config
        self.default_tenant = default_tenant

    def __call__(
            self,
            x_tenant_id: Annotated[str | None, Header()] = None,
            origin: Annotated[str | None, Header()] = None,
    ) -> Session:
        session = self.session_local()
        try:
            subdomain = f"tenant_{tenant_extractor(str(origin), x_tenant_id, self.default_tenant)}"
            if subdomain not in inspect(self.engine).get_schema_names():
                logging.error(f"Schema - {subdomain} is not in the database.")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Schema {subdomain} does not exists in the database",
                )
            logging.info("Changing Schema.")
            session.execute(text(f"SET search_path TO {subdomain}"))

            logging.info("Upgrading Database.")
            self.alembic_config.set_main_option('tenant_name', subdomain)
            command.upgrade(self.alembic_config, 'head')

            yield session
        finally:
            session.close()
