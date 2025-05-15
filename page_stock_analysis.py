import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils_plotly import plotly_table, create_price_chart, create_volume_chart, create_candlestick_chart

def app():
    st.title("Stock Analysis")

    col1, col2, col3 = st.columns(3)
    today = datetime.today()

    with col1:
        ticker = st.text_input("Enter Stock Ticker", "TSLA")
    with col2:
        start_date = st.date_input("Start Date", today - timedelta(days=365))
    with col3:
        end_date = st.date_input("End Date", today)

    try:
        # Get stock information
        stock = yf.Ticker(ticker)
        data = yf.download(ticker, start=start_date, end=end_date)
        
        if data.empty:
            st.error(f"No data found for ticker {ticker} in the selected date range.")
            return
            
        data.reset_index(inplace=True)
    except Exception as e:
        st.error(f"Error retrieving data: {str(e)}")
        return

    # Company information
    st.subheader(f"{ticker} Information")
    
    try:
        # Company name
        company_name = stock.info.get('longName', ticker)
        st.write(f"## {company_name}")
        
        # Company details
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Sector:**", stock.info.get('sector', 'N/A'))
            st.write("**Industry:**", stock.info.get('industry', 'N/A'))
        with col2:
            st.write("**Country:**", stock.info.get('country', 'N/A'))
            st.write("**Website:**", stock.info.get('website', 'N/A'))
        
        # Business summary
        if 'longBusinessSummary' in stock.info:
            with st.expander("Business Summary"):
                st.write(stock.info['longBusinessSummary'])
    except Exception as e:
        st.warning(f"Could not retrieve complete company information: {e}")
    
    # Financial metrics
    st.subheader("Financial Metrics")
    col1, col2 = st.columns(2)
    
    try:
        with col1:
            # Format market cap for better display
            market_cap = stock.info.get('marketCap', 'N/A')
            if isinstance(market_cap, (int, float)):
                market_cap = f"${market_cap:,}"
                
            df = pd.DataFrame(index=['Market Cap', 'Beta', 'EPS', 'PE'])
            df['Value'] = [
                market_cap, 
                stock.info.get('beta', 'N/A'), 
                stock.info.get('trailingEps', 'N/A'), 
                stock.info.get('forwardPE', 'N/A')
            ]
            fig_df = plotly_table(df, ticker)
            st.plotly_chart(fig_df, use_container_width=True)
            
        with col2:
            df = pd.DataFrame(index=['52 Week High', '52 Week Low', '52 Week Change'])
            
            # Format percentage for better display
            week_change = stock.info.get('52WeekChange', 'N/A')
            if isinstance(week_change, (int, float)):
                week_change = f"{week_change * 100:.2f}%"
                
            df['Value'] = [
                stock.info.get('fiftyTwoWeekHigh', 'N/A'), 
                stock.info.get('fiftyTwoWeekLow', 'N/A'), 
                week_change
            ]
            fig_df = plotly_table(df, ticker)
            st.plotly_chart(fig_df, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not display financial metrics: {e}")
    
    # Chart type selector
    chart_type = st.radio(
        "Select Chart Type",
        ["Line Chart", "Candlestick Chart"],
        horizontal=True
    )
    
    # Display price chart based on selection
    st.subheader("Stock Price Chart")
    if chart_type == "Line Chart":
        price_chart = create_price_chart(data, ticker)
    else:
        price_chart = create_candlestick_chart(data, ticker)
    
    st.plotly_chart(price_chart, use_container_width=True)
    
    # Volume chart
    volume_chart = create_volume_chart(data, ticker)
    st.plotly_chart(volume_chart, use_container_width=True)
    
    # Key metrics
    st.subheader("Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    try:
        # Current price and daily change
        current_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
        daily_change = current_price - previous_price
        daily_change_percent = (daily_change / previous_price * 100) if previous_price > 0 else 0
        
        col1.metric(
            "Current Price", 
            f"${current_price:.2f}", 
            f"{daily_change_percent:.2f}%"
        )
        
        # Overall price change for the period
        start_price = data['Close'].iloc[0]
        overall_change = current_price - start_price
        overall_change_percent = (overall_change / start_price * 100) if start_price > 0 else 0
        
        col2.metric(
            "Period Change", 
            f"${overall_change:.2f}", 
            f"{overall_change_percent:.2f}%"
        )
        
        # Average trading volume
        avg_volume = data['Volume'].mean()
        col3.metric("Avg. Volume", f"{avg_volume:,.0f}")
    except Exception as e:
        st.warning(f"Could not calculate metrics: {e}")