import flask
from flask_sqlalchemy import SQLAlchemy

# Flask instance
app = flask.Flask('home_manager')
db = SQLAlchemy()

class BaseConfig():
    """
    Base configuration model for the application.

    Flask pulls configuration. No instantiation required.
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test_password@localhost/home_manager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Prevent CSRF attacks
    SECRET_KEY = 'secret'


# Load configuration
def __init__():
    app.config.from_object(BaseConfig())
    db.init_app(app)

    with app.app_context():
        # Register db models
        import camera, thermostat

        db.create_all()

        # Register blueprints
        app.register_blueprint(camera.camera)
        app.register_blueprint(thermostat.thermostat)

__init__()