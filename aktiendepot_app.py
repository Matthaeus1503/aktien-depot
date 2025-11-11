import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Aktiendepot", layout="wide")

# --- Titel und Gesamtübersicht ---
st.title("📈 Mein Aktiendepot Dashboard")

depots = ["Aktiendepot", "Krypto-Depot", "Fonds-Depot"]
gesamtwert = 100000  # Beispielwert
veränderung_heute = 1.2  # Prozent
farbe = "green" if veränderung_heute >= 0 else "red"

st.metric("Gesamtwert", f"{gesamtwert:,.2f} €", f"{veränderung_heute:+.2f} %")

# --- Depot Auswahl ---
wahl = st.sidebar.selectbox("Depot auswählen:", depots)

# --- Beispiel-Aktienliste ---
daten = {
    "Name": ["Apple", "Microsoft", "Nvidia", "Tesla"],
    "Ticker": ["AAPL", "MSFT", "NVDA", "TSLA"],
    "Anzahl": [10, 5, 8, 6],
    "Einstiegspreis": [160, 300, 400, 200]
}
df = pd.DataFrame(daten)

# --- Live Kursdaten laden ---
for i, row in df.iterrows():
    ticker = yf.Ticker(row["Ticker"])
    kurs = ticker.history(period="1d")["Close"].iloc[-1]
    df.loc[i, "Kurs aktuell"] = kurs
    df.loc[i, "Wert (€)"] = kurs * row["Anzahl"]
    df.loc[i, "Tagesänderung (%)"] = ticker.history(period="2d")["Close"].pct_change().iloc[-1] * 100

gesamtwert = df["Wert (€)"].sum()

st.subheader(f"{wahl}")
st.dataframe(df, use_container_width=True)

# --- Liniendiagramm Tagesverlauf ---
ticker_symbol = "AAPL"
ticker_data = yf.download(ticker_symbol, period="1d", interval="15m")
farbe = "green" if ticker_data["Close"].iloc[-1] >= ticker_data["Close"].iloc[0] else "red"
fig = px.line(ticker_data, y="Close", title=f"Tagesverlauf ({ticker_symbol})", line_shape="spline")
fig.update_traces(line=dict(color=farbe))
st.plotly_chart(fig, use_container_width=True)

# --- Kuchendiagramm Beispiel ---
sektoren = {
    "Technologie": 50,
    "Automobil": 25,
    "Finanzen": 15,
    "Gesundheit": 10
}
fig2 = px.pie(names=list(sektoren.keys()), values=list(sektoren.values()), title="Sektorenanteile")
st.plotly_chart(fig2, use_container_width=True)
