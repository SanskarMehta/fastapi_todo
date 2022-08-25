"""
Class-based FastApi app Configuration.
config class is for base configuration.
"""
import os

from datetime import timedelta
from pydantic import BaseSettings
from pydantic import BaseModel
from logging.config import dictConfig
import logging
from fastapi_mail import ConnectionConfig
SERVER_TYPE_PRODUCTION = "production"
SERVER_TYPE_DEVELOPMENT = "development"


class Settings(BaseSettings):
    # https://pydantic-docs.helpmanual.io/usage/settings/
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    USE_CREDENTIALS: bool = True
    MONGODB_DATABASE_URL: str

    # JWT Token configuration
    JWT_TOKEN_EXPIRES: timedelta = timedelta(hours=48)
    JWT_ALGORITHM: str = "HS384"
    authjwt_header_type: str = "Bearer"
    authjwt_secret_key: str
    # Configure algorithms which is permit
    authjwt_decode_algorithms: set = {"HS384", "HS512"}

    # Domain
    LOCAL_HOST_URL: str

    # database settings.
    AUTOCOMMIT: bool = False
    AUTOFLUSH: bool = False

    class Config:
        env_file = '.env'  # set the env file path.
        env_file_encoding = 'utf-8'


class MailConfig:

    @staticmethod
    def connection_config():
        """
        :return: connection config object.
        """
        return ConnectionConfig(
            MAIL_USERNAME=Settings().MAIL_USERNAME,
            MAIL_PASSWORD=Settings().MAIL_PASSWORD,
            MAIL_FROM=Settings().MAIL_FROM,
            MAIL_PORT=Settings().MAIL_PORT,
            MAIL_SERVER=Settings().MAIL_SERVER,
            MAIL_FROM_NAME=Settings().MAIL_FROM_NAME,
            MAIL_TLS=Settings().MAIL_TLS,
            MAIL_SSL=Settings().MAIL_SSL,
            USE_CREDENTIALS=Settings().USE_CREDENTIALS,
            TEMPLATE_FOLDER='templates/email',
        )


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""
    # https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api

    LOGGER_NAME: str = "fastapi-project"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "fastapi-project": {"handlers": ["default"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger("fastapi-project")


def get_current_server_config():
    """
    This will check FastApi_ENV variable and create an object of configuration according to that
    :return: Production or Development Config object.
    """
    current_config = os.getenv("ENV_FASTAPI_SERVER_TYPE", SERVER_TYPE_DEVELOPMENT)
    return DevelopmentConfig() if current_config == SERVER_TYPE_DEVELOPMENT else ProductionConfig()


class Config(object):
    """
    Set base configuration, env variable configuration and server configuration.
    """
    # The starting execution point of the app.
    FASTAPI_APP = 'main.py'


class DevelopmentConfig(Config):
    """
        This class for generates the config for development instance.
        """
    DEBUG: bool = True
    TESTING: bool = True
    MONGODB_DATABASE_URL = Settings().MONGODB_DATABASE_URL


class ProductionConfig(Config):
    """
    This class for generates the config for the development instance.
    """
    DEBUG: bool = False
    TESTING: bool = False
