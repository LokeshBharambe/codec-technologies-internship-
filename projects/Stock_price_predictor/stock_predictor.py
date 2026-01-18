import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


# ------------- STEP 1: DOWNLOAD STOCK DATA -------------
ticker = "AAPL"          # You can change to: TSLA, MSFT, INFY.NS, TCS.NS, etc.
data = yf.download(ticker, start="2018-01-01", end=None)

print("Data downloaded successfully!")
print(data.head())


# ------------- STEP 2: PREPARE & CREATE FEATURES -------------
data = data[['Close']]

# Moving averages (help model understand trends)
data['MA10'] = data['Close'].rolling(10).mean()
data['MA50'] = data['Close'].rolling(50).mean()

# Target → next day's price
data['Target'] = data['Close'].shift(-1)

# Remove missing rows
data = data.dropna()

X = data[['Close', 'MA10', 'MA50']]
y = data['Target']


# ------------- STEP 3: SPLIT DATA -------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)


# ------------- STEP 4: TRAIN MODEL -------------
model = LinearRegression()
model.fit(X_train, y_train)


# ------------- STEP 5: MAKE PREDICTIONS -------------
predictions = model.predict(X_test)


# ------------- STEP 6: EVALUATE MODEL -------------
mae = mean_absolute_error(y_test, predictions)

# Manual RMSE (works in ALL sklearn versions)
mse = mean_squared_error(y_test, predictions)
rmse = mse ** 0.5

print(f"\nMAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")


# ------------- STEP 7: VISUALIZE RESULTS -------------
plt.figure(figsize=(12,6))
plt.plot(y_test.values, label="Actual Price")
plt.plot(predictions, label="Predicted Price")
plt.title(f"{ticker} Stock Price Prediction (Linear Regression)")
plt.xlabel("Days")
plt.ylabel("Price")
plt.legend()
plt.show()

print("\nPrediction complete!")
# ------------- STEP 8: SAVE MODEL (OPTIONAL) -------------
import joblib   
joblib.dump(model, "stock_model.pkl")   
print("Model saved as stock_model.pkl")
