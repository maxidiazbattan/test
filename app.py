#Importing the libraries.
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output

import pandas as pd



def data_load():
    df_btc = dft.geckoHistorical('bitcoin').reset_index()[['date','price']]
    df_eth = dft.geckoHistorical('ethereum').reset_index()[['date','price']]
    df_bnb = dft.geckoHistorical('binancecoin').reset_index()[['date','price']]

    df_btc = df_btc[df_btc['date'] > '2022-01-01']
    df_eth = df_eth[df_eth['date'] > '2022-01-01']
    df_bnb = df_bnb[df_bnb['date'] > '2022-01-01']

    return df_btc, df_eth, df_bnb


df = pd.read_csv('datasets/cards_tickers.csv', header=0, index_col=0)
df = df.reset_index()


assets={'BTC-USD':'BTC-USD','ETH-USD':'ETH-USD','BNB-USD':'BNB-USD'}
periods={'1mo':'1mo','3mo':'3mo','6mo':'6mo','1y':'1y'}


app =  dash.Dash(__name__,external_stylesheets = [dbc.themes.BOOTSTRAP],
                          #meta_tags=[{'name': 'viewport',
                          #            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = app.server

app.layout = dbc.Container([
    
   dbc.Row([
             dbc.Col([
                      dbc.Card([
                                dbc.CardBody([html.H3("Crypto Dashboard 📈", className='header header-title text-center text-white') ]),
                                ], style={'borderRadius': '10px'}, className='title-card'),], width={'size':4, 'offset':0}),

            dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                        html.H5("Choose an asset", className='header-title text-center text-white'),
                      dcc.Dropdown(id="assets-dropdown",
                         options=[{"label": j, "value": i} for i, j in assets.items()],
                         value="BTC-USD", 
                         clearable=False,
                         style= {'borderRadius': '10px'}, className="m-1",
                        ),
                     ]),], style={'borderRadius': '10px'}, className='dropdown-card main-navigation'),], width={'size':4, 'offset':0}),
    
             dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                        html.H5("Choose a period", className='header-title text-center text-white'),
                      dcc.Dropdown(id="period-dropdown",
                         options=[{"label": j, "value": i} for i, j in periods.items()],
                         value="1mo", 
                         clearable=False,
                         style= {'borderRadius': '10px'}, className="m-1",
                        ),
                     ]),], style={'borderRadius': '10px'}, className='dropdown-card'),], width={'size':4, 'offset':0}),
        ], ),



    dbc.Row([
            dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                                              dbc.Row([
                                                       dbc.Col([dbc.CardImg(src="/assets/bitcoin.png",
                                                                            top=True,
                                                                            style={"width": 50, 'height': 50},)
                                                               ]),

                                                        dbc.Col([html.P("CHANGE (1m)", className="mt-3 ml-1")]),

                                                        dbc.Col([dcc.Graph(id='indicator-graph-1', figure={},
                                                                           config={'displayModeBar':False}, className="mt-2")
                                                            ]),
                                                     ], justify='center'),

                                              dbc.Row([
                                                       dbc.Col([dcc.Graph(id='daily-line-1', figure={},
                                                                          config={'displayModeBar':False})
                                                       ], width=12)
                                                      ]),
                                             ]),
                           
                               ], style={'borderRadius': '10px'}, className="indicators-card mt-1")
                        ], width={'size':4, 'offset':0}),

            dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                                              dbc.Row([
                                                       dbc.Col([dbc.CardImg(src="/assets/ethereum.png",
                                                                            top=True,
                                                                            style={"width": 50, 'height': 50},)
                                                               ]),

                                                        dbc.Col([html.P("CHANGE (1m)", className="mt-3 ml-1")]),

                                                        dbc.Col([dcc.Graph(id='indicator-graph-2', figure={},
                                                                           config={'displayModeBar':False}, className="mt-2")
                                                            ]),
                                                     ], justify='center'),

                                              dbc.Row([
                                                       dbc.Col([dcc.Graph(id='daily-line-2', figure={},
                                                                          config={'displayModeBar':False})
                                                       ], width=12)
                                                      ]),
                                             ]),
                           
                               ], style={'borderRadius': '10px'}, className="indicators-card mt-1")
                        ], width={'size':4, 'offset':0}),
             

             dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                                              dbc.Row([
                                                       dbc.Col([dbc.CardImg(src="/assets/bnb.png",
                                                                            top=True,
                                                                            style={"width": 50, 'height': 50},)
                                                               ]),

                                                        dbc.Col([html.P("CHANGE (1m)", className="mt-3 ml-1")]),

                                                        dbc.Col([dcc.Graph(id='indicator-graph-3', figure={},
                                                                           config={'displayModeBar':False}, className="mt-2")
                                                            ]),
                                                     ], justify='center'),

                                              dbc.Row([
                                                       dbc.Col([dcc.Graph(id='daily-line-3', figure={},
                                                                          config={'displayModeBar':False})
                                                       ], width=12)
                                                      ]),
                                             ]),
                           
                               ], style={'borderRadius': '10px'}, className="indicators-card mt-1")
                        ], width={'size':4, 'offset':0}),

   
        ]),



    
    dbc.Row([            
             dbc.Col([
                      dbc.Card([
                                dbc.CardBody([
                                              dcc.Graph(id='candlestick', figure={}),
                                            ]),
                                ], style= {'borderRadius': '10px'}, className="dropdown-card mt-1"),
                     ], width={'size':12, 'offset':0})
             
            ]),
   
    


dcc.Interval(id='update', n_intervals=0, interval=1000*5)

], fluid=True)



# Indicator Graph 1 -----------------------------------------------------------
@app.callback(
    Output('indicator-graph-1', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    #day_start = df[df['Date'] == df['Date'].min()]['BTC-USD'].values[0]
    #day_end = df[df['Date'] == df['Date'].max()]['BTC-USD'].values[0]

    previous_value = df_btc.iloc[-2]['price']
    last_value = df_btc.iloc[-1]['price']

    fig1 = go.Figure(go.Indicator(
        mode="delta",
        value=last_value,
        delta={'reference': previous_value, 'relative': True, 'valueformat':'.2%'}))
    fig1.update_traces(delta_font={'size':12})
    fig1.update_layout(height=30, width=70,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')

    if last_value >= previous_value:
        fig1.update_traces(delta_increasing_color='green')
    elif last_value < previous_value:
        fig1.update_traces(delta_decreasing_color='red')

    return fig1

# Indicator Graph 2 -----------------------------------------------------------
@app.callback(
    Output('indicator-graph-2', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    #day_start = df[df['Date'] == df['Date'].min()]['price'].values[0]
    #day_end = df[df['Date'] == df['Date'].max()]['price'].values[0]

    previous_value = df_eth.iloc[-2]['price']
    last_value = df_eth.iloc[-1]['price']



    fig2 = go.Figure(go.Indicator(
        mode="delta",
        value=last_value,
        delta={'reference': previous_value, 'relative': True, 'valueformat':'.2%'}))
    fig2.update_traces(delta_font={'size':12})
    fig2.update_layout(height=30, width=70, 
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')

    if last_value >= previous_value:
        fig2.update_traces(delta_increasing_color='green')
    elif last_value < previous_value:
        fig2.update_traces(delta_decreasing_color='red')

    return fig2

# Indicator Graph 3 -----------------------------------------------------------
@app.callback(
    Output('indicator-graph-3', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    #day_start = df[df['Date'] == df['Date'].min()]['price'].values[0]
    #day_end = df[df['Date'] == df['Date'].max()]['price'].values[0]

    
    previous_value = df_bnb.iloc[-2]['price']
    last_value = df_bnb.iloc[-1]['price']


    fig3 = go.Figure(go.Indicator(
        mode="delta",
        value=last_value,
        delta={'reference': previous_value, 'relative': True, 'valueformat':'.2%'}))
    fig3.update_traces(delta_font={'size':12})
    fig3.update_layout(height=30, width=70,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')


    if last_value >= previous_value:
        fig3.update_traces(delta_increasing_color='green')
    elif last_value < previous_value:
        fig3.update_traces(delta_decreasing_color='red')

    return fig3

        
# Line Graph 1 ---------------------------------------------------------------
@app.callback(
    Output('daily-line-1', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    fig4 = px.line(df_btc, x='date', y='price',
                   range_y=[df_btc['price'].min(), df_btc['price'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    #day_start = df[df['Date'] == df['Date'].min()]['BTC-USD'].values[0]
    #day_end = df[df['Date'] == df['Date'].max()]['BTC-USD'].values[0]

    day_start = df_btc.iloc[-2]['price']
    day_end = df_btc.iloc[-1]['price']

    if day_end >= day_start:
        return fig4.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig4.update_traces(fill='tozeroy',
                             line={'color': 'red'})

# # Line Graph 2---------------------------------------------------------------
@app.callback(
    Output('daily-line-2', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    fig5 = px.line(df_eth, x='date', y='price',
                   range_y=[df_eth['price'].min(), df_eth['price'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    day_start = df_eth.iloc[-2]['price']
    day_end = df_eth.iloc[-1]['price']

    if day_end >= day_start:
        return fig5.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig5.update_traces(fill='tozeroy',
                             line={'color': 'red'})
        
# Line Graph 3 ---------------------------------------------------------------
@app.callback(
    Output('daily-line-3', 'figure'),
    Input('update', 'n_intervals')
)
def update_graph(timer):
    
    fig6 = px.line(df_bnb, x='date', y='price',
                   range_y=[df_bnb['price'].min(), df_bnb['price'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))

    day_start = df_eth.iloc[-2]['price']
    day_end = df_eth.iloc[-1]['price']

    if day_end >= day_start:
        return fig6.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig6.update_traces(fill='tozeroy',
                             line={'color': 'red'})

# Candlestick ---------------------------------------------------------------

@app.callback(
    Output('candlestick','figure'),
    Input('assets-dropdown','value'),
    Input('period-dropdown','value'),
)

def build_graph(ticker, periods):

    # df_mkt = yf.download(tickers = ticker, period = periods, interval = "1h")
    # df_mkt = df_mkt.dropna()

    if periods == '1mo':
        df_mkt=pd.read_csv('/content/periods_1mo.csv', header=[0,1], index_col=0)
    elif periods == '3mo':
        df_mkt=pd.read_csv('/content/periods_3mo.csv', header=[0,1], index_col=0)
    elif periods == '6mo':
        df_mkt=pd.read_csv('/content/periods_6mo.csv', header=[0,1], index_col=0)
    else:
        df_mkt=pd.read_csv('/content/periods_1y.csv', header=[0,1], index_col=0)


    fig7 = go.Figure(data=[go.Candlestick(x=df_mkt.index,
                    open=df_mkt['Open'][ticker], high=df_mkt['High'][ticker],
                    low=df_mkt['Low'][ticker], close=df_mkt['Close'][ticker])
                    ])

    fig7.update_layout(title=f'{ticker} {periods}',
                       #xaxis_rangeslider_visible=False,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)')
    
    return fig7  


if __name__ =='__main__':
    app.run_server(host='127.0.0.1',port=8500, use_reloader=False)
