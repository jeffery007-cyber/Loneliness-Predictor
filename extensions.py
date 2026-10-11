"""
extensions.py
--------------
Instantiates Flask extensions WITHOUT binding them to an application.

This is the standard pattern for the Flask Application Factory: extension
objects are created once here (module-level, so every part of the app can
import the same instance), and are only bound to a real Flask app later,
inside create_app(), via each extension's `init_app(app)` method.

Keeping this separate from app/__init__.py avoids circular imports:
models, services, and controllers can `from app.extensions import db`
without ever importing the app factory itself.

NOTE: No models, tables, routes, or authentication logic are defined
here — only the bare extension instances. Actual configuration (e.g.
login_manager.login_view) happens in create_app().
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

# --- Database ORM -----------------------------------------------------------
# Used by every model in app/models/ to define tables and query the
# MySQL database declared in app/config.py.
db = SQLAlchemy()

# --- Password hashing --------------------------------------------------------
# Used by app/services/auth_service.py (to be implemented later) to hash
# and verify user passwords. Never store plaintext passwords.
bcrypt = Bcrypt()

# --- Session / login management ----------------------------------------------
# Manages the logged-in user's session across requests (current_user,
# @login_required, redirect-to-login behaviour, etc.).
login_manager = LoginManager()

# --- Database migrations ------------------------------------------------------
# Tracks incremental changes to the database schema over time so the
# schema can evolve without dropping/recreating tables (flask db migrate/upgrade).
migrate = Migrate()
