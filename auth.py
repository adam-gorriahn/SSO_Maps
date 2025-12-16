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

# Check if we're likely running locally (not in a cloud environment)
# Note: Render doesn't set a RENDER env var, so we rely on ADMIN_PASSWORD being set
# If ADMIN_PASSWORD is set, auth is always enabled regardless of environment
IS_LOCAL = (
    os.getenv('RENDER') is None and 
    os.getenv('DYNO') is None and 
    os.getenv('RAILWAY_ENVIRONMENT') is None and
    os.getenv('VERCEL') is None
)

# Default password for local development
# Allow default password if: DEBUG_MODE is True OR we're running locally without ADMIN_PASSWORD set
# This prevents errors when running locally, but still requires password in production
if not ADMIN_PASSWORD:
    if DEBUG_MODE or IS_LOCAL:
        ADMIN_PASSWORD = 'admin'  # Default for local development only
    else:
        raise ValueError(
            "ADMIN_PASSWORD environment variable must be set in production. "
            "Set it in your deployment platform's environment variables. "
            "For local testing, the app will use 'admin' as default password."
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

