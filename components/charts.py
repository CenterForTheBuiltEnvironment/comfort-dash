import plotly.express as px


def chart_example():
    df = px.data.gapminder()  # replace with your own data source
    countries = df.country.drop_duplicates().sample(n=10, random_state=42)
    df = df[df.country.isin(countries)]

    fig = px.area(df, x="year", y="pop", color="continent", line_group="country")
    return fig

