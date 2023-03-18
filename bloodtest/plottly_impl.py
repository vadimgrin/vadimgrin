from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


class Data:
    def __init__(self, location, sheet):
        self.data = pd.read_excel(location, sheet_name=sheet)
        self.data.dropna(subset=['Measure'], inplace=True)
        self.data.drop(columns=["Category"], inplace=True)
        self.data.reset_index(drop=True, inplace=True)
        self.labels = self.data['Measure']

    def get_data_toplot(self, label):
        row = self.data[self.data['Measure'] == label]
        row = row.fillna(method='ffill', axis=1)
        if not row.empty:
            _lo = row.loc[:, 'Low Boundary'].values[-1]
            _hi = row.loc[:, 'High Boundary'].values[-1]
            row.drop(columns=['Measure', 'High Boundary', 'Low Boundary'], inplace=True)
            a = row.transpose()
            a = a.rename(columns=lambda x: 'Value')
            a['Value'] = pd.to_numeric(a['Value'])
            a['High Bound'] = _hi
            a['Low Bound'] = _lo
        return a


_data = Data("\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx", 'Vadim')
app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Blood Test Results'),
    html.Div([
        html.Div([dcc.RadioItems(_data.labels, _data.labels[0], id='id_metric', labelStyle={'display': 'block'})], style={'display': 'inline-block'}),
        html.Div([
                    html.H1(id='id_title'),
                    dcc.Graph(id='id_graph')
                 ], style={'display': 'inline-block', 'vertical-align': 'top'})
    ])
])

@app.callback(
    Output(component_id='id_graph', component_property='figure'),
    Output(component_id='id_title', component_property='children'),
    Input(component_id='id_metric', component_property='value')
)
def update_graph(metric):
    df = _data.get_data_toplot(metric)
    fig = px.line(df, y=['Value', 'High Bound', 'Low Bound'], markers=[True, False, False], text='Value')
    return fig, metric


if __name__ == '__main__':
    app.run_server(debug=True)
