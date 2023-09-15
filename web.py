from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
import configparser, os
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from helpers.database import Database
from helpers.reality import *

app = Flask(__name__)
project_dir = os.path.dirname(__file__)

# Config MySQL
config = configparser.ConfigParser()
config.read(os.path.join(project_dir,'config.conf'))
db = Database(**dict(config["database"]))

@app.route('/')
def index():
    ## TODO: finish loading realities from DB
    realities = parse_many_from_db(db.get_realities())
    expired_realities = []
    for index, reality in enumerate(realities, 0):
        history_list = parse_history_from_db(db.get_reality_history_by_id(reality.id))
        reality.set_history(history_list)
        if reality.flags:
            reality.flags = reality.flags.split(',')
            if 'EXPIRED' in reality.flags:
                print("Expired reality:", reality.id, reality.title)
                expired_realities.append(reality)
                del realities[index]
                # TODO: FINISH HIDE OF EXPIRED REALITIES
    return render_template('index.html', realities=realities, expired_realities=expired_realities)

# Set reality flags
@app.route('/reality_set', methods=['POST'])
def reality_set():
    if request.method == 'POST':
        # TODO: finish favourite/disable
        reality_id = int(request.form['reality_id'])
        action = request.form['action']
        # TODO: LATEST: pass current_state and invert it to save into DB
        current_state = request.form['current_state']
        print("reality_set_flag triggered with: ", action, " and ", reality_id , " current ", current_state)

        assert(action in ('hide', 'favourite', 'expire'))
        assert(isinstance(reality_id, int) and reality_id > 0)

        # Works as toggle - use inverted current_state, but only if current_state is not None
        value_to_set = not bool(int(current_state)) if current_state is not None else 1
        print(f"changed from {bool(int(current_state))} to {value_to_set}")

        if action == 'hide':
            db.set_flag_by_reality_id(reality_id, 'is_hidden', value_to_set)
        elif action == 'favourite':
            db.set_flag_by_reality_id(reality_id, 'is_favourite', value_to_set)
        elif action == 'expire':
            db.set_flag_by_reality_id(reality_id, 'is_expired', value_to_set)

        return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/')
def energy():


    return render_template('energy.html',)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
