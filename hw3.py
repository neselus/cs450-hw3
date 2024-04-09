import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# Load the dataset
df = pd.read_csv('C:\\Users\\nlus2\\OneDrive\\Desktop\\Spring 2024\\CS450\\ProcessedTweets.csv')

# Create Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Month:"),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': month, 'value': month} for month in df['Month'].unique()],
                    value=df['Month'].unique()[0]  # Set default value
                ),
            ], width=3),
            dbc.Col([
                html.Label("Sentiment Range:"),
                dcc.RangeSlider(
                    id='sentiment-slider',
                    min=df['Sentiment'].min(),
                    max=df['Sentiment'].max(),
                    value=[df['Sentiment'].min(), df['Sentiment'].max()],
                    marks={-1: '-1', 0: '0', 1: '1'},  # Customize slider marks
                ),
            ], width=3),
            dbc.Col([
                html.Label("Subjectivity Range:"),
                dcc.RangeSlider(
                    id='subjectivity-slider',
                    min=df['Subjectivity'].min(),
                    max=df['Subjectivity'].max(),
                    value=[df['Subjectivity'].min(), df['Subjectivity'].max()],
                    marks={0: '0', 0.5: '0.5', 1: '1'},  # Customize slider marks
                ),
            ], width=3),
        ]),
        html.Div([
            dcc.Graph(
                id='scatter-plot',
                style={'height': '400px', 'width': '100%'}  # Adjust height and width
            ),
            dash_table.DataTable(
                id='tweet-table',
                columns=[{'name': 'RawTweet', 'id': 'RawTweet'}],
                page_size=10,
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_cell={'textAlign': 'left', 'fontSize': 12, 'whiteSpace': 'normal', 'paddingTop': '10px'},
                style_header={'fontWeight': 'bold', 'fontSize': 14, 'textAlign': 'center'},
            ),
        ], style={'marginTop': '0px', 'marginBottom': '10px'}),  # Add margin bottom for spacing
    ]),
])

# Initialize selected tweets
selected_tweets = []

# Define callback to update scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('month-dropdown', 'value'),
     Input('sentiment-slider', 'value'),
     Input('subjectivity-slider', 'value')]
)
def update_scatter_plot(selected_month, sentiment_range, subjectivity_range):
    filtered_df = df[df['Month'] == selected_month]
    filtered_df = filtered_df[(filtered_df['Sentiment'] >= sentiment_range[0]) & (filtered_df['Sentiment'] <= sentiment_range[1])]
    filtered_df = filtered_df[(filtered_df['Subjectivity'] >= subjectivity_range[0]) & (filtered_df['Subjectivity'] <= subjectivity_range[1])]

    fig = go.Figure(data=go.Scatter(
        x=filtered_df['Dimension 1'],
        y=filtered_df['Dimension 2'],
        mode='markers',
        hovertext=filtered_df['RawTweet'],
    ))
    fig.update_layout(
        width=1100,  # Set width in pixels
        height=350,  # Set height in pixels
        transition_duration=500,  # Add smooth transition
        xaxis=dict(showticklabels=False),  # Hide x-axis labels
        yaxis=dict(showticklabels=False),  # Hide y-axis labels
    )
    return fig

# Define callback to update selected tweets
@app.callback(
    Output('tweet-table', 'data'),
    [Input('scatter-plot', 'selectedData')]
)
def update_selected_tweets(selected_data):
    global selected_tweets
    selected_tweets = []
    if selected_data and 'points' in selected_data:
        selected_points = selected_data['points']
        for point in selected_points:
            selected_tweets.append({'RawTweet': point['hovertext']})
    return selected_tweets

if __name__ == '__main__':
    app.run_server(debug=True)
