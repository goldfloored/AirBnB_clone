#!/usr/bin/python3
"""starts Flask web application"""
from flask import Flask
from flask import render_template
from models import storage
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """displays a message"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """displays a message"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """displays "C" followed value of text variable"""
    return "C %s" % text.replace("_", " ")


@app.route('/python/', defaults={'text': "is_cool"})
@app.route('/python/<text>', strict_slashes=False)
def py_text(text):
    """displays "Python" followed by value of text variable"""
    return "Python %s" % text.replace("_", " ")


@app.route('/number/<int:n>', strict_slashes=False)
def num_n(n):
    """displays the number entered followed by "is a number" """
    return "%d is a number" % n


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template(n):
    """displays a HTML page if n is an integer"""
    return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_even_num(n):
    """displays a HTML page if n is an integer"""
    return render_template('6-number_odd_or_even.html', n=n)


@app.route('/states_list', strict_slashes=False)
def states_l():
    """displays a HTML page"""
    l_states = storage.all("State").values()
    return render_template('7-states_list.html', l_states=l_states)


@app.route('/cities_by_states', strict_slashes=False)
def cities_l():
    """displays a HTML page"""
    l_states = storage.all("State").values()
    return render_template('8-cities_by_states.html', l_states=l_states)


@app.teardown_appcontext
def rm_curr_session(self):
    """removes the current SQLAlchemy Session"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
