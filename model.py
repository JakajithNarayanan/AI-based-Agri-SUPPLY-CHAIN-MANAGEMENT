import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Path to your dataset
file_path = r"E:\ML projects\GOAT MAH\Vegetable and Fruits Prices in India.csv"

def train_model():
    # Load and prepare data
    data = pd.read_csv(file_path)
    X = data[['Item_Name', 'City']]  # Features
    y = data['Price']  # Target
    
    # Convert categorical data to numeric using one-hot encoding
    X = pd.get_dummies(X, drop_first=True)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model training with RandomForest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(model, 'price_predictor_model.pkl')

def predict_price(vegetable, city):
    model = joblib.load('price_predictor_model.pkl')
    
    # Prepare the input
    input_data = pd.DataFrame([[vegetable, city]], columns=['Item_Name', 'City'])
    
    # One-hot encode the input data
    input_data = pd.get_dummies(input_data, drop_first=True)

    # Align the input data with the model's expected input (training set features)
    model_columns = pd.read_csv(file_path).drop('Price', axis=1).columns.tolist()
    missing_cols = set(model_columns) - set(input_data.columns)
    for col in missing_cols:
        input_data[col] = 0  # Add missing columns with zero values
    input_data = input_data[model_columns]  # Reorder the columns

    # Make prediction
    predicted_price = model.predict(input_data)
    
    return predicted_price[0]

# Uncomment to train the model initially
# train_model()
