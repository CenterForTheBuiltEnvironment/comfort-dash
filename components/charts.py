import plotly.express as px
from utils.my_config_file import (
    MODELS,
    CHARTS,
)
import pandas as pd


# fig example
def chart_example(selected_model, chart_content):

    # PMV - EN 16798 figure
    if selected_model == MODELS.PMV_EN.value:
        if chart_content == CHARTS.psychrometric.value:
            print("PMV_EN psychrometric figure")
            df = px.data.gapminder()  # replace with your own data source
            countries = df.country.drop_duplicates().sample(n=10, random_state=42)
            df = df[df.country.isin(countries)]
            fig = px.line(
                df,
                x="year",
                y="gdpPercap",
                color="country",
                line_group="country",
                title="PMV_EN psychrometric figure",
                labels={"gdpPercap": "GDP per Capita", "year": "Year"},
            )
            return fig
        elif chart_content == CHARTS.psychrometric_operative.value:
            print("PMV_EN psychrometric operative figure")
            df = px.data.gapminder()  # replace with your own data source
            countries = df.country.drop_duplicates().sample(n=10, random_state=42)
            df = df[df.country.isin(countries)]
            fig = px.scatter(
                df,
                x="gdpPercap",
                y="lifeExp",
                size="pop",
                color="continent",
                hover_name="country",
                log_x=True,
                size_max=60,
                title="PMV_EN psychrometric operative figure",
                labels={
                    "gdpPercap": "GDP per Capita",
                    "lifeExp": "Life Expectancy",
                    "pop": "Population",
                },
            )
            return fig
        elif chart_content == CHARTS.relative_humidity.value:
            print("PMV_EN relative_humidity figure")
            data = {
                "Room": ["Room A", "Room B", "Room C", "Room D", "Room E"],
                "Temperature (°C)": [22, 24, 26, 28, 30],
                "Humidity (%)": [40, 45, 50, 55, 60],
                "Air Speed (m/s)": [0.1, 0.2, 0.15, 0.25, 0.3],
                "PMV": [-0.5, -0.3, 0.0, 0.2, 0.5],
            }
            df = pd.DataFrame(data)

            fig = px.bar(
                df,
                x="Room",
                y="PMV",
                color="Temperature (°C)",
                title="PMV_EN relative_humidity figure",
                labels={"PMV": "Predicted Mean Vote"},
                text="PMV",
            )

            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            return fig
        else:
            print("PMV_EN psychrometric figure")
            df = px.data.gapminder()  # replace with your own data source
            countries = df.country.drop_duplicates().sample(n=10, random_state=42)
            df = df[df.country.isin(countries)]
            fig = px.line(
                df,
                x="year",
                y="gdpPercap",
                color="country",
                line_group="country",
                title="PMV_EN psychrometric figure",
                labels={"gdpPercap": "GDP per Capita", "year": "Year"},
            )
            return fig

    # PMV - Ashare 55 figure
    elif selected_model == MODELS.PMV_ashrae.value:
        if chart_content == CHARTS.psychrometric.value:
            print("PMV_ashrae psychrometric figure")
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
        elif chart_content == CHARTS.psychrometric_operative.value:
            print("PMV_ashrae psychrometric operative figure")
            df = px.data.gapminder()
            countries = df.country.drop_duplicates().sample(n=10, random_state=42)
            df = df[df.country.isin(countries)]
            fig = px.line(
                df,
                x="year",
                y="gdpPercap",
                color="continent",
                line_group="country",
                title="PMV_ashrae psychrometric operative figure",
                labels={
                    "gdpPercap": "GDP per Capita",
                    "year": "Year",
                    "continent": "Continent",
                },
            )
            return fig
        elif chart_content == CHARTS.relative_humidity.value:
            print("PMV_ashrae relative_humidity figure")
            data = {
                "Room": ["Room A", "Room B", "Room C", "Room D", "Room E"],
                "Temperature (°C)": [22, 24, 26, 28, 30],
                "Humidity (%)": [40, 45, 50, 55, 60],
                "Air Speed (m/s)": [0.1, 0.2, 0.15, 0.25, 0.3],
                "PMV": [-0.5, -0.3, 0.0, 0.2, 0.5],
            }
            df = pd.DataFrame(data)

            fig = px.bar(
                df,
                x="Room",
                y="PMV",
                color="Temperature (°C)",
                title="PMV_ashrae relative_humidity figure",
                labels={"PMV": "Predicted Mean Vote"},
                text="PMV",
            )

            fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
            return fig
        elif chart_content == CHARTS.air_speed.value:
            print("PMV_ashrae air speed figure")
            df = px.data.gapminder()
            countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
            df = df[df["country"].isin(countries)]

            fig = px.scatter(
                df,
                x="gdpPercap",
                y="pop",
                size="gdpPercap",
                color="continent",
                hover_name="country",
                log_x=True,
                size_max=60,
                title="PMV_ashrae air speed figure",
                labels={"gdpPercap": "GDP per Capita", "pop": "Population"},
            )
            return fig
        elif chart_content == CHARTS.thermal_heat.value:
            print("PMV_ashrae thermal heat figure")
            df = px.data.gapminder()
            countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
            df = df[df["country"].isin(countries)]

            fig = px.line(
                df,
                x="year",
                y="pop",
                color="continent",
                line_group="country",
                title="PMV_ashrae thermal heat figure",
                labels={"pop": "Population", "year": "Year"},
            )
            return fig
        elif chart_content == CHARTS.set_outputs.value:
            print("PMV_ashrae set output figure")
            df = px.data.gapminder()
            countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
            df = df[df["country"].isin(countries)]
            fig = px.bar(
                df,
                x="continent",
                y="lifeExp",
                color="continent",
                barmode="group",
                title="PMV_ashrae set output figure",
                labels={"lifeExp": "Life Expectancy", "continent": "Continent"},
                hover_name="country",
            )
            return fig
        # default
        else:
            print("PMV_ashrae psychrometric figure")
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

    # Adaptive - Ashare 55 figure
    elif selected_model == MODELS.Adaptive_ashrae.value:
        print("Adaptive Ashare figure")
        df = px.data.gapminder()
        countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
        df = df[df["country"].isin(countries)]

        fig = px.area(
            df,
            x="year",
            y="gdpPercap",
            color="continent",
            line_group="country",
            title="Adaptive Ashare figure",
            labels={"gdpPercap": "GDP per Capita", "year": "Year"},
        )
        return fig

    # Adaptive - EN 16798 figure
    elif selected_model == MODELS.Adaptive_EN.value:
        print("Adaptive EN figure")
        df = px.data.gapminder()
        countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
        df = df[df["country"].isin(countries)]

        fig = px.box(
            df,
            x="continent",
            y="lifeExp",
            color="continent",
            title="Adaptive EN figure",
            labels={"lifeExp": "Life Expectancy", "continent": "Continent"},
            points="all",
        )
        return fig

    # Fans & Heat figure
    elif selected_model == MODELS.Fans_heat.value:
        print("Fans and Heat show figure")
        df = px.data.gapminder()
        countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
        df = df[df["country"].isin(countries)]

        fig = px.scatter(
            df,
            x="gdpPercap",
            y="lifeExp",
            color="continent",
            size="pop",
            hover_name="country",
            log_x=True,
            size_max=60,
            title="Fans and Heat show figure",
            labels={
                "gdpPercap": "GDP per Capita",
                "lifeExp": "Life Expectancy",
                "pop": "Population",
            },
        )

        return fig
    # PHS figure
    elif selected_model == MODELS.Phs.value:
        print("PHS show figure")
        df = px.data.gapminder()
        countries = df["country"].drop_duplicates().sample(n=10, random_state=42)
        df = df[df["country"].isin(countries)]

        fig = px.scatter(
            df,
            x="year",
            y="gdpPercap",
            size="pop",
            color="continent",
            hover_name="country",
            log_y=True,
            size_max=60,
            animation_frame="year",
            animation_group="country",
            title="PHS show figure",
            labels={"gdpPercap": "GDP per Capita", "year": "Year", "pop": "Population"},
        )
        return fig

    else:
        print("PMV_ashrae psychrometric figure")
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
