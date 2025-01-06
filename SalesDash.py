# import related libraries
import plotly.express as px
import pandas as pd
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from datetime import date
from dash.dependencies import Output, Input

# prepare data
df_orders = pd.read_csv('OrdersSmallest.csv')
df_orders['Order Date'] = pd.to_datetime(df_orders['Order Date'], format='%d/%m/%Y')
df_orders['Ship Date'] = pd.to_datetime(df_orders['Ship Date'], format='%d/%m/%Y')
# removing $ and , and convert to numeric field
df_orders['Profit'] = df_orders['Profit'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df_orders['Profit'] = pd.to_numeric(df_orders['Profit'])
# removing $ and , and convert to numeric field
df_orders['Sales'] = df_orders['Sales'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df_orders['Sales'] = pd.to_numeric(df_orders['Sales'])

# using a bootstrap theme SKETCHY
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SKETCHY])

# prepare two charts using the processed dataframe
fig1 = px.histogram(df_orders, x='Order Date', y='Sales', title='Sales by Order Date')
fig2 = px.histogram(df_orders, x='Category', y='Quantity', title='Category Quantity',
                    color='Category', barmode='group')

# configure layout
# layout has 3 rows, 1st row contains image & Title, 2nd row are cards, 3rd row are charts
app.layout = dbc.Container([
    # row 1, logo image needs to be stored in the assets subfolder
    dbc.Row([
        dbc.Col([
            html.Img(src=app.get_asset_url('Logo.png'), alt='dashlogo')
        ], width=2),
        dbc.Col([
            dcc.DatePickerSingle(
                id='my_start_date',
                display_format='YYY-MM-DD',
                date=date(2015, 12, 1)
            ),
            dcc.DatePickerSingle(
                id='my_end_date',
                display_format='YYY-MM-DD',
                date=date(2015, 12, 31)
            ),
        ], width=4),
        dbc.Col([
            html.H1('Sales & Profit Dashboard')
        ], width=6),
    ], className='mb-2 mt-2'),
    # row 2, consists of 4 cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Sales'),
                    html.H2(id='card_TotalSales', children='000')
                ],style={'textAlign':'center'})
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Profit'),
                    html.H2(id='card_TotalProfit', children='000')
                ], style={'textAlign': 'center'})
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Total Quantity'),
                    html.H2(id='card_TotalQuantity', children='000')
                ], style={'textAlign': 'center'})
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('Customer Count'),
                    html.H2(id='card_TotalCustomer', children='000')
                ], style={'textAlign': 'center'})
            ])
        ], width=3),
    ], className='mb-2 mt-2'),
    # row 3 consists of two charts fig1 & fig2
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='chart1',
                figure=fig1
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='chart2',
                figure=fig2
            )
        ], width=6),
    ], className='mb-2 mt-2')
])


# define callback for row 2 cards
@app.callback(
    Output('card_TotalSales', 'children'),
    Output('card_TotalProfit', 'children'),
    Output('card_TotalQuantity', 'children'),
    Output('card_TotalCustomer', 'children'),
    Input('my_start_date', 'date'),
    Input('my_end_date', 'date'),
)
def update_cards(start_date, end_date):
    # filter the records to mask & allocate new dataframe
    mask = (df_orders['Order Date'] >= start_date) & (df_orders['Order Date'] <= end_date)
    df2 = df_orders.loc[mask]
    total_sales = round(df2['Sales'].sum(), 0)
    total_profit = round(df2['Profit'].sum(), 0)
    total_quantity = df2['Quantity'].sum()
    total_customer = len(df2['Customer ID'].unique())
    return total_sales, total_profit, total_quantity, total_customer


# define callback for row 3 charts
@app.callback(
    Output('chart1', 'figure'),
    Output('chart2', 'figure'),
    Input('my_start_date', 'date'),
    Input('my_end_date', 'date'),
)
def update_charts(start_date, end_date):
    # filter the records to mask & allocate new dataframe
    mask = (df_orders['Order Date'] >= start_date) & (df_orders['Order Date'] <= end_date)
    df2 = df_orders.loc[mask]
    fig_1 = px.histogram(df2, x='Order Date', y='Sales', title='Sales by Order Date')
    fig_2 = px.histogram(df2, x='Category', y='Quantity', title='Category Quantity', color='Category', barmode='group')
    return fig_1, fig_2


# execute the program
if __name__ == '__main__':
    app.run_server(host='localhost', port=8050)
