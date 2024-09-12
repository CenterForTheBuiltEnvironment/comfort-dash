import math
import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# 计算函数
def calculate_saturation_vapor_pressure(temp_c):
    return 610.94 * np.exp(17.625 * temp_c / (temp_c + 243.04))

def calculate_dew_point(temp_c, relative_humidity):
    saturation_vapor_pressure = calculate_saturation_vapor_pressure(temp_c)
    actual_vapor_pressure = relative_humidity / 100.0 * saturation_vapor_pressure
    dew_point = 243.04 * np.log(actual_vapor_pressure / 610.94) / (17.625 - np.log(actual_vapor_pressure / 610.94))
    return dew_point

def calculate_wet_bulb_temp(dry_bulb_temp, relative_humidity):
    epsilon = 0.0001
    wet_bulb_temp = dry_bulb_temp
    while True:
        prev_wet_bulb_temp = wet_bulb_temp
        wet_bulb_temp = dry_bulb_temp * math.atan(0.151977 * math.sqrt(relative_humidity + 8.313659)) \
                        + math.atan(dry_bulb_temp + relative_humidity) \
                        - math.atan(relative_humidity - 1.676331) \
                        + 0.00391838 * (relative_humidity ** 1.5) * math.atan(0.023101 * relative_humidity) \
                        - 4.686035
        if abs(prev_wet_bulb_temp - wet_bulb_temp) < epsilon:
            break
    return wet_bulb_temp

def calculate_absolute_humidity(dry_bulb_temp, relative_humidity):
    saturation_vapor_pressure = calculate_saturation_vapor_pressure(dry_bulb_temp)
    actual_vapor_pressure = relative_humidity / 100.0 * saturation_vapor_pressure
    absolute_humidity = 216.7 * (actual_vapor_pressure / (dry_bulb_temp + 273.15))
    return absolute_humidity

def calculate_humidity_parameters(dry_bulb_temp, relative_humidity):
    dew_point_temp = calculate_dew_point(dry_bulb_temp, relative_humidity)
    wet_bulb_temp = calculate_wet_bulb_temp(dry_bulb_temp, relative_humidity)
    absolute_humidity = calculate_absolute_humidity(dry_bulb_temp, relative_humidity)
    enthalpy = (dry_bulb_temp + relative_humidity) * 0.24  
    return {
        "Dry Bulb Temperature (°C)": dry_bulb_temp,
        "Relative Humidity (%)": relative_humidity,
        "Absolute Humidity (g/m^3)": absolute_humidity,
        "Wet Bulb Temperature (°C)": wet_bulb_temp,
        "Dew Point Temperature (°C)": dew_point_temp,
        "Enthalpy (kJ/kg)": enthalpy  
    }

def generate_vapor_pressure_chart(fixed_temperature, fixed_humidity):
    temperatures = np.linspace(10, 36, 500)
    relative_humidities = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    
    traces = []


    green_zone_1_left = 22
    green_zone_1_right = 24
    green_zone_2_left = 24
    green_zone_2_right = 26
    green_zone_3_left = 26
    green_zone_3_right = 28

    vapor_pressure_min = 0  
    vapor_pressure_max = 3000

    traces.append(go.Scatter(
        x=np.concatenate([np.array([green_zone_1_left, green_zone_1_right]), 
                          np.array([green_zone_1_right, green_zone_1_left])]),
        y=np.concatenate([np.array([vapor_pressure_max, vapor_pressure_max]), 
                          np.array([vapor_pressure_min, vapor_pressure_min])]),
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.2)',  
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False
    ))

    traces.append(go.Scatter(
        x=np.concatenate([np.array([green_zone_2_left, green_zone_2_right]), 
                          np.array([green_zone_2_right, green_zone_2_left])]),
        y=np.concatenate([np.array([vapor_pressure_max, vapor_pressure_max]), 
                          np.array([vapor_pressure_min, vapor_pressure_min])]),
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.4)',  
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False
    ))

    traces.append(go.Scatter(
        x=np.concatenate([np.array([green_zone_3_left, green_zone_3_right]), 
                          np.array([green_zone_3_right, green_zone_3_left])]),
        y=np.concatenate([np.array([vapor_pressure_max, vapor_pressure_max]), 
                          np.array([vapor_pressure_min, vapor_pressure_min])]),
        fill='toself',
        fillcolor='rgba(0, 255, 0, 0.6)',  
        line=dict(color='rgba(255,255,255,0)'),
        showlegend=False
    ))

    
    for RH in relative_humidities:
        vapor_pressures = RH / 100.0 * calculate_saturation_vapor_pressure(temperatures)
        trace = go.Scatter(
            x=temperatures,
            y=vapor_pressures,
            mode='lines',
            line=dict(color='black', width=1),
            hoverinfo='x+y',
            name=f'{RH}% RH'
        )
        traces.append(trace)

    vapor_pressure_fixed = fixed_humidity / 100.0 * calculate_saturation_vapor_pressure(fixed_temperature)
    traces.append(go.Scatter(
        x=[fixed_temperature],
        y=[vapor_pressure_fixed],
        mode='markers',
        marker=dict(color='red', size=10, symbol='circle'),
        name='Fixed Point'
    ))

    layout = go.Layout(
        title='Vapor Pressure vs. Dry Bulb Temperature for Different Relative Humidities',
        xaxis=dict(title='Dry Bulb Temperature (°C)', showgrid=False),
        yaxis=dict(title='Vapor Pressure (Pa)', showgrid=False),
        showlegend=True,
        plot_bgcolor='white'
    )
    
    fig = go.Figure(data=traces, layout=layout)

    return fig



app = Dash(__name__)

fixed_temperature = 26
fixed_humidity = 50

app.layout = html.Div([
    dcc.Graph(
        id='vapor-pressure-chart',
        figure=generate_vapor_pressure_chart(fixed_temperature, fixed_humidity),
        config={'displayModeBar': False},  
    ),
    html.Div(id='hover-data', style={'position': 'absolute', 'top': '60px', 'left': '120px', 'font-size': '14px'})
])

@app.callback(
    Output('hover-data', 'children'),
    Input('vapor-pressure-chart', 'hoverData')
)
def update_hover_text(hoverData):
    if hoverData is None:
        return 'Hover over the chart'
    
    point = hoverData['points'][0]
    temperature = point['x']
    vapor_pressure = point['y']

    params = calculate_humidity_parameters(temperature, 50)  

    hover_text = [
        html.P(f"Dry Bulb Temp: {params['Dry Bulb Temperature (°C)']:.1f}°C"),
        html.P(f"Relative Humidity: {params['Relative Humidity (%)']:.1f}%"),
        html.P(f"Absolute Humidity: {params['Absolute Humidity (g/m^3)']:.1f} g/m³"),
        html.P(f"Wet Bulb Temp: {params['Wet Bulb Temperature (°C)']:.1f}°C"),
        html.P(f"Dew Point Temp: {params['Dew Point Temperature (°C)']:.1f}°C"),
        html.P(f"Enthalpy: {params['Enthalpy (kJ/kg)']:.1f} kJ/kg")
    ]

    return hover_text

if __name__ == '__main__':
    app.run_server(debug=True)
