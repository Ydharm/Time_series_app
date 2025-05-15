import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from utils_plotly import create_price_chart

def app():
    st.title("Stock Price Prediction")
    
    col1, col2, col3 = st.columns(3)
    today = datetime.today()
    
    with col1:
        ticker = st.text_input("Enter Stock Ticker", "TSLA")
    with col2:
        start_date = st.date_input("Start Date", today - timedelta(days=365))
    with col3:
        end_date = st.date_input("End Date", today)
    
    # Prediction method selection
    prediction_method = st.radio(
        "Select Prediction Method",
        ["Linear Regression", "Moving Average"],
        horizontal=True
    )
    
    # Prediction days slider
    prediction_days = st.slider("Prediction Days", 1, 30, 7)
    
    try:
        # Get stock data
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            st.error(f"No data found for ticker {ticker} in the selected date range.")
            return
            
        data.reset_index(inplace=True)
    except Exception as e:
        st.error(f"Error retrieving data: {str(e)}")
        return
    
    # Display historical data
    st.subheader("Historical Stock Price")
    price_chart = create_price_chart(data, ticker)
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Make prediction when button is clicked
    if st.button("Generate Prediction"):
        if prediction_method == "Linear Regression":
            with st.spinner("Generating prediction with Linear Regression..."):
                predictions = linear_regression_prediction(data, ticker, prediction_days)
                display_predictions(data, predictions, ticker)
        else:  # Moving Average
            with st.spinner("Generating prediction with Moving Average..."):
                predictions = moving_average_prediction(data, ticker, prediction_days)
                display_predictions(data, predictions, ticker)

def linear_regression_prediction(data, ticker, prediction_days):
    """
    Make a stock price prediction using linear regression
    """
    # Create a copy of the data
    df = data.copy()
    
    # Create a column for the sequence of trading days
    df['Trading_Day'] = range(len(df))
    
    # Create the input features and target variable
    X = df[['Trading_Day']]
    y = df['Close']
    
    # Create and train the model
    model = LinearRegression()
    model.fit(X, y)
    
    # Generate future dates
    last_date = df['Date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=prediction_days)
    
    # Create future trading days
    future_days = range(len(df), len(df) + prediction_days)
    
    # Predict future prices
    future_prices = model.predict(np.array(future_days).reshape(-1, 1))
    
    # Create a DataFrame for the predictions
    predictions = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Close': future_prices
    })
    
    return predictions

def moving_average_prediction(data, ticker, prediction_days):
    """
    Make stock price predictions using moving average
    """
    # Calculate the moving average (last 30 days or all data if less)
    window_size = min(30, len(data))
    avg_price = data['Close'].tail(window_size).mean()
    
    # Generate future dates
    last_date = data['Date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=prediction_days)
    
    # Create a DataFrame with the same price repeated
    predictions = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Close': [avg_price] * prediction_days
    })
    
    return predictions

def display_predictions(data, predictions, ticker):
    """
    Display the prediction results
    """
    # Display predictions table
    st.subheader("Price Predictions")
    
    # Format the date and price columns
    display_predictions = predictions.copy()
    display_predictions['Date'] = display_predictions['Date'].dt.date
    display_predictions['Predicted_Close'] = display_predictions['Predicted_Close'].round(2)
    
    st.write(display_predictions)
    
    # Plot predictions with historical data
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='Historical Prices',
        line=dict(color='#4DA8DA')
    ))
    
    # Add predictions
    fig.add_trace(go.Scatter(
        x=predictions['Date'],
        y=predictions['Predicted_Close'],
        mode='lines+markers',
        name='Predicted Prices',
        line=dict(color='#EF5350')
    ))
    
    # Add a vertical line at the last historical date
    fig.add_vline(
        x=data['Date'].iloc[-1], 
        line_dash="dash", 
        line_color="gray", 
        annotation_text="Prediction Start", 
        annotation_position="top right"
    )
    
    fig.update_layout(
        title=f'{ticker} Stock Price Prediction',
        title_font_color='white',
        xaxis_title='Date',
        xaxis_title_font_color='white',
        yaxis_title='Price ($)',
        yaxis_title_font_color='white',
        paper_bgcolor='#1E1E1E',
        plot_bgcolor='#2E2E2E',
        xaxis=dict(
            showgrid=True,
            gridcolor='#444444',
            tickfont=dict(color='white')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#444444',
            tickfont=dict(color='white')
        ),
        height=500,
        legend=dict(font=dict(color='white'))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show prediction summary
    st.subheader("Prediction Summary")
    
    last_price = data['Close'].iloc[-1]
    predicted_end_price = predictions['Predicted_Close'].iloc[-1]
    price_change = predicted_end_price - last_price
    price_change_percent = (price_change / last_price) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Last Close Price", f"${last_price:.2f}")
    col2.metric("Predicted End Price", f"${predicted_end_price:.2f}")
    col3.metric("Predicted Change", f"{price_change_percent:.2f}%")
    
    # Disclaimer
    st.info("Disclaimer: This is a simple prediction based on historical data and should not be used for actual investment decisions.")