from flask import Flask, escape, request, make_response
from flask_cors import CORS
import json
import requests

from LuChenProject import workflow

from hidden_link_calculate import constructR
from hidden_link_calculate import matchingPersuit
from hidden_link_calculate import main

from twitter import tw
from twitter import tw_clean
from twitter import tw_tokenize

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
def jaixin():
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


            result = json.loads(main.main(json.dumps(dataForTool[0]),json.dumps(dataForTool[1])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)

        elif bodyData[0] == "parallel_r_main":

            result = json.loads(constructR.parallel_r_main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)

        elif bodyData[0] == "parallel_minimizer":

            result = json.loads(matchingPersuit.parallel_minimizer(json.dumps(dataForTool[0])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)



    elif(request.method == "GET"):
        apiInfo = {
        "name": "Hidden",
        "desc": "Hidden Link Calculate",
        "methods": [
            {
                "name": "Main",
                "parameter": ["UserInfo","DiffusionInfo"],
                "output": ["Result"]
            },
            {
                "name": "parallel_r_main",
                "parameter": ["Data"],
                "output": ["Result"]
            },
            {
                "name": "parallel_minimizer",
                "parameter": ["Data"],
                "output": ["Result"]
            }
        ]
        }
        response = make_response(json.dumps(apiInfo))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
    return response

@app.route('/matt', methods= ["GET","POST"])
def matt():
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


            result = json.loads(tw.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)

        if bodyData[0] == "Clean":


            result = json.loads(tw_clean.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
            response = make_response(resultSend)

        if bodyData[0] == "Tokenize":


            result = json.loads(tw_tokenize.main(json.dumps(dataForTool[0])))
            resultDataId = requests.post("https://cache.rrworkflow.com/putData", json=result).text
            resultSend = json.dumps(["https://cache.rrworkflow.com/getData?" + resultDataId])
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