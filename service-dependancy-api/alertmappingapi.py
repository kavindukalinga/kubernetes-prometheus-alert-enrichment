from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import alertmappingmain
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return redirect('/get-depend/enter-service-name')

@app.route('/get-depend/<string:source_service>')
def get_depend(source_service):
    try:
        # Attempt to get dependent services
        dependendt_service = alertmappingmain.main(parameter=source_service)
        
        # Convert set to list
        destinations_list = list(dependendt_service)

        # Serialize list to JSON
        # destinations_json = json.dumps(destinations_list)

        # Return JSON response
        return jsonify({"source_service": source_service,
                        "dependent_service": destinations_list}), 200
    except Exception as e:
        # Handle exceptions
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
