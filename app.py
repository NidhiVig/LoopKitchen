from flask import Flask, request, Response, render_template,jsonify, send_file
import random
from output import get_output
import requests
import os
import csv

app = Flask(__name__)

# Store the report generation status and data
report_data = {}

@app.route('/trigger_report')
def trigger_report():
    report_id = generate_report_id()
    report_data[report_id] = {'status': 'Running'}
    report = get_output.get_output()
    report_data[report_id] = {'status': 'Complete', 'data': report}
    return jsonify({'report_id': report_id})

@app.route('/get_report', methods=['GET'])
def get_report():
    # Check if the report_id exists in the report_data dictionary
    json_data = request.json
    report_id = json_data.get('report_id') 
    if report_id in report_data:
        report_status = report_data[report_id]['status']
        print(report_status)
        if report_status == 'Complete':
            current_dir = os.path.abspath(os.path.dirname(__file__))
            csv_location = os.path.join(current_dir, report_data[report_id]['data'])
            with open(csv_location, 'r') as file:
                csv_data = csv.DictReader(file)
                # Convert CSV data to a list of dictionaries
                data = [row for row in csv_data]
            # Set the appropriate MIME type for CSV
            mime_type = 'text/csv'

            # Return the CSV file as a response
            # return jsonify({'status': 'Complete', 'data':send_file(csv_location, mimetype=mime_type, as_attachment=True)})
            return jsonify({'status': 'Complete', 'data': data})
            # return send_file(report_data[report_id]['data'], as_attachment=True)
        else:
            return jsonify({'status': 'Running'})
    else:
        return jsonify({'status': 'Invalid report ID'})
    

@app.route('/')
def index():
    return render_template('index.html')


def generate_report_id():
    # Generate a random report ID
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))

if __name__ == '__main__':
    app.run(debug=True)