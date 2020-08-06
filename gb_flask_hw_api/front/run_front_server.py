import urllib.request
import json
import pandas as pd
import calendar
from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import SelectField, StringField, DateField, DecimalField
from wtforms.validators import DataRequired
from datetime import date, timedelta


class ClientDataForm(FlaskForm):
    name = StringField('Short description',
                       validators=[DataRequired()])
    main_category = SelectField('Main Category',
                                validators=[DataRequired()],
                                choices=[(f, f) for f in pd.read_csv("./dicts/main_category.csv")['main_category'].values])
    category = SelectField('Category',
                           validators=[DataRequired()],
                           choices=[(f, f) for f in pd.read_csv("./dicts/category.csv")['category'].values])
    country = SelectField('Country',
                          validators=[DataRequired()],
                          choices=[(f, f) for f in pd.read_csv("./dicts/country.csv")['country'].values])
    launched = DateField('Start date',
                         validators=[DataRequired()],
                         format='%d.%m.%Y',
                         default=date.today())
    deadline = DateField('Deadline',
                         validators=[DataRequired()],
                         format='%d.%m.%Y',
                         default=(date.today() + timedelta(days=calendar.monthrange(
                             date.today().year, date.today().month)[1])))
    usd_goal_real = DecimalField('Target amount (USD)',
                                 validators=[DataRequired()],
                                 places=2)


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)


def get_prediction(name, main_category, category, country, launched, deadline, usd_goal_real):
    body = {'name': name,
            'main_category': main_category,
            'category': category,
            'country': country,
            'launched': launched,
            'deadline': deadline,
            'usd_goal_real': usd_goal_real,
            }

    myurl = "http://localhost:5000/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data['name'] = request.form.get('name')
        data['main_category'] = request.form.get('main_category')
        data['category'] = request.form.get('category')
        data['country'] = request.form.get('country')
        data['launched'] = request.form.get('launched')
        data['deadline'] = request.form.get('deadline')
        data['usd_goal_real'] = float(request.form.get('usd_goal_real'))

        try:
            response = str(get_prediction(data['name'],
                                          data['main_category'],
                                          data['category'],
                                          data['country'],
                                          data['launched'],
                                          data['deadline'],
                                          data['usd_goal_real'],
                                          ))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)