import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.graph_objects as go
from datetime import datetime

file_path = "E:/Documents/BloodTests Vadim/Blood Tests.xlsx"
sheet_name = "Vadim"
df = pd.read_excel(file_path, sheet_name=sheet_name)
df = df[df["Measure"].notna()].reset_index(drop=True)
date_cols = [c for c in df.columns if isinstance(c, pd.Timestamp)]

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H3("Measures"),
        dcc.RadioItems(
            id="measure-picker",
            options=[{"label": m, "value": m} for m in df["Measure"]],
            value=df["Measure"].iloc[0],
            labelStyle={"display": "block"}
        )
    ], style={"width": "20%", "display": "inline-block", "verticalAlign": "top"}),

    html.Div([
        dcc.Graph(id="measure-plot"),
        dash_table.DataTable(
            id="measure-table",
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "center"}
        )
    ], style={"width": "75%", "display": "inline-block", "paddingLeft": "20px"})
])


@app.callback(
    [Output("measure-plot", "figure"),
     Output("measure-table", "data"),
     Output("measure-table", "columns")],
    Input("measure-picker", "value")
)
def update_output(selected_measure):
    row = df[df["Measure"] == selected_measure].iloc[0]

    # Get all date columns dynamically (everything after "High Boundary")
    time_cols = df.columns[df.columns.get_loc("High Boundary") + 1:]

    # Format dates as strings for display
    x_labels = [c.strftime("%Y-%m-%d") if isinstance(c, pd.Timestamp) else str(c) for c in time_cols]

    # Extract Y values
    y = row[time_cols].astype(float).tolist()   # force numeric
    low = [row["Low Boundary"]] * len(x_labels)
    high = [row["High Boundary"]] * len(x_labels)

    # --- Plot ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_labels, y=low, mode="lines", name="Low Bound"))
    fig.add_trace(go.Scatter(x=x_labels, y=high, mode="lines", name="High Bound"))
    fig.add_trace(go.Scatter(x=x_labels, y=y, mode="lines+markers", name=selected_measure))
    fig.update_layout(
        title=selected_measure,
        xaxis_title="Date",
        yaxis_title="Value",
        xaxis=dict(tickangle=-45)
    )

    # --- Table ---
    row_dict = {}
    for k, v in row.to_dict().items():
        if isinstance(k, (pd.Timestamp,datetime)):
            row_dict[k.strftime("%Y-%m-%d")] = v
        else:
            row_dict[str(k)] = v

    data = [row_dict]
    columns = [{"name": c, "id": c} for c in row_dict.keys()]

    return fig, data, columns

if __name__ == "__main__":
    app.run(debug=True)
