import os

from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import InputRequired, URL
from dotenv import load_dotenv
import csv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[InputRequired()])
    location = StringField('Location URL', validators=[InputRequired(), URL(message="URL not valid")])
    open_time = StringField('Open Time', validators=[InputRequired()])
    closing_time = StringField('Closing Time', validators=[InputRequired()])
    coffee_rating = SelectField('Coffee Rating',
                                choices=['✘', '☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
                                validators=[InputRequired()])
    wifi_rating = SelectField('Wifi Rating',
                                choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'],
                              validators=[InputRequired()])
    power_rating = SelectField('Power Rating',
                                choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'],
                               validators=[InputRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a') as cafe_list:
            cafe_list.write(f'\n{form.cafe.data},{form.location.data}, '
                            f'{form.open_time.data},{form.closing_time.data},{form.coffee_rating.data},'
                            f'{form.wifi_rating.data},{form.power_rating.data}')
            return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
