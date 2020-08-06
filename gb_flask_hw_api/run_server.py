# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
import flask
import logging
import numpy as np
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)


modelpath = "./models/pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Predicting the likelihood of successful crowdfunding fundraising. Please use 'http://[address]/predict' to POST"""


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        name, category, main_category, deadline, launched, country, usd_goal_real = "", "", "", "", "", "", ""

        request_json = flask.request.get_json()

        if request_json["name"]:
            name = request_json['name']

        if request_json["category"]:
            category = request_json['category']

        if request_json["main_category"]:
            main_category = request_json['main_category']

        if request_json["deadline"]:
            deadline = request_json['deadline']

        if request_json["launched"]:
            launched = request_json['launched']

        if request_json["country"]:
            country = request_json['country']

        if request_json["usd_goal_real"]:
            usd_goal_real = request_json['usd_goal_real']

        logger.info(f'{dt} Data: name={name}, category={category}, main_category={main_category}, ' +
                    f'deadline={deadline}, launched={launched}, country={country}, usd_goal_real={usd_goal_real}')
        try:
            preds = model.predict_proba(pd.DataFrame({"name": [name],
                                                      "category": [category],
                                                      "main_category": [main_category],
                                                      "deadline": [deadline],
                                                      "launched": [launched],
                                                      "country": [country],
                                                      "usd_goal_real": [usd_goal_real],
                                                      }))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[:, 1][0]
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)
