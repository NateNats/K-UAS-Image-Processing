import os

APP_NAME = "UAS Pemrosesan Citra"
APP_VERSION = "1.0.0"
APP_AUTHOR = ["Nicolaus Reva Sagraha", "Gabriel Bayu H", "Nicholas Pratama", "Joseph Aprilio"]

def get_project_root():
    return os.path.dirname(os.path.abspath(__file__))

def format_title():
    return f"{APP_NAME} v{APP_VERSION}"

def format_author():
    return " | ".join(APP_AUTHOR)