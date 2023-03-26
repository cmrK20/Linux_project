import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime, timedelta

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
    data['price'] = data['price'].astype(float)
    data = data.sort_values(by='timestamp')
    
    fig = px.line(data, x='timestamp', y='price', title='Ethereum Price Time Series')
    fig.update_layout(xaxis_range=[pd.Timestamp.today().strftime('%Y-%m-%d'), pd.Timestamp.today().strftime('%Y-%m-%d 23:59:59')])

    # Daily report calculation
    now = datetime.now()
    if now.hour >= 8:
        daily_data = data[data['timestamp'].dt.date == now.date()].copy()
    else:
        yesterday = now - timedelta(days=1)
        daily_data = data[data['timestamp'].dt.date == yesterday.date()].copy()
    daily_data['change'] = daily_data['price'].pct_change() * 100
    daily_data['volatility'] = daily_data['change'].rolling(window=2).std()
    daily_data['volatility'] = daily_data['volatility'].fillna(0)

    # Daily report display
    report = html.Table([
        html.Tr([html.Th('Date'), html.Th('Price'), html.Th('Change (%)'), html.Th('Volatility')])
    ] + [
        html.Tr([html.Td(daily_data['timestamp'].iloc[-1].strftime('%Y-%m-%d')),
                 html.Td(f"{daily_data['price'].iloc[-1]:.2f}"),
                 html.Td(f"{daily_data['change'].iloc[-1]:.2f}"),
                 html.Td(f"{daily_data['volatility'].iloc[-1]:.2f}")])
    ])

    return fig, report

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

