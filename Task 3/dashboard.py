# Step 1: Install Required Libraries
# Run this in your terminal or Colab: !pip install dash dash-bootstrap-components pandas

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from sklearn.datasets import fetch_california_housing

# Step 2: Load Dataset
data = fetch_california_housing(as_frame=True)
df = data.frame

# Rename columns for better readability
df.rename(
    columns={
        "MedInc": "Median_Income",
        "AveRooms": "Average_Rooms",
        "AveBedrms": "Average_Bedrooms",
        "AveOccup": "Average_Occupants",
        "HouseAge": "House_Age",
        "MedHouseVal": "Median_House_Value",
    },
    inplace=True,
)

# Step 3: Initialize Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Step 4: Create Dashboard Layout
app.layout = dbc.Container(
    [
        html.H1("California Housing Dashboard", style={"textAlign": "center", "marginTop": 20}),
        html.P(
            "Explore trends in the California Housing Dataset, including median house value, income, and more.",
            style={"textAlign": "center"},
        ),
        # Dropdown for X-Axis selection
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select X-Axis:"),
                        dcc.Dropdown(
                            id="x-axis-dropdown",
                            options=[
                                {"label": col, "value": col}
                                for col in [
                                    "Median_Income",
                                    "House_Age",
                                    "Average_Rooms",
                                    "Average_Bedrooms",
                                    "Average_Occupants",
                                ]
                            ],
                            value="Median_Income",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        html.Label("Select Y-Axis:"),
                        dcc.Dropdown(
                            id="y-axis-dropdown",
                            options=[
                                {"label": "Median House Value", "value": "Median_House_Value"}
                            ],
                            value="Median_House_Value",
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
            ],
            className="mb-4",
        ),
        # Graph Component
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="scatter-plot", style={"height": "500px"}), width=12
            )
        ),
        # Histogram Component
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Select a Feature for Histogram:"),
                        dcc.Dropdown(
                            id="histogram-dropdown",
                            options=[
                                {"label": col, "value": col}
                                for col in [
                                    "Median_Income",
                                    "House_Age",
                                    "Average_Rooms",
                                    "Average_Bedrooms",
                                    "Average_Occupants",
                                    "Median_House_Value",
                                ]
                            ],
                            value="Median_Income",
                            clearable=False,
                        ),
                        dcc.Graph(id="histogram", style={"height": "500px"}),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
)

# Step 5: Callbacks for Interactivity
@app.callback(
    Output("scatter-plot", "figure"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value"),
)
def update_scatter(x_axis, y_axis):
    fig = px.scatter(
        df,
        x=x_axis,
        y=y_axis,
        color="House_Age",
        title=f"Scatter Plot: {y_axis} vs {x_axis}",
        labels={x_axis: x_axis, y_axis: y_axis},
    )
    fig.update_layout(template="plotly_dark", title_x=0.5)
    return fig


@app.callback(
    Output("histogram", "figure"),
    Input("histogram-dropdown", "value"),
)
def update_histogram(feature):
    fig = px.histogram(
        df,
        x=feature,
        nbins=30,
        title=f"Histogram of {feature}",
        labels={feature: feature},
    )
    fig.update_layout(template="plotly_dark", title_x=0.5)
    return fig


# Step 6: Run the Dash App
if __name__ == "__main__":
    app.run_server(debug=True)
