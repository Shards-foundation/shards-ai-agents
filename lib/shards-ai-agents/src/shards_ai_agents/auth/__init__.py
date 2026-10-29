"""Authentication utilities — re-exported from ``shards_ai_agents_core.auth``."""

from __future__ import annotations

from shards_ai_agents_core.auth import (
    AuthError as AuthError,
    AuthenticationCommand as AuthenticationCommand,
    Oauth2Settings as Oauth2Settings,
    ProviderFactory as ProviderFactory,
    get_auth_token as get_auth_token,
    validate_jwt_token as validate_jwt_token,
)


__all__ = [
    "AuthError",
    "AuthenticationCommand",
    "Oauth2Settings",
    "ProviderFactory",
    "get_auth_token",
    "validate_jwt_token",
]
