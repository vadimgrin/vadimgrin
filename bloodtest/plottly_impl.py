from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


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


_file_path = "\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx"
_data = Data(_file_path, 'Vadim')
app = Dash(__name__)


app.layout = html.Div([
    html.H1('Blood Test Results'),   # <== Row1 of Div1
    html.Div([html.Div([html.Div([dcc.RadioItems(_data.labels, _data.labels[0], id='id_metric', labelStyle={'display': 'block'})], style={ 'display': 'inline-block', 'height': '810px', 'overflow-y': 'scroll'}),
                        html.Div([html.H1(id='id_title'),
                                  dcc.Graph(id='id_graph'),
                                  html.Table([html.Thead(html.Tr([html.Th('A'),html.Th('B'),html.Th('C')])),html.Tbody([html.Tr([html.Td(1),html.Td(2),html.Td(3)])])])
                                 ], style={'display': 'inline-block','vertical-align': 'top','width': '50vw'}),
                ],style={'display': 'flex', 'flexDirection': 'row'})
], style={'display': 'flex', 'flexDirection': 'column'})])


def getFigure(df, mode='px'):
    if mode == 'px':
        return px.line(df, y=['Value', 'High Bound', 'Low Bound'], markers='Value')
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['High Bound'], mode='lines', name=f'High ({df["High Bound"][0]})'))
        fig.add_trace(go.Scatter(x=df.index, y=df['Value'], mode='lines+markers+text', name='Value', text=df['Value'], textposition='top center'))
        fig.add_trace(go.Scatter(x=df.index, y=df['Low Bound'], mode='lines', name=f'Low ({df["Low Bound"][0]})'))
        return fig


@app.callback(
    Output(component_id='id_graph', component_property='figure'),
    Output(component_id='id_title', component_property='children'),
    Input(component_id='id_metric', component_property='value')
)
def update_graph(metric):
    df = _data.get_data_toplot(metric)
    fig = getFigure(df, mode='go')
    return fig, metric


if __name__ == '__main__':
    app.run(debug=True)
