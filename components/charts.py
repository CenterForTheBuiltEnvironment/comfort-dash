import plotly.express as px


# fig example
def chart_example(selected_model, chart_content):

    df = px.data.gapminder()
    countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
    df = df[df["country"].isin(countries)]
    fig = px.bar(
        df,
        x="year",
        y="lifeExp",
        color="country",
        barmode="group",
        title="PMV_ashrae psychrometric figure",
    )
    return fig
