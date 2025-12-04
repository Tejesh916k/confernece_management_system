import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration from .env or environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = app.config['ENV'] == 'development'
    
    # Session configuration
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400 * 7  # 7 days
    
    # Validate MongoDB URI
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        print("[ERROR] MONGODB_URI not found in environment variables")
        if app.config['ENV'] == 'production':
            raise ValueError('MONGODB_URI environment variable is required')
    elif '<db_password>' in mongodb_uri or '<password>' in mongodb_uri:
        print("[ERROR] MONGODB_URI contains placeholder")
        if app.config['ENV'] == 'production':
            raise ValueError('MONGODB_URI contains unreplaced placeholders')
    
    # Initialize MongoDB Atlas connection
    try:
        from config.database import init_db
        init_db(app)
        print("[OK] MongoDB Atlas connected successfully")
    except Exception as e:
        print(f"[ERROR] MongoDB connection error: {e}")
        if app.config['ENV'] == 'production':
            raise
    
    # Create upload folder
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Register blueprints
    try:
        from controllers.main_routes import main_bp
        from controllers.auth_routes import auth_bp
        from controllers.conference_routes import conference_bp
        from controllers.feature.upload_routes import upload_bp
        from controllers.feature.session_routes import session_bp
        from controllers.feature.payment_routes import payment_bp
        from controllers.feature.report_routes import report_bp
        from controllers.feature.review_routes import review_bp
        from controllers.feature.user_routes import user_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(conference_bp, url_prefix='/conferences')
        app.register_blueprint(upload_bp, url_prefix='/api/upload')
        app.register_blueprint(session_bp)
        app.register_blueprint(payment_bp)
        app.register_blueprint(report_bp)
        app.register_blueprint(review_bp, url_prefix='/reviews')
        app.register_blueprint(user_bp, url_prefix='/users')
        print("[OK] Blueprints registered successfully")
    except ImportError as e:
        print(f"[ERROR] Error loading blueprints: {e}")
        if app.config['ENV'] == 'production':
            raise
    
    return app

# Create app instance for Gunicorn
app = create_app()

if __name__ == '__main__':
    host = os.getenv('HOST', 'localhost')
    port = int(os.getenv('PORT', 5000))
    debug = app.config['ENV'] == 'development'
    
    print(f"\nStarting Flask application...")
    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"Debug: {debug}")
    print(f"Open browser: http://{host}:{port}")
    
    # Disable Flask's auto-reloader for debug mode to prevent double initialization
    app.run(host=host, port=port, debug=debug, use_reloader=False)
