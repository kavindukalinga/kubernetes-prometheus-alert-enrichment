
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return redirect('/get-depend/source_service.source_namespace')

@app.route('/get-depend/<string:source_service>')
def get_depend(source_service):
    try:
        service_name,service_namespace=source_service.split(".")  # aero-agent-credit-service.aero-agent-stage4
        # prom_url=os.environ['prometheusUrl']
        # url=prom_url+"/api/v1/query?query=sum%28irate%28istio_requests_total%7Breporter%3D%7E%22source%22%2C+connection_security_policy%21%3D%22mutual_tls%22%2C+destination_service%3D%7E%22aero-anci-seatmap-service.aero-anci-prod.svc.cluster.local%22%2Cresponse_code%21%7E%225.*%22%2Cresponse_flags%3D%7E%22-%7Cunknown%22%2C+source_workload%3D%7E%22.*%22%2C+source_workload_namespace%3D%7E%22.*%22%7D%5B5m%5D%29%29+by+%28source_workload%2C+source_workload_namespace%29+%2F+sum%28irate%28istio_requests_total%7Breporter%3D%7E%22source%22%2C+connection_security_policy%21%3D%22mutual_tls%22%2C+destination_service%3D%7E%22aero-anci-seatmap-service.aero-anci-prod.svc.cluster.local%22%2C+source_workload%3D%7E%22.*%22%2C+source_workload_namespace%3D%7E%22.*%22%7D%5B5m%5D%29%29+by+%28source_workload%2C+source_workload_namespace%29+*100&time=1713246054.457"
        # url= f"http://172.31.2.84:30092/api/v1/query?query=sum%28istio_requests_total%7Bsource_workload%21%7E%22%28istio-ingressgateway%7Cunknown%29%22+%2C+source_workload%3D%22aero-agent-credit-service%22+%2C+source_workload_namespace%3D%22aero-agent-stage4%22%7D+%29+by+%28destination_service%29&time=1713339138.162"
        url= f"http://172.31.2.84:30092/api/v1/query?query=sum%28istio_requests_total%7Bsource_workload%21%7E%22%28istio-ingressgateway%7Cunknown%29%22+%2C+source_workload%3D%22{service_name}%22+%2C+source_workload_namespace%3D%22{service_namespace}%22%7D+%29+by+%28destination_service%29&time=1713339138.162"
        response = requests.get(url)
        responsestr=response.json()
        if response.status_code == 200:
            return jsonify(responsestr), 200
        else:
            return jsonify({"error": "Error fetching data"}), 500

        # Return JSON response
        
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
