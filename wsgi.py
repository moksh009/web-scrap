#!/usr/bin/env python3
"""
WSGI entry point for production deployment on Render
"""

from app import app, socketio

if __name__ == "__main__":
    socketio.run(app)
