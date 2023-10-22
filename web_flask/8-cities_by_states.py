#!/usr/bin/python3
"""display Hello HBNB!"""

from flask import Flask
from models import storage
from models.state import State
from flask import render_template


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """displays an HTML document 7"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def state_city():
    """displays list of cities"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_session(self):
    '''Removes current SQLAlchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
