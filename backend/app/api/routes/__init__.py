# Route Handlers Package
# Import and register all route modules

from app.api.routes import auth, users, homework, submissions, textbooks, analytics, classes

__all__ = [
    "auth",
    "users",
    "homework",
    "submissions",
    "textbooks",
    "analytics",
    "classes"
]
