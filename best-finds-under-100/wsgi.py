"""WSGI entry point for non-Replit hosts (PythonAnywhere, gunicorn, Render, etc.).

PythonAnywhere: in the Web tab's WSGI config file, use:

    import sys
    sys.path.insert(0, '/home/YOUR_USERNAME/flohouse-cmyk.github.io/best-finds-under-100')
    from wsgi import application

gunicorn: gunicorn wsgi:application
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app as application
