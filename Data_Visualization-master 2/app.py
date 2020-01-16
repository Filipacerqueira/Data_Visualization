import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

df_social_progress_index = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Social Progress Index')
df_basic_human_needs = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Basic Human Needs')
df_foundations = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Foundations of Wellbeing')
df_opportunity = pd.read_excel('.\\Data\\2014-2019-SPI-Public.xlsx', sheet_name='Opportunity')

df_final = pd.read_excel('.\\Data\\Final df.xlsx')
df_final.iloc[:, 5] = df_final.iloc[:, 5] * 100
data_2016 = pd.read_csv('.\\Data\\cost-of-living-2016.csv')
data_2017 = pd.read_csv('.\\Data\\cost-of-living-2017.csv')
data_2018 = pd.read_csv('.\\Data\\cost-of-living-2018.csv')

df_hdi = pd.read_csv('.\\Data\\human-development-index.csv', header=0, quotechar="'")

for index, row in df_hdi.iterrows():
    if row['Year'] < 2017:
        df_hdi.drop(index, inplace=True)

df_hdi = df_hdi.drop(['Year'], axis=1).reset_index(drop=True)
df_hdi = df_hdi.rename(columns={" ((0-1; higher values are better))": "2017", 'Entity': 'Country'})

data_2016 = data_2016.loc[:, ['City', 'Country', 'Cost.of.Living.Index', 'Rent.Index', 'Groceries.Index']]
data_2016.rename(inplace=True,
                 columns={'Cost.of.Living.Index': 'CLI_16', 'Rent.Index': 'R_16', 'Groceries.Index': 'G_16'})

data_2017 = data_2017.loc[:, ['City', 'Country', 'CLI', 'Rent Index', 'Groceries Index']]
data_2017.rename(columns={'CLI': 'CLI_17', 'Rent Index': 'R_17', 'Groceries Index': 'G_17'}, inplace=True)

data_2018 = data_2018.loc[:, ['City', 'Cost of Living Index', 'Rent Index', 'Groceries Index']]
data_2018.rename(columns={'Cost of Living Index': 'CLI_18', 'Rent Index': 'R_18', 'Groceries Index': 'G_18'},
                 inplace=True)

city = []
country = []
for value in data_2018.loc[:, 'City']:
    city.append(value.split(',')[0])
    country.append(value.split(',')[-1])

data_2018.insert(1, 'Country', pd.DataFrame(country))
data_2018.loc[:, 'City'] = city

all_data = data_2016.merge(data_2017, how='outer', left_on='City', right_on='City')
all_data = all_data.merge(data_2018, how='outer', left_on='City', right_on='City')

all_data.isna().sum()

temp_data = all_data.loc[:, ['Country_x', 'Country_y', 'Country']]
temp_data.replace(np.nan, 0, inplace=True)
all_data.loc[:, ['Country_x', 'Country_y', 'Country']] = temp_data

countries_complete = []
for i in range(all_data.shape[0]):
    if all_data.loc[i, 'Country'] != 0:
        countries_complete.append(all_data.loc[i, 'Country'])
    elif all_data.loc[i, 'Country_y'] != 0:
        countries_complete.append(all_data.loc[i, 'Country_y'])
    else:
        countries_complete.append(all_data.loc[i, 'Country_x'])

countries_complete = [i.strip() for i in countries_complete]
countries_complete = ['United States' if len(i) == 2 else i for i in countries_complete]

all_data['Country_final'] = pd.DataFrame(countries_complete)
all_data = all_data.drop(columns=['Country_x', 'Country_y', 'Country'])
all_data = all_data.rename(columns={'Country_final': 'Country'})

df_cost_living = all_data.loc[:, ['City', 'Country', 'CLI_16', 'CLI_17', 'CLI_18']]
df_rent = all_data.loc[:, ['City', 'Country', 'R_16', 'R_17', 'R_18']]
df_groceries = all_data.loc[:, ['City', 'Country', 'G_16', 'G_17', 'G_18']]

df_cost_living.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_cost_living.reset_index(drop=True, inplace=True)
df_rent.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_rent.reset_index(drop=True, inplace=True)
df_groceries.drop_duplicates(subset=['City', 'Country'], inplace=True)
df_groceries.reset_index(drop=True, inplace=True)

df_temperature = pd.read_csv('.\\Data\\avg_temperature.csv', header=0, sep=';')
df_temperature['Temperature'] = df_temperature['Temperature'].map(lambda x: str(x.replace(',', '.')))
df_temperature['Temperature'] = pd.to_numeric(df_temperature['Temperature'])

df_precipitation = pd.read_csv('.\\Data\\API_AG.LND.PRCP.MM_DS2_en_csv_v2_620809.csv')

df_data_scientist_salary = pd.read_excel('.\\Data\\Data Scientists GROSS Anual Compensation Around the World.xlsx')
df_wage = pd.read_excel('.\\Data\\wage.xlsx')
df_wage1 = df_wage.melt(id_vars='Country', var_name='Year', value_name='Wage')

df_happiness_score = pd.read_excel('.\\Data\\Hapiness Score.xlsx')

df_cost_living_mean = df_cost_living.set_index('Country').groupby(level='Country').mean().reset_index()
df_groceries_mean = df_groceries.set_index('Country').groupby(level='Country').mean().reset_index()
df_rent_mean = df_rent.set_index('Country').groupby(level='Country').mean().reset_index()

df_countries = [df_data_scientist_salary, df_foundations.loc[:, ['Country', 2018]],
                df_hdi, df_opportunity.loc[:, ['Country', 2018]],
                df_social_progress_index.loc[:, ['Country', 2018]],
                df_temperature, df_wage.loc[:, ['Country', '2017']],
                df_cost_living_mean.loc[:, ['Country', 'CLI_18']],
                df_groceries_mean.loc[:, ['Country', 'G_18']],
                df_rent_mean.loc[:, ['Country', 'R_18']],
                df_happiness_score.loc[:, ['Country', 2018]]]

df = df_basic_human_needs.loc[:, ['Country', 2018]]

for dataframe in df_countries:
    cols = dataframe.columns
    if 'Code' in cols:
        dataframe = dataframe.drop(columns='Code')
    if 'Country Name' in cols:
        dataframe = dataframe.rename(columns={'Country Name': 'Country'})
    df = pd.merge(df, dataframe, how='outer', on='Country')

df.columns = ['Country', 'Basic Human Needs', 'Data Scientist Salary', 'Foundations of Wellbeing',
              'HDI', 'Opportunity', 'Social Progress Index', 'Temperature', 'Wage', 'Cost of Living',
              'Groceries', 'Rent', 'Happiness Score']

del all_data, countries_complete, data_2018, data_2017, data_2016, city, country, temp_data

country_options = [dict(label=country, value=country) for country in df_opportunity.iloc[:, 0].unique()]

app = dash.Dash(__name__)

variable_options = [dict(label=variable, value=variable) for variable in df.columns[1:]]

dropdown_globe = dcc.Dropdown(id="dropdown-globe", options=variable_options, value="HDI", clearable=False)

title_two_globe = html.H1(id="title-two-globe", children="About")  # satellite_title, id = satellite-name

globe_description = html.P(
    className="globe-description", id="globe-description", children="""This Dashboard offers you the possibility of \
    comparing various countries in the world,regarding multiple aspects that may peak your interest, while exploring \
    your possibilities when moving abroad. Especially if you're interested in the area of Data Science, it helps you \
    to weigh your options and make the best decision. Start by choosing a variable you want to display on our globe!"""
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

tab1_layout = html.Div(
    id="root",
    children=[
        side_panel_layout,
        globe_body,
    ],
)

tab2_layout = html.Div(children=[
    html.Div([
        html.Div(id='tabContainer2', className='tabs1', children=[
            html.Div(id='tab2_1',
                     children=[html.Div(className='control-tab', id='description2', children=[
                         html.H4(id='title2_1', children=['Which factors matter the most when going abroad?']),
                         html.P(
                             'Now that we already know what each variable represents, it´s important to understand'
                             ' what countries have the best values for each one of them. Choose one of the following'
                             ' variables and take a closer look at the Top 5 countries with the highest values.',
                             id='description2_1', className='description'),
                         html.Div(id='tab2_2',
                                  children=[dcc.Dropdown(id='dropdown_tab2', options=variable_options,
                                                         value='Data Scientist Salary', clearable=False)]
                                  )]
                                        )])]
                 )], style={'width': '49%', 'display': 'inline-block',
                            'vertical-align': 'middle'}, className='row flex-display'),
    html.Div([
        html.Div(
            children=[dcc.Graph(id='barGraph')],
            id='bargraph', className='tabs1'
        )],
        style={'width': '49%', 'display': 'inline-block', 'vertical-align': 'middle'}, className='ta',
        id="mainContainer2")
])

app.layout = html.Div([
    html.Div(id='control_tabs', className='control-tabs',
             children=[
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
                 html.P(id="title-one-globe", children=['PLANNING ON GOING ABROAD?']),
                 html.Br(),
                 dcc.Tabs(id='big-tabs', value='tab1', className='tabs', children=[
                     dcc.Tab(id='tab1',
                             value='tab1',
                             label='World',
                             children=[tab1_layout]
                             ),
                     dcc.Tab(id='tab2',
                             label='Features',
                             children=[tab2_layout]
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
                                                     html.Br(),
                                                     html.Label('About', id='title1',
                                                                className="title"),
                                                     html.P(
                                                         "When moving to a new place, there are many"
                                                         " different factors to consider. "
                                                         "In this tab you can compare these factors "
                                                         "by choosing which countries you want to know "
                                                         "the information about."
                                                         " If you’re interested, you can also see their "
                                                         "gender wage gap evolution over time.",
                                                         id='description',
                                                         className="description",
                                                     ),
                                                     html.Br(),
                                                     html.Label('Select your Countries here',
                                                                style={'font-size': '0.9rem',
                                                                       'colour': '#e0e0eb',
                                                                       'margin-right': '2rem',
                                                                       'margin-left': '2rem',
                                                                       'line-height': '2rem'
                                                                       }),
                                                     dcc.Dropdown(
                                                         id='country_drop',
                                                         options=country_options,
                                                         value=['Portugal', 'United Kingdom', 'Italy', 'Indonesia'],
                                                         multi=True,
                                                         className='drown'
                                                     ),
                                                     html.Br(),
                                                     html.Label('Select a year range',
                                                                style={'margin-right': '2rem',
                                                                       'margin-left': '2rem',
                                                                       'font-size': '0.9rem',
                                                                       'colour': '#e0e0eb'}
                                                                ),
                                                     dcc.RangeSlider(
                                                         id='year_slider',
                                                         min=2006,
                                                         max=2017,
                                                         marks={str(i): '{}'.format(str(i)) for i in
                                                                [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
                                                                 2014, 2015, 2016, 2017]},
                                                         value=[2006, 2017],
                                                         step=1,
                                                         className="dcc_control"
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
                                                                  html.P("World Happiness Score"),
                                                                  html.P("5.38 /10", style={'font-weight': 'bold'})],
                                                                 id="hap_score",
                                                                 className="mini_container",
                                                             ),
                                                             html.Div(
                                                                 [html.H6(id="cosliving"),
                                                                  html.P("World Cost of Living Index"),
                                                                  html.P("63.65%", style={'font-weight': 'bold'
                                                                                          })],
                                                                 id="cli",
                                                                 className="mini_container",
                                                             ),
                                                             html.Div(
                                                                 [html.H6(id="DS_sal"),
                                                                  html.P("World Annual Data Scientists' Salary"),
                                                                  html.P("$ 57576", style={'font-weight': 'bold'})],
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
                                     style={"justify-content": "center"}
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
    data_line = []
    for pais in countries:
        df_line = df_wage1.loc[(df_wage1['Country'] == pais)]
        x_line = [int(el) for el in range(year[0], year[1] + 1, 1)]
        y_line = df_line['Wage']

        data_line.append(dict(type='scatter', mode='lines', x=x_line, y=y_line, name=pais))
    layout_line = dict(title=dict(text='Gender Wage Gap'),
                       yaxis=dict(title='Wage (%)'),
                       template="plotly_dark"
                       )

    data_scatter = []

    for pais1 in countries:
        df_sct = df.loc[(df['Country'] == pais1)]

        x_sct = df_sct['Data Scientist Salary']
        y_sct = df_sct['Happiness Score']
        siz = df_sct['Opportunity']

        data_scatter.append(dict(type='scatter', mode='markers', x=x_sct, y=y_sct,
                                 name=pais1, marker=dict(size=siz),
                                 hovertemplate='Data Scientists Salary: %{x}$ <br>' +
                                               'Happiness Score Index: %{y}% <br>' + 'Opportunity Index:\
                                                %{marker.size}%'))

    layout_sct = dict(title=dict(text='Happiness Score and Opportunity Index by DS Salary'),
                      yaxis=dict(title='Happiness Score'),
                      xaxis=dict(title='Data Scientists Salary'),
                      template="plotly_dark"
                      )

    data_bar = []
    for pais2 in countries:
        df_bar = df.loc[(df['Country'] == pais2)]

        y = df_bar[['Cost of Living', 'Groceries', 'Rent']].values[0]

        x0 = ['Cost of Living', 'Groceries', 'Rent']
        data_bar.append(dict(type='bar', x=x0, y=y,
                             name=pais2))

    layout_bar = dict(title=dict(text='How expensive is it to live here?'),
                      template="plotly_dark")

    x_dot1 = []
    x_dot2 = []
    x_dot3 = []
    x_dot4 = []
    data_dot = []

    for pais3 in countries:
        df_dot = df_final.loc[(df_final['Country'] == pais3)]
        x_dot1.append(list(df_dot['Basic Human Needs'])[0])
        x_dot2.append(list(df_dot['Foundations of wellbeing'])[0])
        x_dot3.append(list(df_dot['Social Progress Index'])[0])
        x_dot4.append(list(df_dot['HDI'])[0])

    y_dot = countries
    x = [x_dot1, x_dot2, x_dot3, x_dot4]
    colors = ['#1798AF', '#4A52B4', '#7C4AB4', '#AC402E']
    names = ['Basic Human Needs', 'Foundations of Wellbeing', 'Social Progress Index', 'HDI']

    for i1 in range(len(x)):
        data_dot.append(dict(type='scatter', mode='markers', x=x[i1], y=y_dot,
                             name=names[i1], marker=dict(color=colors[i1], line_width=1, symbol='circle', size=16)))

    layout_dot = dict(title="Countries' Indexes",
                      xaxis=dict(
                          showgrid=False,
                          showline=True,
                          linecolor='rgb(102, 102, 102)',
                          tickfont_color='rgb(102, 102, 102)',
                          showticklabels=True,
                          tick0=0,
                          ticks='outside',
                          tickcolor='rgb(102, 102, 102)',
                      ),
                      legend=dict(
                          font_size=10,
                          x=-0.5,
                          y=-0.5,
                      ),
                      template="plotly_dark",
                      )

    return go.Figure(data=data_line, layout=layout_line), go.Figure(data=data_scatter, layout=layout_sct), \
           go.Figure(data=data_bar, layout=layout_bar), go.Figure(data=data_dot, layout=layout_dot)


@app.callback(
    Output("globe-graph", "figure"),
    [
        Input("dropdown-globe", "value"),
    ],
)
def update_globe_body(variable):
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
                                   text='Scale of ' + str(variable),
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
    fig.update_layout(paper_bgcolor="#1e1e1e")

    return fig


@app.callback(
    Output('dropdown-variable-description', 'children'),
    [Input('dropdown-globe', 'value')])
def variable_description(val):
    df_colnames = [j for j in df.columns]
    variable_descriptions = ['Basic Human Needs is an Index that combines multiple factors regarding Nutrition and '
                             'Basic Medical Care, Water and Sanitation, Shelter and Personal Safety.',
                             'Data Scientists salary refers to the average gross Annual Compensation of someone '
                             'working in the area of Data Science',
                             'Foundations of Wellbeing is an Index that is mainly focused on the Access to Basic'
                             ' Knowledge, Access to Information and Communications, Health and Wellness and '
                             'Environmental Quality.',
                             'The Human Development Index is about emphasizing that people and their capabilities '
                             'should be the ultimate criteria for assessing the development of a country, not '
                             'economic growth alone.It includes a Life expectancy Index, Education Index and GNI'
                             ' Index.',
                             'Opportunity is an Index that includes Personal Rights, Personal Freedom and Choice,'
                             ' Inclusiveness and Access to Advanced Education.',
                             'Social Progress Index joins the Basic Human Needs, Foundations of Wellbeing and '
                             'Opportunity Indices into one.',
                             'Temperature is the average minimal(mean) and maximal(mean) temperature of a country.',
                             'Wage is an Index that refers to the unadjusted Gender Pay Gap (GPG) and represents the '
                             'difference between average gross hourly earnings of male paid employees and of female '
                             'paid employees as a percentage of average gross hourly earnings of male paid employees',
                             'Cost of living is an Index regarding the overall estimation of living in a country, '
                             'including every necessary expenses one can have.',
                             'Groceries is an Index regarding the average princes for groceries in a country.',
                             'The Rent Index refers to the average cost of renting an apartment in a country',
                             'Happiness Score by the The World Happiness Report is an annual publication of the United'
                             ' Nations Sustainable Development Solutions Network. It contains articles, and rankings of'
                             ' national happiness based on respondent ratings of their own lives, which the report '
                             'also correlates with various life factors']

    return variable_descriptions[df_colnames.index(str(val)) - 1]


@app.callback(Output("barGraph", "figure"), [Input("dropdown_tab2", "value")])
def plot_tab2(var):
    data_bar = []

    df_bar = df.sort_values(by=[str(var)], ascending=False).iloc[0:5]

    x_bar = df_bar[str(var)]
    y_bar = df_bar['Country']

    data_bar.append(dict(type='bar', x=x_bar, y=y_bar, name=var, orientation='h',
                         marker=dict(color=['#05946E', '#1798AF', '#4A52B4', '#7C4AB4', '#AC402E'])))

    layout_bar = dict(title=dict(text='Top 5 Countries for ' + str(var), x=.5, ), template="plotly_dark")
    fig = go.Figure(data=data_bar, layout=layout_bar)
    return fig


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
