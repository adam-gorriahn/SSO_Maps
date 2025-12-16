"""
Password authentication middleware for Dash application
"""
import os
from functools import wraps
from flask import request, Response, session, redirect, url_for
import hashlib
import secrets

# Get password from environment variable
# In production, ADMIN_PASSWORD MUST be set via environment variable
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

# Default password only for local development (when DEBUG_MODE is True)
if not ADMIN_PASSWORD and DEBUG_MODE:
    ADMIN_PASSWORD = 'admin'  # Default for local development only
elif not ADMIN_PASSWORD:
    raise ValueError(
        "ADMIN_PASSWORD environment variable must be set in production. "
        "Set it in your deployment platform's environment variables."
    )

SESSION_SECRET_KEY = os.getenv('SESSION_SECRET_KEY', secrets.token_hex(32))

def check_auth(username, password):
    """Check if username/password combination is valid"""
    # Simple single password check (username is ignored but required for basic auth)
    return password == ADMIN_PASSWORD

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Please enter your password to access this site',
        401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    """Decorator to require authentication for a route"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def init_auth(app):
    """Initialize authentication for the Dash app"""
    # Set secret key for sessions
    app.server.secret_key = SESSION_SECRET_KEY
    
    # Protect all routes with basic authentication
    @app.server.before_request
    def require_auth():
        # Skip authentication for static assets
        if request.path.startswith('/_dash') or request.path.startswith('/assets'):
            return None
        
        # Check if user is already authenticated via session
        if session.get('authenticated'):
            return None
        
        # Check basic auth
        auth = request.authorization
        if auth and check_auth(auth.username, auth.password):
            session['authenticated'] = True
            return None
        
        # Require authentication
        return authenticate()
    
    return app

