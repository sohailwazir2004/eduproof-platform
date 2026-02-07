# Core module - Configuration, Security, Dependencies

from app.core.config import settings, get_settings
from app.core.database import Base, get_db, init_db, close_db, engine
from app.core.security import (
    UserRole,
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user_id,
    get_current_user_role,
    RoleChecker,
    require_student,
    require_teacher,
    require_parent,
    require_principal,
    require_admin,
    require_teacher_or_principal,
    oauth2_scheme,
)

__all__ = [
    # Config
    "settings",
    "get_settings",
    # Database
    "Base",
    "get_db",
    "init_db",
    "close_db",
    "engine",
    # Security
    "UserRole",
    "hash_password",
    "verify_password",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "get_current_user_id",
    "get_current_user_role",
    "RoleChecker",
    "require_student",
    "require_teacher",
    "require_parent",
    "require_principal",
    "require_admin",
    "require_teacher_or_principal",
    "oauth2_scheme",
]
