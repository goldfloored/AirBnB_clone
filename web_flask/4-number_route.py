#!/usr/bin/python3
"""starts Flask web application"""
from flask import Flask
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
