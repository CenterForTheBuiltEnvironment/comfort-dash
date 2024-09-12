import numpy as np
import plotly.graph_objs as go
from pythermalcomfort.models import adaptive_en

def generate_comfort_chart(tdb, tr, t_running_mean, v):
    
    x_values = np.linspace(10, 30,5) 
    
    y_values_cat_i_up = []
    y_values_cat_i_low = []
    y_values_cat_ii_up = []
    y_values_cat_ii_low = []
    y_values_cat_iii_up = []
    y_values_cat_iii_low = []

    for x in x_values:
        results = adaptive_en(tdb=tdb, tr=tr, t_running_mean=x, v=v)
        y_values_cat_i_up.append(results['tmp_cmf_cat_i_up'])
        y_values_cat_i_low.append(results['tmp_cmf_cat_i_low'])
        y_values_cat_ii_up.append(results['tmp_cmf_cat_ii_up'])
        y_values_cat_ii_low.append(results['tmp_cmf_cat_ii_low'])
        y_values_cat_iii_up.append(results['tmp_cmf_cat_iii_up'])
        y_values_cat_iii_low.append(results['tmp_cmf_cat_iii_low'])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=np.concatenate([x_values, x_values[::-1]]),
        y=np.concatenate([y_values_cat_iii_up, y_values_cat_iii_low[::-1]]),
        fill='toself',
        fillcolor='rgba(144, 238, 144, 0.3)',  
        line=dict(color='rgba(144, 238, 144, 0)', shape='linear'),  
        name='Category III',
        mode='lines'
    ))

    fig.add_trace(go.Scatter(
        x=np.concatenate([x_values, x_values[::-1]]),
        y=np.concatenate([y_values_cat_ii_up, y_values_cat_ii_low[::-1]]),
        fill='toself',
        fillcolor='rgba(34, 139, 34, 0.5)', 
        line=dict(color='rgba(34, 139, 34, 0)', shape='linear'),  
        name='Category II',
        mode='lines'
    ))
    results_current = adaptive_en(tdb=tdb, tr=tr, t_running_mean=t_running_mean, v=v)
    fig.add_trace(go.Scatter(
        x=np.concatenate([x_values, x_values[::-1]]),
        y=np.concatenate([y_values_cat_i_up, y_values_cat_i_low[::-1]]),
        fill='toself',
        fillcolor='rgba(0, 100, 0, 0.7)', 
        line=dict(color='rgba(0, 100, 0, 0)', shape='linear'),  
        name='Category I',
        mode='lines'
    ))

    results_current = adaptive_en(tdb=tdb, tr=tr, t_running_mean=t_running_mean, v=v)
    fig.add_trace(go.Scatter(
        x=[t_running_mean],
        y=[results_current['tmp_cmf']],
        mode='markers',
        marker=dict(
            color='red', 
            size=10, 
            line=dict(color='black', width=2), 
            symbol='circle'
        ),
        name=f"Current Condition: {results_current['tmp_cmf']:.1f} °C"
    ))

    fig.update_layout(
        title="Adaptive Thermal Comfort Chart - EN 16798",
        xaxis_title="Outdoor Running Mean Temperature (°C)",
        yaxis_title="Operative Temperature (°C)",
        xaxis=dict(
            range=[10, 30],
            showgrid=True, 
            gridcolor='lightgray', 
            gridwidth=1.5,  
            ticks='outside',
            ticklen=5
        ),
        yaxis=dict(
            range=[14, 36],
            showgrid=True, 
            gridcolor='lightgray', 
            gridwidth=1.5,  
            ticks='outside',
            ticklen=5
        ),
        legend=dict(x=0.8, y=1),
        plot_bgcolor='white'
    )

    return fig



