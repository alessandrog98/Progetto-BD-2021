from flask import url_for
from flask_login import current_user
from context import app
from datetime import datetime


def static(filename):
    return url_for('static', filename=filename)


@app.context_processor
def context():
    return {
        'now': datetime.utcnow(),
        'static': static,
        'user': current_user if current_user.is_authenticated else None,
    }
