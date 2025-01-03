from flask import Flask, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb+srv://revanth200319:revanth200319@cluster0.zrtypbn.mongodb.net/")
db = client["formData"]
collection = db["entries"]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    number = int(request.form['number'])
    team_lead = request.form['teamlead']
    name = request.form['name']
    date = request.form['date']
    college_visited = request.form['college_visited']
    forenoon = request.form['forenoon']
    afternoon = request.form['afternoon']

    # Insert data into MongoDB
    collection.insert_one({
        "CT-ID": number,
        "Team Lead": team_lead,
        "name": name,
        "date": date,
        "college_visited": college_visited,
        "forenoon": forenoon,
        "afternoon": afternoon
    })

    return render_template('index.html', message="Details submitted successfully.")

@app.route('/fetch_sorted_by_number', methods=['GET'])
def fetch_sorted_by_number():
    number = request.args.get('number')  # Get CT ID from query string
    
    # Ensure number is valid and numeric
    if number and number.isdigit():
        number_int = number 
        data = list(collection.find({"CT-ID": number_int}, {'_id': 0}))
        if not data:
            message = f"No data found for CT ID: {number}"
            return render_template('fetch_data.html', data=None, message=message)
    else:
        message = "Please enter a valid CT ID."
        return render_template('fetch_data.html', data=None, message=message)

    return render_template('fetch_data.html', data=data)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

