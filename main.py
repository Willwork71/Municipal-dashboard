
import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px
import os

# Sample economic data
budget_data = {
    "Sector": ["Education", "Healthcare", "Infrastructure", "Public Safety", "Welfare"],
    "Allocation (in Millions)": [150, 120, 200, 90, 80]
}

revenue_expense_data = {
    "Year": [2021, 2022, 2023],
    "Revenue": [600, 650, 700],
    "Expenses": [580, 660, 690]
}

economic_indicators = {
    "Indicator": ["Unemployment Rate", "Inflation Rate", "GDP Growth", "Debt Ratio"],
    "Value": ["4.2%", "3.1%", "2.5%", "62%"]
}

# Sustainability data
sustainability_data = {
    "Year": [2021, 2022, 2023],
    "Carbon Emissions (tons)": [120000, 115000, 110000],
    "Renewable Energy %": [32, 35, 40],
    "Waste Recycled %": [60, 63, 65]
}

# Convert to DataFrames
df_budget = pd.DataFrame(budget_data)
df_revenue_expense = pd.DataFrame(revenue_expense_data)
df_indicators = pd.DataFrame(economic_indicators)
df_sust = pd.DataFrame(sustainability_data)

# Simple rule-based AI for sustainability insights
def analyze_sustainability(row):
    if row["Renewable Energy %"] >= 40 and row["Carbon Emissions (tons)"] < 115000:
        return "On track"
    elif row["Renewable Energy %"] < 30:
        return "Needs improvement"
    else:
        return "Moderate progress"

df_sust["AI Insight"] = df_sust.apply(analyze_sustainability, axis=1)

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Municipal Economic Dashboard with Sustainability AI"

# Layout
app.layout = html.Div([
    html.H1("Municipal Economic Dashboard", style={'textAlign': 'center'}),

    html.H2("Annual Revenue vs Expenses"),
    dcc.Graph(
        figure=px.bar(df_revenue_expense, x="Year", y=["Revenue", "Expenses"], barmode='group',
                      title="Revenue and Expenses Over Years")
    ),

    html.H2("Budget Allocation by Sector"),
    dcc.Graph(
        figure=px.pie(df_budget, values="Allocation (in Millions)", names="Sector",
                      title="Budget Allocation by Sector")
    ),

    html.H2("Key Economic Indicators"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_indicators.columns],
        data=df_indicators.to_dict('records'),
        style_table={'width': '50%'},
        style_cell={'textAlign': 'left'}
    ),

    html.H2("Sustainability Trends"),
    dcc.Graph(
        figure=px.line(df_sust, x="Year", y=["Carbon Emissions (tons)", "Renewable Energy %"],
                       title="Carbon Emissions and Renewable Energy Trends")
    ),

    html.H2("Sustainability AI Insights"),
    dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_sust.columns],
        data=df_sust.to_dict("records"),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    )
])

# Run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(debug=True, host='0.0.0.0', port=port)
