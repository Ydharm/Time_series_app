import streamlit as st
import page_stock_analysis
import page_stock_prediction

# Set page configuration
st.set_page_config(
    page_title="Stock Trading App",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add dark theme styling
st.markdown("""
<style>
.stApp {
    background-color: #1E1E1E;
    color: white;
}
h1, h2, h3 {
    color: white;
}
.css-1d391kg {
    background-color: #1E1E1E;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Stock Analysis", "Stock Prediction"])

# Display the selected page
if page == "Home":
    st.title("Trading App")
    st.write("Welcome to the Trading App! This app allows you to analyze and predict stock market data.")

    st.markdown(
        """
        ## Features
        - **Stock Analysis**: View company information and historical stock prices.
        - **Stock Prediction**: Make simple predictions for future stock prices.
        
        ### How to use
        1. Navigate to the desired page using the sidebar.
        2. Enter a stock ticker symbol (e.g., AAPL, TSLA, AMZN).
        3. Select the date range for analysis.
        4. View the analysis or generate predictions.
        """
    )
    
    # Add sample image
    try:
        st.image("D:/Time_series_app/background.jpg", 
                caption="Stock Market Analysis",
                use_column_width=True)
    except:
        st.write("Stock market visualization")
    
elif page == "Stock Analysis":
    page_stock_analysis.app()
    
elif page == "Stock Prediction":
    page_stock_prediction.app()