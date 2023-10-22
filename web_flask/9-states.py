#!/usr/bin/python3
"""display Hello HBNB!"""

from flask import Flask
from models import storage
from models.state import State
from flask import render_template


app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def states():
    """Returns a template with all the states in storage"""
    states = storage.all(State).values()
    return render_template("9-states.html", states=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id(id):
    """finds city with id"""
    states = storage.all(State).values()
    for state in states:
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html", not_found=True)


@app.teardown_appcontext
def close_session(self):
    """Removes current SQLAlchemy session"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
