
import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import requests
import os
from datetime import datetime

# --- Simulated Real-Time Data (or API could go here) ---
def fetch_data():
    # Simulated live data for speed (replace with real API if desired)
    return {
        "Year": [2021, 2022, 2023],
        "Carbon Emissions (tons)": [120000, 115000, 118000],
        "Renewable Energy %": [32, 35, 34],
        "GDP Growth %": [2.3, 2.7, 2.1],
        "Debt Ratio %": [60, 65, 72]
    }

data = fetch_data()
df = pd.DataFrame(data)

# --- AI Logic ---
def interpret(row):
    insights = []
    if row["Carbon Emissions (tons)"] > 116000 and row["Renewable Energy %"] < 35:
        insights.append("High emissions and low renewables: invest in clean energy.")
    if row["Debt Ratio %"] > 70:
        insights.append("Debt ratio above safe threshold — consider fiscal reform.")
    if row["GDP Growth %"] < 2.5:
        insights.append("Slow GDP growth — review economic stimulus options.")
    if not insights:
        return "On track"
    return " | ".join(insights)

df["AI Insight"] = df.apply(interpret, axis=1)
df["Last Updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

# --- Dash App Setup ---
app = dash.Dash(__name__)
app.title = "Real-Time Sustainability AI Dashboard"

app.layout = html.Div([
    html.H1("Sustainability AI Dashboard", style={'textAlign': 'center'}),

    html.H2("Real-Time Indicators"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    ),

    html.H2("Visual Trends"),
    dcc.Graph(
        figure=px.line(df, x="Year", y=["Carbon Emissions (tons)", "Renewable Energy %"],
                       title="Emissions vs Renewable Energy")
    ),

    dcc.Graph(
        figure=px.bar(df, x="Year", y=["GDP Growth %", "Debt Ratio %"],
                      barmode="group", title="Economic Stability Indicators")
    )
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=True, host="0.0.0.0", port=port)
