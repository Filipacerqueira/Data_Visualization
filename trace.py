data_trace = []
    for country in countries:
        df_trace = df_final.loc[(df['Country'] == country)]
        x1 = df_trace[['Opportunity']]
        x2 = df_trace[['Basic Human Needs']]
        x3 = df_trace[['Foundations of wellbeing']]

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
