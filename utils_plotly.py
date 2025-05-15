import plotly.graph_objects as go
import pandas as pd

def plotly_table(df, ticker):
    """
    Function to create a Plotly table from a DataFrame.
    """
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            fill_color='#4DA8DA',  # Blue header
            align='left',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color='#2E2E2E',  # Dark background
            align='left',
            font=dict(color='white', size=12)
        )
    )])
    
    fig.update_layout(
        title=f"Data for {ticker}",
        title_font_color='white',
        paper_bgcolor='#1E1E1E',  # Match Streamlit dark background
        height=300
    )
    
    return fig

def create_price_chart(data, ticker):
    """
    Function to create a line chart for stock prices.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#4DA8DA', width=2)  # Blue line
    ))
    
    fig.update_layout(
        title=f'{ticker} Stock Price',
        title_font_color='white',
        xaxis_title='Date',
        xaxis_title_font_color='white',
        yaxis_title='Price ($)',
        yaxis_title_font_color='white',
        paper_bgcolor='#1E1E1E',  # Match Streamlit dark background
        plot_bgcolor='#2E2E2E',  # Slightly lighter for contrast
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
        height=500
    )
    
    return fig

def create_volume_chart(data, ticker):
    """
    Function to create a volume chart
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=data['Date'],
        y=data['Volume'],
        name='Volume',
        marker_color='rgba(77, 168, 218, 0.5)'  # Semi-transparent blue
    ))
    
    fig.update_layout(
        title=f'{ticker} Trading Volume',
        title_font_color='white',
        xaxis_title='Date',
        xaxis_title_font_color='white',
        yaxis_title='Volume',
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
        height=300
    )
    
    return fig

def create_candlestick_chart(data, ticker):
    """
    Function to create a candlestick chart
    """
    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        increasing_line_color='#26A69A',  # Green for increasing
        decreasing_line_color='#EF5350'   # Red for decreasing
    )])
    
    fig.update_layout(
        title=f'{ticker} Stock Price',
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
        xaxis_rangeslider_visible=False,
        height=500
    )
    
    return fig