from flask import Flask
from models import db
from routes.users import users
from routes.courses import courses
from routes.enrollment import enrollment
from routes.main import main
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Configure Flask-Session
    app.config['SESSION_TYPE'] = 'filesystem'  # Or 'redis', 'memcached', etc.
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    db.init_app(app)
    Session(app)
    # Register Blueprints
    app.register_blueprint(users, url_prefix='/api')
    app.register_blueprint(courses, url_prefix='/api')
    app.register_blueprint(enrollment, url_prefix='/api')
    app.register_blueprint(main)  # Register the main blueprint

    with app.app_context():
        # Create all tables
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
