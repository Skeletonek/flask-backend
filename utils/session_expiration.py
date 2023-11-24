from flask import session
from datetime import timedelta

def session_expiration(app):
    session.permanent = True
    app.permament_session_lifetime = timedelta(minutes=1)
    return app.permament_session_lifetime