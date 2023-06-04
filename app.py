from flask import Flask, render_template,jsonify
import create.create_store_status as create_store_status
import math
import output.get_output

app = Flask(__name__)
# Store the report generation status and data
report_data = {}

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    # Trigger report generation
    report_id = generate_report_id()
    report_data[report_id] = {'status': 'Running'}
    
    # Perform the actual report generation task here
    # Fetch data from the database and generate the report
    report = output.get_output()
    
    # Save the report data
    report_data[report_id] = {'status': 'Complete', 'data': report}
    
    return jsonify({'status': 'success', 'report_id': report_id})

@app.route('/get_report/<report_id>', methods=['GET'])
def get_report(report_id):
    # Check if the report_id exists in the report_data dictionary
    if report_id in report_data:
        report_status = report_data[report_id]['status']
        if report_status == 'Running':
            return jsonify({'status': 'Running'})
        elif report_status == 'Complete':
            # Return the complete report data (CSV file data)
            report_data = report_data[report_id]['data']
            return jsonify({'status': 'Complete', 'data': report_data})
    else:
        return jsonify({'status': 'error', 'message': 'Report not found'}), 404

@app.route('/')
def index():
    create_store_status.create_table()
    return render_template('index.html')


def generate_report_id():
    # Generate a random report ID
    return ''.join(math.random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890', k=8))

if __name__ == '__main__':
    app.run(debug=True)