from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)


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
            a['Low Bound'] = _lo
            a['High Bound'] = _hi
        return a


if __name__ == '__main__':
    d = Data("\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx", 'Vadim')
    df = d.get_data_toplot('Sodium')

    fig = px.line(df, y=['Value', 'Low Bound', 'High Bound'])

    app.layout = html.Div(children=[
        html.H1(children='Blood Test Results'),

        html.Div(children='''
            This graph shows historical results for any individual test metric
        '''),

        dcc.Graph(
            id='results',
            figure=fig
        )
    ])

    app.run_server(debug=True)
