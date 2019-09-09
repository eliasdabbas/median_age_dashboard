import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s==%(funcName)s==%(message)s')

age_df = pd.read_csv('data/country_data_master.csv', 
                     usecols=lambda cols: 'perc' in cols or cols == 'country' or cols == 'median_age_total')
age_df = age_df.sort_values(['median_age_total'])
age_categories = ['0-14', '15-24', '25-54', '55-64', '65+']


app = dash.Dash()
server = app.server

app.layout = html.Div([
    
    dcc.Graph(id='median_age_graph', 
              config={'displayModeBar': False}),
    html.Div([
    dcc.Dropdown(id='country_dropdown',
                 multi=True,
                 value=tuple(),
                 options=[{'label': c, 'value': c}
                          for c in sorted(age_df['country'])]),        
    ], style={'width': '50%', 'margin-left': '25%'}),
    dcc.Graph(id='age_graph',
             config={'displayModeBar': False}),
    # html.Div([
    # html.Content('Data: CIA Factbook'), html.Content('  '),
    # html.A('Median Age', href='https://www.cia.gov/library/publications/the-world-factbook/fields/2177.html'), html.Content('   '),
    # html.A('Age Structure', href='https://www.cia.gov/library/publications/the-world-factbook/fields/2010.html'),
    #
    # ], style={'display': 'inline'}),

], style={'background-color': '#eeeeee'})

@app.callback(Output('median_age_graph', 'figure'),
             [Input('country_dropdown', 'value')])
def plot_median_age(countries):
    logging.info(msg=locals())
    df = age_df[age_df['country'].isin(countries)]
    return {
        'data': [go.Scatter(x=age_df['country'],
                            y=age_df['median_age_total'],
                            mode='markers',
                            showlegend=False,
                            legendgroup='one',
                            name='',
                            hoverlabel={'font': {'size': 20}},
                            marker={'color': '#bbbbbb'})] +
                [go.Scatter(x=df[df['country']==c]['country'],
                            y=df[df['country']==c]['median_age_total'],
                            mode='markers',
                            marker={'size': 15},
                            # hovertext={'font': {'size': 30}},
                            hoverlabel={'font': {'size': 20}},
                            name=c)
                 for c in sorted(countries)],
        'layout': go.Layout(title='Median Age by Country: ' + ', '.join(countries),
                            xaxis={'title': 'Countries', 'zeroline': False, 
                                   'showticklabels': False},
                            yaxis={'title': 'Median Age', 'zeroline': False},
                            font={'family': 'Palatino'},
                            paper_bgcolor='#eeeeee',
                            plot_bgcolor='#eeeeee'
),
    }

@app.callback(Output('age_graph', 'figure'),
             [Input('country_dropdown', 'value')])
def plot_countries(countries):
    df = age_df[age_df['country'].isin(countries)].sort_values('country')
    return {
        'data': [go.Bar(x=age_categories,
                        y=[0 for i in range(len(age_categories))],
                        showlegend=False,
                        width=0.1,
                        hoverinfo='none')] +
                
                [go.Bar(x=age_categories,
                        y=df.iloc[x, 2:7],
                        name=df.iloc[x, 0],
                        text=df.iloc[x, 2:7].astype(str) + '%',
                        hoverinfo='name+y',
                        textposition='inside',
                        textfont={'color': 'white'})
                 for x in range(len(df))],
        'layout': go.Layout(title='Age Distribution by Country: ' + ', '.join(countries),
                            xaxis={'title': 'Age Group Percentage', 'zeroline': False},
                            yaxis={'title': 'Percentage', 'zeroline': False},
                            font={'family': 'Palatino'},
                            barmode='group',
                            plot_bgcolor='#eeeeee',
                            paper_bgcolor='#eeeeee')
        
    }

if __name__ == '__main__':
    app.run_server()