from urllib import request
import urllib.request
import json


def get_prediction(name, category, main_category, deadline, launched, country, usd_goal_real):
    body = {'name': name,
            'category': category,
            'main_category': main_category,
            'deadline': deadline,
            'launched': launched,
            'country': country,
            'usd_goal_real': usd_goal_real,
            }

    myurl = "http://localhost:5000/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']


if __name__ == '__main__':
    name = 'The Songs of Adelaide & Abullah'
    category = 'Poetry'
    main_category = 'Publishing'
    deadline = '2015-10-09'
    launched = '2015-08-11'
    country = 'GB'
    usd_goal_real = 1533.95
    preds = get_prediction(name, category, main_category, deadline, launched, country, usd_goal_real)
    print(preds)
