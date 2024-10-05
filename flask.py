from flask import Flask, jsonify, request, render_template
import requests
import pandas as pd
import joblib
from flask_cors import CORS
from model import predict_price  # Import prediction function
from wordcloud import WordCloud
import os

app = Flask(__name__)
CORS(app)

# Twitter API credentials (update with actual credentials)
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Weather API URL (Update the city dynamically if needed)
weather_api_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Coimbatore?unitGroup=metric&key=LW4AYXQP248MQAWE5RKWZQPAX&contentType=json"

# Price data API details
api_key = 'your_actual_api_key_here'
base_url = "http://data.gov.in/api/datastore/resource.json"
resource_id = "9ef84268-d588-465a-a308-a864a43d0070"
filter_vegetables = ['Tomato', 'Potato', 'Onion', 'Carrot', 'Spinach']
filter_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_weather_data', methods=['GET'])
def get_weather_data():
    response = requests.get(weather_api_url)
    if response.status_code == 200:
        weather_data = response.json()
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Could not retrieve weather data'})

@app.route('/get_twitter_data', methods=['GET'])
def get_twitter_data():
    query = request.args.get('query')
    
    # Mocking tweet data for the example
    tweets = ['Example tweet about price trends', 'Another tweet on vegetable prices']
    
    tweet_texts = ' '.join(tweets)
    wc = WordCloud(width=800, height=400).generate(tweet_texts)
    wc.to_file('static/images/wordcloud.png')  # Save word cloud image
    return jsonify({'wordcloud_url': '/static/images/wordcloud.png'})

@app.route('/get_price_prediction', methods=['POST'])
def get_price_prediction():
    user_input = request.json['input']
    vegetable = user_input['vegetable']
    city = user_input['city']
    
    # Predict price using the model
    predicted_price = predict_price(vegetable, city)
    
    # Mock historical price data or generate trend data from the model
    price_trend = {
        'dates': ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05'],
        'prices': [100, 110, 115, 120, predicted_price]  # Example price trend with prediction
    }
    
    # Mock logic for estimating days for price change
    twitter_factor = get_twitter_sentiment_change_days(vegetable)
    weather_factor = get_weather_change_days(city)
    news_factor = get_news_impact_days(vegetable)
    
    days_to_change = max(twitter_factor, weather_factor, news_factor)  # Placeholder logic
    
    return jsonify({'predicted_price': predicted_price, 'days_to_change': days_to_change, 'price_trend': price_trend})

# Functions to determine how long the price will take to change (mock logic)
def get_twitter_sentiment_change_days(vegetable):
    return 3  # Placeholder value

def get_weather_change_days(city):
    return 2  # Placeholder value

def get_news_impact_days(vegetable):
    return 5  # Placeholder value

@app.route('/get_vegetable_prices', methods=['GET'])
def get_vegetable_prices():
    response = requests.get(f"{base_url}?resource_id={resource_id}&api-key={api_key}")
    if response.status_code == 200:
        data = response.json()
        filtered_data = [entry for entry in data['records'] if entry['Item_Name'] in filter_vegetables and entry['City'] in filter_cities]
        return jsonify(filtered_data)
    else:
        return jsonify({'error': 'Could not retrieve vegetable price data'})

if __name__ == '__main__':
    app.run(debug=True)
