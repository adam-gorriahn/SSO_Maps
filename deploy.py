#!/usr/bin/env python3
"""
Production deployment script for the Agentic Dataverse Visualizer
"""
import os
import sys
import subprocess
import argparse

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import dash
        import plotly
        import numpy
        import dash_vtk
        import dash_leaflet
        import pyvista
        import pandas
        import sklearn
        import scipy
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def run_production():
    """Run the app in production mode"""
    print("🚀 Starting production server...")
    
    # Set production environment variables
    env = os.environ.copy()
    env['DEBUG_MODE'] = 'False'
    env['HOST'] = '0.0.0.0'
    env['PORT'] = '8050'
    
    try:
        subprocess.run([sys.executable, 'app.py'], env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def run_development():
    """Run the app in development mode"""
    print("🔧 Starting development server...")
    
    # Set development environment variables
    env = os.environ.copy()
    env['DEBUG_MODE'] = 'True'
    env['HOST'] = '127.0.0.1'
    env['PORT'] = '8050'
    
    try:
        subprocess.run([sys.executable, 'app.py'], env=env, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Deploy the Agentic Dataverse Visualizer')
    parser.add_argument('--mode', choices=['dev', 'prod'], default='dev',
                       help='Run in development or production mode')
    parser.add_argument('--check', action='store_true',
                       help='Only check requirements, do not start server')
    
    args = parser.parse_args()
    
    print("🔍 Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    if args.check:
        print("✅ All checks passed!")
        return
    
    if args.mode == 'prod':
        run_production()
    else:
        run_development()

if __name__ == "__main__":
    main()
