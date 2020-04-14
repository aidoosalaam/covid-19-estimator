import time, datetime
import logging
from dicttoxml import dicttoxml
from flask import Flask,request,jsonify,Response,g
from .estimator import Impact, SevereImpact

app = Flask(__name__)
#logger = logging.getLogger("estimator")
logging.basicConfig(format='%(message)s',filename='log.log',filemode='w', level=logging.DEBUG)
response = Response()




@app.before_request
def start_timer():
    g.start = time.time()



def log_request():
    now = time.time()
    duration = round(now - g.start, 2)
    log_params = {
        'method': request.method,
        'path': request.path,
        'status': str(response.status_code),
        'duration': str(int(duration))
    }
    log_msg =log_params["method"] +"\t"+ log_params["path"] +"\t" + log_params["status"] + "\t" + log_params["duration"]+"ms"
    logging.debug(log_msg)
    f=open("estimator.log","a+")
    f.write("\r\n"+log_msg)
    #f.close()

def covidEstimator(data):
    impact = Impact(data)
    severe_impact = SevereImpact(data)
    data = {
            "data" : data,
            "Impact":{
                "currentlyInfected" : impact.infectionByRequestedTime(),
                "severeCasesByRequestedTime" : impact.severeCasesByRequestedTime(),
                "hospitalBedsByRequestedTime" : impact.availableHospitalBedsByRequestedTime(),
                "casesForICUByRequestedTime" : impact.casesForICUByRequestedTime(),
                "casesForVentilatorsByRequestedTime" : impact.casesForVentilatorsByRequestedTime(),
                "dollarsInFlight" : impact.dollarsInFlight()
            },
            "SevereImpact":{
                "currentlyInfected" : severe_impact.infectionByRequestedTime(),
                "severeCasesByRequestedTime" : severe_impact.severeCasesByRequestedTime(),
                "hospitalBedsByRequestedTime" : severe_impact.availableHospitalBedsByRequestedTime(),
                "casesForICUByRequestedTime" : severe_impact.casesForICUByRequestedTime(),
                "casesForVentilatorsByRequestedTime" : severe_impact.casesForVentilatorsByRequestedTime(),
                "dollarsInFlight" : severe_impact.dollarsInFlight()
            }
    }
    return data



@app.route('/api/v1/on-covid-19/log',methods=['GET'])
def tolog():
    log_request()
    log_contents=""
    f=open("estimator.log","r")
    fr = f.readlines()
    for l in fr:
        print("l.." + l)
        log_contents = log_contents + l
    return log_contents



@app.route('/api/v1/on-covid-19',methods=['POST'])
def toJson():
    data = request.json
    data = covidEstimator(data)
    log_request()
    # convert into JSON:
    json_data = jsonify(data)
    return json_data

@app.route('/api/v1/on-covid-19/<msg_type>',methods=['POST'])
def toJsonXml(msg_type):
    data = request.json
    data = covidEstimator(data)
    log_request()
    
    if msg_type =="xml":
        xml_data = dicttoxml(data)
        return xml_data
    elif msg_type =="json":
        # convert into JSON:
        json_data = jsonify(data)
        return json_data
    else:
        # convert into JSON:
        json_data = jsonify(data)
        return json_data

