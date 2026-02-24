from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from routes import books_bp, members_bp, transactions_bp


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(transactions_bp)

    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'healthy', 'message': 'College Library API is running'}

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)