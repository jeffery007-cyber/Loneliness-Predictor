"""
app/__init__.py
-----------------
The Flask Application Factory.

Rather than creating a single global `app = Flask(__name__)` at import
time, this module exposes a create_app() function that builds and
returns a fully configured Flask application on demand. This is the
recommended pattern for larger Flask projects because it:

  - Allows multiple app instances with different configs (dev/test/prod)
    to be created in the same process, which is essential for testing.
  - Avoids circular imports: extensions and models are defined
    independently and only wired together inside create_app().
  - Keeps configuration, extension setup, and blueprint registration
    in one clearly readable place.
"""

from flask import Flask

from app.config import config
from app.extensions import db, bcrypt, login_manager, migrate


def create_app(config_name="default"):
    """
    Application factory.

    Args:
        config_name (str): Which configuration to load — one of
            'development', 'testing', 'production', or 'default'.
            Defaults to 'default' (DevelopmentConfig) if not specified.

    Returns:
        Flask: A fully configured Flask application instance, ready to
        run or to be handed to a test client.
    """
    app = Flask(__name__)

    # --- Load configuration -------------------------------------------------
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # --- Initialise extensions -----------------------------------------------
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"
    migrate.init_app(app, db)

    # Import all models so Flask-Migrate can detect them during autogenerate.
    from app.models import AssessmentHistory, Question, User, VideoRecommendation  # noqa: F401

    # --- Register blueprints (controllers) ------------------------------------
    from app.controllers.assessment_controller import assessment_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.history_controller import history_bp
    from app.controllers.main_controller import main_bp
    from app.controllers.profile_controller import profile_bp
    from app.controllers.question_controller import question_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(profile_bp)

    return app
