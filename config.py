"""
config.py
----------
Centralised configuration for the Digital Loneliness Prediction application.

Defines one base Config class holding settings shared across every
environment, and three environment-specific subclasses (Development,
Testing, Production) that override only what needs to differ.

The active configuration is selected at app-creation time in
app/__init__.py via the `config` dictionary at the bottom of this file,
e.g. create_app('development').

NOTE: This file intentionally contains no database models, ORM setup,
authentication logic, or ML code — configuration values only.
"""

import os
from datetime import timedelta

# Absolute path to the project root (two levels up from this file:
# app/config.py -> app/ -> project root)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config:
    """
    Base configuration.

    Holds settings that are common to every environment. Environment
    variables are preferred over hard-coded values so secrets never
    live in source control — see .env.example for the expected keys.
    """

    # --- Core Flask settings -------------------------------------------------
    # SECRET_KEY signs session cookies and CSRF tokens. A fallback value is
    # provided ONLY for local development convenience; production must
    # always supply SECRET_KEY via environment variable.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # --- Database (MySQL) -----------------------------------------------------
    # Expected format:
    # mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:Arul%402005@localhost:3306/digital_loneliness_db",
    )
    # Disables a SQLAlchemy feature that tracks object modifications and
    # emits signals; not needed here and adds unnecessary overhead.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Logs generated SQL statements to the console; useful in development,
    # noisy and unnecessary in production, so each subclass sets this itself.
    SQLALCHEMY_ECHO = False

    # --- Session settings -------------------------------------------------
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # --- File / upload paths (reserved for future use, e.g. profile pictures)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB max upload size

    # --- Machine learning artifact paths -----------------------------------
    # Paths only — the actual loading/inference logic belongs in
    # app/services/ml_service.py and app/ml/, not here.
    ML_MODEL_DIR = os.path.join(BASE_DIR, "app", "ml", "model_registry")
    ML_BEST_MODEL_PATH = os.path.join(ML_MODEL_DIR, "best_model.pkl")
    ML_SCALER_PATH = os.path.join(ML_MODEL_DIR, "scaler.pkl")
    ML_ENCODER_PATH = os.path.join(ML_MODEL_DIR, "label_encoder.pkl")

    # --- Pagination defaults (used later by history / admin listing pages) --
    RECORDS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        """
        Hook for environment-agnostic app initialisation steps that need
        the `app` instance itself (e.g. ensuring upload folders exist).
        Subclasses can override or extend this. Left as a no-op here so
        the base Config stays purely declarative.
        """
        pass


class DevelopmentConfig(Config):
    """Used for local development. Verbose logging, debug mode enabled."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "mysql+pymysql://root:Arul%402005@localhost:3306/digital_loneliness_db",
    )


class TestingConfig(Config):
    """
    Used when running the automated test suite (tests/).
    Uses a separate database so tests never touch development data,
    and disables CSRF so test clients can POST forms without tokens.
    """

    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "mysql+pymysql://root:Arul%402005@localhost:3306/digital_loneliness_test_db",
    )


class ProductionConfig(Config):
    """
    Used for the deployed application. Debug mode is always off, and
    SECRET_KEY / SQLALCHEMY_DATABASE_URI are required to come from the
    environment — no insecure fallbacks are provided for production.
    """

    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True  # cookies only sent over HTTPS

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        # Fail loudly at startup if critical secrets were not configured,
        # rather than silently running with insecure defaults.
        if app.config["SECRET_KEY"] == "dev-secret-key-change-me":
            raise RuntimeError(
                "SECRET_KEY environment variable must be set in production."
            )


# Maps a short string name (used in create_app(config_name=...)) to the
# corresponding configuration class. 'default' is used when no explicit
# environment is requested.
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
