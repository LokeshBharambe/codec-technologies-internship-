import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt


st.set_page_config(page_title="Stock Price Predictor", layout="centered")
st.title("📈 Stock Price Predictor (Linear Regression)")


# -------- Sidebar --------
st.sidebar.header("Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol", 
    value="AAPL", 
    help="Example: AAPL, TSLA, MSFT, INFY.NS, TCS.NS"
)

start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2018-01-01"))


if st.sidebar.button("Predict", type="primary"):
    st.write("Downloading stock data… please wait ⏳")

    
    # ---- STEP 1: DOWNLOAD DATA ----
    st.write(f"### Downloading data for **{ticker}**...")
    data = yf.download(ticker, start=str(start_date), end=None)

    if data.empty:
        st.error("No data found. Check the stock symbol.")
    else:
        st.success("Data loaded successfully!")

        st.write("### Raw Data (Preview)")
        st.dataframe(data.head())

        # ---- STEP 2: PREPARE DATA ----
        data = data[['Close']]
        data['MA10'] = data['Close'].rolling(10).mean()
        data['MA50'] = data['Close'].rolling(50).mean()
        data['Target'] = data['Close'].shift(-1)

        data = data.dropna()

        X = data[['Close', 'MA10', 'MA50']]
        y = data['Target']

        # ---- STEP 3: SPLIT ----
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, shuffle=False
        )

        # ---- STEP 4: TRAIN ----
        model = LinearRegression()
        model.fit(X_train, y_train)

        # ---- STEP 5: PREDICT ----
        predictions = model.predict(X_test)

        # ---- STEP 6: METRICS ----
        mae = mean_absolute_error(y_test, predictions)
        mse = mean_squared_error(y_test, predictions)
        rmse = mse ** 0.5

        st.write("### 📊 Model Performance")
        st.metric("MAE", f"{mae:.4f}")
        st.metric("RMSE", f"{rmse:.4f}")

        # ---- STEP 7: PLOT ----
        st.write("### 📉 Actual vs Predicted Prices")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(y_test.values, label="Actual")
        ax.plot(predictions, label="Predicted")
        ax.set_xlabel("Days")
        ax.set_ylabel("Price")
        ax.legend()

        st.pyplot(fig)

        st.success("Prediction complete!")
else:
    st.info("💡 Enter a stock symbol and click **Predict**.")
