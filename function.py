import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
import plotly.graph_objs as go

from DV_code import *


###################### Data Processing ###################################################################

#mudar no scatter o happiness score bem
#meter no mini container do salario o salario anual para estar coerente com o grafico

#################################################################################################################

country_options = [dict(label=country, value=country) for country in df_opportunity.iloc[:, 0].unique()]

app = dash.Dash(__name__)

# Functions for the first tab

# Dropdown to chose variable that's displayed on the globe
variable_options = [dict(label=variable, value=variable) for variable in df.columns[1:]]

dropdown_globe = dcc.Dropdown(
    id="dropdown-globe",
    options=variable_options,
    value="HDI",
    clearable=False
)


title_two_globe = html.H1(id="title-two-globe", children="About") # satellite_title, id = satellite-name

globe_description = html.P(
    className="globe-description", id="globe-description", children="""This Dashboard offers you the possibility of comparing various countries in the world,\
    regarding multiple aspects that may peak your interest, while exploring your possibilities when moving abroad. Especially if you're interested in the area of Data\
    Science, it helps you to weigh your options and make the best decision. Start by choosing a variable you want to display on our globe!"""
)


side_panel_layout = html.Div(
    id="panel-side",
    children=[
        html.Div(id="panel-side-text", children=[title_two_globe, globe_description]),
        html.Br(),
        html.Div(id="globe-dropdown", children=dropdown_globe),
        html.Div(id='dropdown-variable-description'),
    ],
)


globe_body = html.Div(
    id='globe-body',
    children=[

        dcc.Graph(
        id='globe-graph',
        )
    ],
)

# Layout for the first tab
tab1_layout = html.Div(
    id="root",
    children=[
        side_panel_layout, # side_panel_layout
        globe_body, # main_panel_layout
    ],
)



 ################################################################################################################
app.layout = html.Div([
    html.Div(id='control_tabs', className='control-tabs',
             children=[
                # Code for header layout
                html.Div([
                        html.Img(
                            src=app.get_asset_url("IMS_logo.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "100px",
                                "margin-bottom": "0px",
                            },
                        )
                    ]),
                 # html.Br(),
                 html.P(id="title-one-globe", children=['PLANNING ON GOING ABROAD?']),
                 html.Br(),
                 dcc.Tabs(id='big-tabs', value='what-is', className='tabs', children=[
                     dcc.Tab(id='tab1',
                             label='World',
                             children=[tab1_layout]
                             ),
                     dcc.Tab(id='tab2',
                             label='Features',
                             children=[]
                             ),
                     dcc.Tab(id='tab3',
                             label='Countries',
                             children=[
                                 html.Br(),
                                 html.Div([
                                     html.Div(
                                         [
                                             html.Div(
                                                 [
                                                     html.Label('About', id='title1',
                                                                className="title"),
                                                     html.P(
                                                         "When moving to a new place there are many"
                                                         " different factors to consider."
                                                         "In this tab you can compare this factors "
                                                         "by choosing which countries you want to know "
                                                         "the information about."
                                                         "If you’re interested you can also see their "
                                                         "gender wage gap evolution over time.",
                                                         id='description',
                                                         className="description",
                                                     ),
                                                     html.Br(),
                                                     html.Label('Select your Countries here'),
                                                     dcc.Dropdown(
                                                         id='country_drop',
                                                         options=country_options,
                                                         value=['Portugal'],
                                                         multi=True,
                                                         className='drown'
                                                     ),
                                                     html.Br(),
                                                     html.Label('Year Range'),
                                                     dcc.RangeSlider(
                                                         id='year_slider',
                                                         min=2006,
                                                         max=2017,
                                                         marks={str(i): '{}'.format(str(i)) for i in
                                                                [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
                                                                 2015, 2016, 2017]},
                                                         value=[2006, 2017],
                                                         step=1,
                                                         className="dcc_control",
                                                     ),
                                                 ],
                                                 className="pretty_container four columns",
                                                 id="cross-filter-options",
                                             ),
                                             html.Div(
                                                 [
                                                     html.Div(
                                                         [
                                                             html.Div(
                                                                 [html.H6(id="happiness"),
                                                                  html.P("World Happiness Score"), html.P("5.38 /10")],
                                                                 id="hap_score",
                                                                 className="mini_container",
                                                             ),
                                                             html.Div(
                                                                 [html.H6(id="cosliving"),
                                                                  html.P("World Cost of Living Index"),
                                                                  html.P("63.65%")],
                                                                 id="cli",
                                                                 className="mini_container",
                                                             ),
                                                             html.Div(
                                                                 [html.H6(id="DS_sal"),
                                                                  html.P("World Annual Data Scientists' Salary"),
                                                                  html.P("$ 57576")],
                                                                 id="salary",
                                                                 className="mini_container",
                                                             ),
                                                         ],
                                                         id="info-container",
                                                         className="row container-display",
                                                     ),
                                                     html.Div(
                                                         [dcc.Graph(id="wage_graph")],
                                                         id="wageGraphContainer",
                                                         className="pretty_container",
                                                     ),
                                                 ],
                                                 id="right-column",
                                                 className="eight columns",
                                             ),
                                         ],
                                         className="row flex-display",

                                     ),
                                     html.Div(
                                         [
                                             html.Div(
                                                 [dcc.Graph(id="scatter")],
                                                 className="pretty_container seven columns",
                                             ),
                                             html.Div(
                                                 [dcc.Graph(id="funnel")],
                                                 className="pretty_container five columns",
                                             ),
                                         ],
                                         className="row flex-display",
                                     ),
                                     html.Div(
                                         [
                                             html.Div(
                                                 [dcc.Graph(id="bar_graph")],
                                                 className="pretty_container seven columns",
                                             ),
                                         ],
                                         className="row flex-display",
                                     ),
                                 ],
                                     id="mainContainer",
                                     style={"display": "flex", "flex-direction": "column"}
                                 )

                             ]
                             )

                 ])
             ])
])


@app.callback(
    [
        Output("wage_graph", "figure"),
        Output("scatter", "figure"),
        Output("bar_graph", "figure"),
        Output("funnel", "figure"),
    ],
    [
        Input("year_slider", "value"),
        Input("country_drop", "value"),
    ]
)
def plots(year, countries):
    ######################################################################################################
    data_line = []
    for country in countries:
        df_line = df_wage1.loc[(df_wage1['Country'] == country)]
        x_line = df_line['Year']
        y_line = df_line['Wage']

        data_line.append(dict(type='scatter', mode='lines', x=x_line, y=y_line, name=country))
    layout_line = dict(title=dict(text='Gender Wage Gap'),
                       yaxis=dict(title='Wage (%)'),
                       template="plotly_dark"
                       )

    ####################################################################################################################
    data_scatter = []

    for country in countries:
        df_sct = df.loc[(df['Country'] == country)]

        x_sct = df_sct['Data Scientist salary']
        y_sct = df_sct['Happiness Score']
        siz = df_sct['Opportunity']

        data_scatter.append(dict(type='scatter', mode='markers', x=x_sct, y=y_sct,
                                 name=country, marker=dict(size=siz),
                                 hovertemplate='Data Scientists Salary: %{x}$ <br>' +
                                               'Happiness Score Index: %{y}% <br>' + 'Opportunity Index: %{marker.size}%'))

        layout_sct = dict(title=dict(text='Happiness Score and Opportunity Index by DS Salary'),
                          yaxis=dict(title='Happiness Score'),
                          xaxis=dict(title='Data Scientists Salary'),
                          template="plotly_dark"
                          )
    ####################################################################################################################
    data_bar = []
    for country in countries:
        df_bar = df.loc[(df['Country'] == country)]

        y = df_bar[['Cost of living', 'Groceries', 'Rent']].values[0]

        x0 = ['Cost of Living', 'Groceries', 'Rent']
        data_bar.append(dict(type='bar', x=x0, y=y,
                             name=country))

        layout_bar = dict(title=dict(text='How expensive is it to live here?'),
                          template="plotly_dark")
    ####################################################################################################################
    x1 = df_final[['Opportunity']]
    x2 = df_final[['Basic Human Needs']]
    x3 = df_final[['Foundations of wellbeing']]

    trace1 = go.Funnel(
        name='Opportunity',
        orientation="h",
        y=countries, x=x1)

    trace2 = go.Funnel(
        name='Basic Human Needs',
        orientation="h",
        y=countries, x=x2)

    trace3 = go.Funnel(
        name='Foundations of Wellbeing',
        orientation="h",
        y=countries, x=x3)

    layout = go.Layout(margin={"l": 200, "r": 200}, funnelmode="stack", showlegend=True, template="plotly_dark")

    return go.Figure(data=data_line, layout=layout_line), \
           go.Figure(data=data_scatter, layout=layout_sct),\
           go.Figure(data=data_bar, layout=layout_bar), \
           go.Figure([trace1, trace2, trace3], layout),



# Callbacks for the first tab

@app.callback(
    Output("globe-graph", "figure"),
    [
        Input("dropdown-globe", "value"),
    ],
)

def update_globe_body(variable): # update_word_map
    data_choropleth = dict(type='choropleth',
                           locations=df['Country'],
                           locationmode='country names',
                           z=df[str(variable)],
                           text=df['Country'],
                           colorscale='Viridis',
                           colorbar=dict(
                               ticks="outside",
                               tickfont=dict(
                                   color='#cdecf2'
                               ),
                               title=dict(
                                   text='Scale of '+str(variable),
                                   font=dict(
                                       color='#cdecf2'))))

    layout_choropleth = dict(width=800,
                             height=800,
                             geo=dict(scope='world',  # default
                                      projection=dict(type='orthographic',
                                                      ),
                                      landcolor='black',
                                      lakecolor='#1e1e1e',
                                      showocean=True,
                                      oceancolor='#cdecf2',
                                      bgcolor='#1e1e1e',
                                      showframe=False,
                                      ),
                             )

    fig = go.Figure(data=data_choropleth, layout=layout_choropleth)
    fig.update_layout(
        # margin=dict(l=0, r=20, t=20, b=20),
        paper_bgcolor="#1e1e1e",
    )

    return fig

# Returns a description of the variable selected in dropdown-globe
@app.callback(
    Output('dropdown-variable-description', 'children'),
    [Input('dropdown-globe', 'value')])

def variable_description(value):
    df_colnames = [i for i in df.columns]
    variable_descriptions =    ['Basic Human Needs is an Index that combines multiple factors regarding Nutrition and \
    Basic Medical Care, Water and Sanitation, Shelter and Personal Safety.','Data Scientists salary refers to the \
    average gross Anual Compensation of someone working in the area of Data Science', 'Foundations of Wellbeing is an \
    Index that is mainly focused on the Access to Basic Knowledge, Access to Information and Communications, Health and\
     Wellness and Environmental Quality.', 'The Human Development Index is about emphasizing that people and their \
     capabilities should be the ultimate criteria for assessing the development of a country, not economic growth alone. \
     It includes a Life expectancy Index, Education Index and GNI Index.', 'Opportunity is an Index that includes \
     Personal Rights, Personal Freedom and Choice, Inclusiveness and Access to Advanced Education.', 'Social Progress \
     Index joins the Basic Human Needs, Foundations of Wellbeing and Opportunity Indices into one.', 'Temperature is the \
     average minimal(mean) and maximal(mean) temperature of a country.','Wage is an Index that refers to the unadjusted \
     Gender Pay Gap (GPG) and represents the difference between average gross hourly earnings of male paid employees and \
     of female paid employees as a percentage of average gross hourly earnings of male paid employees', 'Cost of living \
     is an Index regarding the overall estimation of living in a country, including every necessary expenses one can \
     have.', 'Groceries is an Index regarding the average princes for groceries in a country.', 'The Rent Index refers \
     to the average cost of renting an apartment in a country','Happiness Score by the The World Happiness Report is an \
     annual publication of the United Nations Sustainable Development Solutions Network. It contains articles, and \
     rankings of national happiness based on respondent ratings of their own lives, which the report also correlates \
     with various life factors']

    return variable_descriptions[df_colnames.index(str(value))-1]


if __name__ == '__main__':
    app.run_server(debug=True)
