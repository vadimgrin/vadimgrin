from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import random

class Data:
    def __init__(self, location, sheet):
        self.data = pd.read_excel(location, sheet_name=sheet)
        self.data.dropna(subset=['Measure'], inplace=True)
        self.data.drop(columns=["Category"], inplace=True)
        self.data.reset_index(drop=True, inplace=True)
        self.labels = self.data['Measure']

    def get_data_toplot(self, label):
        row = self.data[self.data['Measure'] == label]
        # row = row.fillna(method='ffill', axis=1)
        row = row.ffill(axis=1)
        if not row.empty:
            a = row.transpose()
            a = a.rename(columns=lambda x: 'Value')
            a['Measure'] = a['Value']['Measure']
            a['High Bound'] = a['Value']['High Boundary']
            a['Low Bound'] = a['Value']['Low Boundary']
            a.drop(['Measure', 'High Boundary', 'Low Boundary'], inplace=True)
            a = a.astype({'Measure': 'string'})
            a['Value'] = pd.to_numeric(a['Value'])
            a = a.reset_index().rename(columns={'index': 'Sample Date'})
            a['Sample Date'].astype('datetime64[ns]')
        return a[['Sample Date', 'Measure', 'Value', 'Low Bound', 'High Bound']]

    def dash_table(self, df):
        mytable = dash_table.DataTable(
            id='id_table1',
            columns=[{"name": i, "id": i, 'type': 'numeric', 'format': {'specifier': ',.1f'}} if i not in [
                'Measure'] else {"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            style_as_list_view=True,
            style_cell={'padding': '2px'},
            page_action='none',
            style_table={'height': '600px', 'overflowY': 'auto'},
            style_cell_conditional=[
                {
                    'if': {'column_id': 'Sample Date'},
                    'textAlign': 'left', 'width': '50px',
                },
            ],
            style_data_conditional=[
                {
                    'if': {'row_index': 0},
                    'backgroundColor': '#FFF2CC',
                },
            ],
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold',
                'textAlign': 'center'
            },
        )
        return mytable


_file_path = "\\\MYBOOKLIVE\\Public\\Vadim Documents\\BloodTests Vadim\\Blood Test Results.xlsx"
_data = Data(_file_path, 'Vadim')
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Blood Test Results'),
    html.Div([html.Div([html.Div(
        [dcc.RadioItems(_data.labels, _data.labels[0], id='id_metric', labelStyle={'display': 'block'})],
        style={'display': 'inline-block', 'height': '60vw', 'overflow-y': 'scroll'}),
                        html.Div([html.H1(id='id_title'),
                                  dcc.Graph(id='id_graph'),
                                  _data.dash_table(_data.get_data_toplot(_data.labels[0])),
                                  ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '50vw'}),
                        ], style={'display': 'flex', 'flexDirection': 'row'})
              ], style={'display': 'flex', 'flexDirection': 'column'})])


def getFigure(df, mode='px'):
    if mode == 'px':
        return px.line(df, y=['Value', 'High Bound', 'Low Bound'], markers='Value')
    else:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['High Bound'], mode='lines', name=f'High ({df["High Bound"][0]})'))
        fig.add_trace(go.Scatter(x=df.index, y=df['Value'], mode='lines+markers+text', name='Value', text=df['Value'],
                                 textposition='top center'))
        fig.add_trace(go.Scatter(x=df.index, y=df['Low Bound'], mode='lines', name=f'Low ({df["Low Bound"][0]})'))
        return fig


@app.callback(
    Output(component_id='id_graph', component_property='figure'),
    Output(component_id='id_title', component_property='children'),
    Output(component_id='id_table1', component_property='data'),
    Input(component_id='id_metric', component_property='value')
)
def update_graph(metric):
    df = _data.get_data_toplot(metric)
    fig = getFigure(df, mode='go')
    dt = df.to_dict(orient='records')
    return fig, metric, dt


if __name__ == '__main__':
    app.run(debug=True)
