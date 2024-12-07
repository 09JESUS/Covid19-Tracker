import requests
import pandas as pd
from flask import Flask, render_template
import matplotlib.pyplot as plt
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Function to get COVID-19 data
def get_covid_data():
    url = "https://disease.sh/v3/covid-19/all"
    response = requests.get(url)
    data = response.json()
    return data

# Route for the home page
@app.route('/')
def index():
    covid_data = get_covid_data()

    # Data extraction
    cases = covid_data['cases']
    deaths = covid_data['deaths']
    recovered = covid_data['recovered']
    active = covid_data['active']
    critical = covid_data['critical']

    # Prepare data for visualization
    labels = ['Total Cases', 'Total Deaths', 'Total Recovered', 'Active Cases', 'Critical Cases']
    values = [cases, deaths, recovered, active, critical]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.

    # Convert plot to PNG image and then to base64 for embedding in HTML
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()

    return render_template('index.html', img_data=img_base64)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
