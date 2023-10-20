#!/usr/bin/python3
"""a script that starts a Flask web application"""


from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def state_list():
    """fetches data from the storage engine"""
    states = storage.all(State)
    return render_template("7-states_list.py", state=states)


@app.teardown_appcontext
def close_session():
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
