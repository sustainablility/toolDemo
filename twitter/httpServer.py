from flask import Flask, escape, request, make_response
from flask_cors import CORS
import json
import requests
import main
import main_clean
import main_tokenize

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/', methods= ["GET","POST"])
def hello():
    if(request.method == "POST"):


        bodyData = request.get_json()
        dataForTool = []
        for data in bodyData[1:]:
            if type(data) == str:
                dataFromApi = requests.get(data).json()
                dataForTool.append(dataFromApi)
            else:
                dataForTool.append(data)

        if bodyData[0] == "Main":


            result = json.loads(main.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("http://127.0.0.1:2223/putData", json=result).text
            resultSend = json.dumps(["http://127.0.0.1:2223/getData?" + resultDataId])
            response = make_response(resultSend)

        if bodyData[0] == "Clean":


            result = json.loads(main_clean.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("http://127.0.0.1:2223/putData", json=result).text
            resultSend = json.dumps(["http://127.0.0.1:2223/getData?" + resultDataId])
            response = make_response(resultSend)

        if bodyData[0] == "Tokenize":


            result = json.loads(main_tokenize.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("http://127.0.0.1:2223/putData", json=result).text
            resultSend = json.dumps(["http://127.0.0.1:2223/getData?" + resultDataId])
            response = make_response(resultSend)


    elif(request.method == "GET"):
        apiInfo = {
        "name": "Twitter analysis",
        "desc": "Twitter-sentiment-analysis",
        "methods": [
            {
                "name": "Main",
                "parameter": ["token"],
                "output": ["Result"]
            },
            {
                "name": "Clean",
                "parameter": ["data"],
                "output": ["Cleaned"]
            },
            {
                "name": "Tokenize",
                "parameter": ["Cleaned"],
                "output": ["Tokenout"]
            }
        ]
        }
        response = make_response(json.dumps(apiInfo))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response
