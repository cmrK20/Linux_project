import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='interval-component', interval=5*60*1000, n_intervals=0),
    dcc.Graph(id='time-series-graph'),
    html.Div(id='daily-report')
])

@app.callback(
    Output('time-series-graph', 'figure'),
    Output('daily-report', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_dashboard(_):
    data = pd.read_csv('eth_price_history.csv', names=['timestamp', 'price'])
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    fig = px.line(data, x='timestamp', y='price', title='Ethereum Price Time Series')

    # Daily report calculation
    daily_data = data[data['timestamp'].dt.hour == 20].copy()
    daily_data['change'] = daily_data['price'].pct_change() * 100
    daily_data['volatility'] = daily_data['change'].rolling(window=2).std()

    # Daily report display
    report = html.Table([
        html.Tr([html.Td('Date'), html.Td('Price'), html.Td('Change (%)'), html.Td('Volatility')])
    ] + [
        html.Tr([html.Td(row['timestamp'].strftime('%Y-%m-%d')),
                 html.Td(f"{row['price']:.2f}"),
                 html.Td(f"{row['change']:.2f}"),
                 html.Td(f"{row['volatility']:.2f}")]) for _, row in daily_data.iterrows()
    ])

    return fig, report

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

