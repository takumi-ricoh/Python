import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input_id', value=None, type='text'),
    html.Div(id='output_div')
])


@app.callback(
    Output(component_id='output_div', component_property='children'),
    [Input(component_id='input_id', component_property='value')]
)
def update_output_div(input_value):
    if input_value:
        return html.Div(className='output-area', children=[
            html.Span(input_value)
        ])
    else:
        html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)