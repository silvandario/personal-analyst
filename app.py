import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta  # Technical Analysis library
from datetime import datetime, timedelta

# Function to fetch stock data with extra buffer for lagging indicators
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df.index = df.index.tz_localize(None)
    return df

# Function to calculate technical indicators
def calculate_indicators(df, indicators):
    if 'SMA' in indicators:
        df['SMA'] = ta.trend.sma_indicator(df['Close'], window=20)
    if 'EMA' in indicators:
        df['EMA'] = ta.trend.ema_indicator(df['Close'], window=20)
    if 'RSI' in indicators:
        df['RSI'] = ta.momentum.rsi(df['Close'], window=14)
    if 'Bollinger Bands' in indicators:
        df['Bollinger_High'], df['Bollinger_Low'] = ta.volatility.bollinger_hband(df['Close']), ta.volatility.bollinger_lband(df['Close'])
    if 'MACD' in indicators:
        df['MACD'] = ta.trend.macd(df['Close'])
        df['MACD_Signal'] = ta.trend.macd_signal(df['Close'])
    if 'ADX' in indicators:
        df['ADX'] = ta.trend.adx(df['High'], df['Low'], df['Close'])
    if 'Stochastic Oscillator' in indicators:
        df['Stochastic_K'], df['Stochastic_D'] = ta.momentum.stoch(df['High'], df['Low'], df['Close'])
    if 'ATR' in indicators:
        df['ATR'] = ta.volatility.average_true_range(df['High'], df['Low'], df['Close'])
    if 'OBV' in indicators:
        df['OBV'] = ta.volume.on_balance_volume(df['Close'], df['Volume'])
    return df

# Streamlit UI
st.title("Stock Comparison and Technical Indicators")

# User inputs
tickers_input = st.text_input("Enter stock tickers separated by commas (e.g., AAPL, GOOGL, MSFT)")
indicators = st.multiselect("Select technical indicators", options=['SMA', 'EMA', 'RSI', 'Bollinger Bands', 'MACD', 'ADX', 'ATR', 'OBV'])

if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
    combined_df = pd.DataFrame()
    start_date = st.date_input("Select start date", value=datetime.now() - timedelta(days=365))
    end_date = st.date_input("Select end date", value=datetime.now())
    start_date = pd.Timestamp(start_date).tz_localize(None)
    end_date = pd.Timestamp(end_date).tz_localize(None)

    for ticker in tickers:
        df = get_stock_data(ticker, start_date, end_date)
        df = calculate_indicators(df, indicators)
        df['Ticker'] = ticker  # Add ticker column for identification
        combined_df = pd.concat([combined_df, df])

    # Plotting the stock prices
    fig = go.Figure()
    for ticker in tickers:
        df = combined_df[combined_df['Ticker'] == ticker]
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=f'{ticker} Close Price'))
    fig.update_layout(title="Close Prices",
                      xaxis_title="Date",
                      yaxis_title="Price",
                      legend_title="Legend")
    st.plotly_chart(fig)

    # Checkboxes for individual plots
    individual_plots = st.checkbox("Show individual plots for each time span and stock")

    # Plotting each technical indicator separately
    if 'SMA' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines', name=f'{ticker} SMA'))
                fig.update_layout(title=f"{ticker} Simple Moving Average (SMA)",
                                  xaxis_title="Date",
                                  yaxis_title="SMA",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA'], mode='lines', name=f'{ticker} SMA'))
            fig.update_layout(title="Simple Moving Average (SMA)",
                              xaxis_title="Date",
                              yaxis_title="SMA",
                              legend_title="Legend")
            st.plotly_chart(fig)
    
    if 'EMA' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name=f'{ticker} EMA'))
                fig.update_layout(title=f"{ticker} Exponential Moving Average (EMA)",
                                  xaxis_title="Date",
                                  yaxis_title="EMA",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['EMA'], mode='lines', name=f'{ticker} EMA'))
            fig.update_layout(title="Exponential Moving Average (EMA)",
                              xaxis_title="Date",
                              yaxis_title="EMA",
                              legend_title="Legend")
            st.plotly_chart(fig)
    
    if 'RSI' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name=f'{ticker} RSI'))
                fig.update_layout(title=f"{ticker} Relative Strength Index (RSI)",
                                  xaxis_title="Date",
                                  yaxis_title="RSI",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], mode='lines', name=f'{ticker} RSI'))
            fig.update_layout(title="Relative Strength Index (RSI)",
                              xaxis_title="Date",
                              yaxis_title="RSI",
                              legend_title="Legend")
            st.plotly_chart(fig)
    
    if 'Bollinger Bands' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_High'], mode='lines', name=f'{ticker} Bollinger High'))
                fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_Low'], mode='lines', name=f'{ticker} Bollinger Low'))
                fig.update_layout(title=f"{ticker} Bollinger Bands",
                                  xaxis_title="Date",
                                  yaxis_title="Bollinger Bands",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_High'], mode='lines', name=f'{ticker} Bollinger High'))
                fig.add_trace(go.Scatter(x=df.index, y=df['Bollinger_Low'], mode='lines', name=f'{ticker} Bollinger Low'))
            fig.update_layout(title="Bollinger Bands",
                              xaxis_title="Date",
                              yaxis_title="Bollinger Bands",
                              legend_title="Legend")
            st.plotly_chart(fig)
    
    if 'MACD' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name=f'{ticker} MACD'))
                fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name=f'{ticker} MACD Signal'))
                fig.update_layout(title=f"{ticker} MACD",
                                  xaxis_title="Date",
                                  yaxis_title="MACD",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], mode='lines', name=f'{ticker} MACD'))
                fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], mode='lines', name=f'{ticker} MACD Signal'))
            fig.update_layout(title="MACD",
                              xaxis_title="Date",
                              yaxis_title="MACD",
                              legend_title="Legend")
            st.plotly_chart(fig)

    if 'ADX' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['ADX'], mode='lines', name=f'{ticker} ADX'))
                fig.update_layout(title=f"{ticker} Average Directional Movement Index (ADX)",
                                  xaxis_title="Date",
                                  yaxis_title="ADX",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['ADX'], mode='lines', name=f'{ticker} ADX'))
            fig.update_layout(title="Average Directional Movement Index (ADX)",
                              xaxis_title="Date",
                              yaxis_title="ADX",
                              legend_title="Legend")
            st.plotly_chart(fig)

    if 'ATR' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['ATR'], mode='lines', name=f'{ticker} ATR'))
                fig.update_layout(title=f"{ticker} Average True Range (ATR)",
                                  xaxis_title="Date",
                                  yaxis_title="ATR",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['ATR'], mode='lines', name=f'{ticker} ATR'))
            fig.update_layout(title="Average True Range (ATR)",
                              xaxis_title="Date",
                              yaxis_title="ATR",
                              legend_title="Legend")
            st.plotly_chart(fig)

    if 'OBV' in indicators:
        if individual_plots:
            for ticker in tickers:
                fig = go.Figure()
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], mode='lines', name=f'{ticker} OBV'))
                fig.update_layout(title=f"{ticker} On-Balance Volume (OBV)",
                                  xaxis_title="Date",
                                  yaxis_title="OBV",
                                  legend_title="Legend")
                st.plotly_chart(fig)
        else:
            fig = go.Figure()
            for ticker in tickers:
                df = combined_df[combined_df['Ticker'] == ticker]
                fig.add_trace(go.Scatter(x=df.index, y=df['OBV'], mode='lines', name=f'{ticker} OBV'))
            fig.update_layout(title="On-Balance Volume (OBV)",
                              xaxis_title="Date",
                              yaxis_title="OBV",
                              legend_title="Legend")
            st.plotly_chart(fig)
