from flask import Flask, render_template, flash, redirect, url_for, session, logging
from helpers.database import Database
from helpers.reality import *


from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt


app = Flask(__name__)

db = Database(host="innodb.endora.cz",
                user="realityuser",
                password="Ab1122334455",
                database="realitydb")


@app.route('/')
def index():
    ## TODO: finish loading realities from DB
    realities = parse_many_from_db(db.get_realities())
    for key, reality in enumerate(realities):
        history_list = parse_history_from_db(db.get_reality_history_by_id(reality.id))
        reality.set_history(history_list)
        if key == 5:
            break
    return render_template('index.html', realities=realities)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def energy():


    return render_template('energy.html',)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
