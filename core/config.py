# import os
import secrets  # Provides secure random numbers for managing secrets
import warnings  # Issues warning messages to users
from typing import Annotated, Any  # , Literal  # Type hinting utilities

# from pydantic import HttpUrl  # Ensures a string is a valid HTTP URL
from pydantic import AnyUrl  # Represents a validated URL
from pydantic import computed_field  # Decorator for computed properties
from pydantic import (
    model_validator,  # Used to define validation logic at the model level
)
from pydantic import (
    BeforeValidator,
)  # Runs a function before validating a field
from pydantic_settings import (  # Settings management for Pydantic models; SettingsConfigDict,
    BaseSettings,
)
from typing_extensions import Self  # Self type hinting for class methods


def parse_cors(v: Any) -> list[str] | str:
    """Parses a CORS (Cross-Origin Resource Sharing) setting from a string or list."""
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    # model_config = ".env"
    # model_config = SettingsConfigDict(
    #     env_file=".env",  # Specifies the environment file location
    #     # env_ignore_empty=True,  # Ignores empty environment variables
    #     # extra="ignore",  # Ignores extra fields not defined in the model
    # )

    # API_V1_STR: str = "/api/v1"  # API version prefix

    SECRET_KEY: str = secrets.token_urlsafe(
        32
    )  # Generates a secure random key

    # ACCESS_TOKEN_EXPIRE_MINUTES: int = (
    #     60 * 24 * 8
    # )  # Token expiration time (8 days)

    # FIRST_SUPERUSER: EmailStr  # Superuser email (must be set in environment)
    # FIRST_SUPERUSER_PASSWORD: (
    #     str  # Superuser password (must be set in environment)
    # )

    FRONTEND_HOST: str = "http://localhost:5173"  # Frontend application URL

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []  # Defines allowed CORS origins

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        """Returns a list of all CORS origins including the frontend host."""
        return [
            str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS
        ] + [self.FRONTEND_HOST]

    PROJECT_NAME: str = (
        "Project Test"  # Project name (must be set in environment variables)
    )

    POSTGRES_SERVER: str  # PostgreSQL server address
    POSTGRES_PORT: int  # Default PostgreSQL port
    POSTGRES_USER: str  # PostgreSQL username
    POSTGRES_PASSWORD: str  # PostgreSQL password (default empty)
    POSTGRES_DB: str  # PostgreSQL database name

    def _check_default_secret(self, var_name: str, value: str | None) -> None:
        """Checks if a sensitive secret has the default value and warns or raises an error."""
        if value == "changethis":
            message = (
                f'The value of {var_name} is "changethis", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "local":
                warnings.warn(
                    message, stacklevel=1
                )  # Issues a warning in local environment
            else:
                raise ValueError(
                    message
                )  # Raises an error in staging/production

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        """Ensures that critical secrets are not left at their default values."""
        self._check_default_secret("SECRET_KEY", self.SECRET_KEY)
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
        # self._check_default_secret(
        #     "FIRST_SUPERUSER_PASSWORD", self.FIRST_SUPERUSER_PASSWORD
        # )
        return self


settings = Settings()  # Loads settings from environment variables or defaults
