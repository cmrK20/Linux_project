import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Event
from scrape_xrates import scrape_xrates

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H2('Live EUR/USD Exchange Rate'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000,  # update every 5 seconds
            n_intervals=0
        )
    ]
)

@app.callback(Output('live-update-text', 'children'),
              [Event('interval-component', 'interval')])
def update_rate():
    rate = scrape_xrates()
    if rate:
        return 'The current EUR/USD exchange rate is: {}'.format(rate)
    else:
        return 'Unable to retrieve exchange rate data'

@app.callback(Output('live-update-graph', 'figure'),
              [Event('interval-component', 'interval')])
def update_graph():
    df = pd.DataFrame({'time': [pd.Timestamp.now()], 'rate': [scrape_xrates()]})
    trace = go.Scatter(
        x=df['time'],
        y=df['rate'],
        name='EUR/USD Exchange Rate'
    )
    layout = go.Layout(
        title='Live EUR/USD Exchange Rate',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Exchange Rate')
    )
    return {'data': [trace], 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)

