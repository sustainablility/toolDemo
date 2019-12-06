from flask import Flask, escape, request, make_response
from flask_cors import CORS
import json
import requests

from LuChenProject import workflow
from hidden_link_calculate import main

app = Flask(__name__)
CORS(app, resources=r'/*')

@app.route('/luchen', methods= ["GET","POST"])
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


            result = json.loads(workflow.main(json.dumps(dataForTool[0]), json.dumps(dataForTool[1])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)


    elif(request.method == "GET"):
        apiInfo = {
        "name": "Lu Chen",
        "desc": "Lu Chen's script",
        "methods": [
            {
                "name": "Main",
                "parameter": ["example","industry+list"],
                "output": ["Result"]
            }
        ]
        }
        response = make_response(json.dumps(apiInfo))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

@app.route('/jiaxin', methods= ["GET","POST"])
def hi():
    if(request.method == "POST"):
        bodyData = request.get_json()
        dataForTool = []
        for data in bodyData[1:]:
            if type(data) == str:
                dataFromApi = requests.get(data).json()
                dataForTool.append(dataFromApi)
            else:
                dataForTool.append(data)

        outputT = open("test.json","w")
        outputT.write(main.main(json.dumps(dataForTool[0]),json.dumps(dataForTool[1])))
        result = json.loads(main.main(json.dumps(dataForTool[0]),json.dumps(dataForTool[1])))
        resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
        resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
        response = make_response(resultSend)
    elif(request.method == "GET"):
        apiInfo = {
        "name": "Hidden",
        "desc": "Hidden Link Calculate",
        "methods": [
            {
                "name": "Analysis",
                "parameter": ["UserInfo","DiffusionInfo"],
                "output": ["Result"]
            }
        ]
        }
        response = make_response(json.dumps(apiInfo))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response