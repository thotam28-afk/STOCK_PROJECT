# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ------------------------
# Paths to data
# ------------------------
DATA_DIR = Path(__file__).parent.parent / "DATA"

AGG1_FILE = DATA_DIR / "agg1.parquet"
AGG2_FILE = DATA_DIR / "agg2.parquet"
AGG3_FILE = DATA_DIR / "agg3.parquet"

# ------------------------
# Load data
# ------------------------
@st.cache_data
def load_data(file_path):
    return pd.read_parquet(file_path)

agg1 = load_data(AGG1_FILE)
agg2 = load_data(AGG2_FILE)
agg3 = load_data(AGG3_FILE)

# ------------------------
# Streamlit App
# ------------------------
st.title("Stock Market Dashboard")

st.sidebar.header("Visualizations")

option = st.sidebar.selectbox(
    "Choose a view:",
    ["Daily Average Close Price by Ticker", "Average Volume by Sector", "Daily Returns by Ticker"]
)

# ------------------------
# 1️⃣ Daily Average Close Price by Ticker
# ------------------------
if option == "Daily Average Close Price by Ticker":
    tickers = agg1['ticker'].unique()
    selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)
    df_plot = agg1[agg1['ticker'] == selected_ticker]

    fig = px.line(
        df_plot,
        x="trade_date",
        y="close_price",
        title=f"Daily Average Close Price: {selected_ticker}",
        labels={"trade_date": "Date", "close_price": "Avg Close Price"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# 2️⃣ Average Volume by Sector
# ------------------------
elif option == "Average Volume by Sector":
    fig = px.bar(
        agg2,
        x="sector",
        y="volume",
        title="Average Volume by Sector",
        labels={"volume": "Average Volume", "sector": "Sector"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ------------------------
# 3️⃣ Daily Returns by Ticker
# ------------------------
elif option == "Daily Returns by Ticker":
    tickers = agg3['ticker'].unique()
    selected_ticker = st.sidebar.selectbox("Select Ticker", tickers)
    df_plot = agg3[agg3['ticker'] == selected_ticker]

    fig = px.line(
        df_plot,
        x="trade_date",
        y="daily_return",
        title=f"Daily Returns: {selected_ticker}",
        labels={"trade_date": "Date", "daily_return": "Daily Return"}
    )
    st.plotly_chart(fig, use_container_width=True)
