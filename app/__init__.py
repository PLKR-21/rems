from flask import Flask, render_template
import os
import logging
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    
    # Set up logging
    if not app.debug:
        logging.basicConfig(level=logging.INFO)
        app.logger.setLevel(logging.INFO)
    
    # Register blueprints
    from app.routes.main import main
    from app.routes.properties import properties
    from app.routes.owners import owners
    from app.routes.tenants import tenants
    from app.routes.leases import leases
    from app.routes.payments import payments
    
    app.register_blueprint(main)
    app.register_blueprint(properties)
    app.register_blueprint(owners)
    app.register_blueprint(tenants)
    app.register_blueprint(leases)
    app.register_blueprint(payments)
    
    # Error handlers
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('Server Error: %s', error)
        return render_template('error.html', error=error), 500
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error=error), 404
    
    return app 