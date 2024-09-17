import base64
import io
from copy import deepcopy

#test function t_ra_PMV
from scipy.optimize import fsolve

import dash_mantine_components as dmc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pythermalcomfort.models import pmv, set_tmp, two_nodes, adaptive_ashrae
from pythermalcomfort.utilities import v_relative, clo_dynamic
from pythermalcomfort.psychrometrics import psy_ta_rh



from scipy import optimize

from components.drop_down_inline import generate_dropdown_inline
from utils.my_config_file import ElementsIDs, Models
from utils.website_text import TextHome
import matplotlib

matplotlib.use("Agg")


def chart_selector(selected_model: str):
    list_charts = deepcopy(Models[selected_model].value.charts)
    list_charts = [chart.name for chart in list_charts]
    drop_down_chart_dict = {
        "id": ElementsIDs.chart_selected.value,
        "question": TextHome.chart_selection.value,
        "options": list_charts,
        "multi": False,
        "default": list_charts[0],
    }

    return generate_dropdown_inline(
        drop_down_chart_dict, value=drop_down_chart_dict["default"], clearable=False
    )


# fig example
def t_rh_pmv(inputs: dict = None, model: str = "iso"):
    results = []
    pmv_limits = [-0.5, 0.5]
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=inputs[ElementsIDs.met_input.value]
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )

    current_tdb = inputs[ElementsIDs.t_db_input.value]
    current_rh = inputs[ElementsIDs.rh_input.value]
    print(current_rh, current_tdb)
    psy_data = psy_ta_rh(current_tdb, current_rh)

    for pmv_limit in pmv_limits:
        for rh in np.arange(0, 110, 10):
            psy_data_rh = psy_ta_rh(current_tdb, rh)

            def function(x):
                return (
                    pmv(
                        x,
                        tr=inputs[ElementsIDs.t_r_input.value],
                        vr=vr,
                        rh=rh,
                        met=inputs[ElementsIDs.met_input.value],
                        clo=clo_d,
                        wme=0,
                        standard=model,
                        limit_inputs=False,
                    )
                    - pmv_limit
                )

            temp = optimize.brentq(function, 10, 40)
            results.append(
                {
                    "rh": rh,
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )
    #####        
    df = pd.DataFrame(results)  # Convert the result to DataFrame

    # Draw a chart
    fig, axs = plt.subplots(figsize=(8, 6))
    # Initial previous_hr_values is none
    previous_hr_values = None
    previous_temp_range = None

    #left and right for the central range
    length = 2

    # Traverse relative humidity and draw corresponding lines
    for rh in np.arange(10, 110, 10):
        temp_range = np.arange(10, 40, 1)  # Temperature range
        hr_values = [psy_ta_rh(t, rh)["hr"] * 1000 for t in temp_range]  # the center of humidity ratio
        
        axs.plot(temp_range, hr_values, color="grey", linestyle="--")  # Remove label to avoid legend
        
        #fill the area based on the upper and lower curve distribution
        if previous_hr_values is not None and previous_temp_range is not None:
            # The limitation of fulfill area

            central_fill_range_min = max(current_tdb - length, temp_range[0])
            central_fill_range_max = min(current_tdb + length, temp_range[-1])
             
            fill_temp_range = np.linspace(central_fill_range_min, central_fill_range_max, 100)
            fill_hr_values_low = np.interp(fill_temp_range, previous_temp_range, previous_hr_values)
            fill_hr_values_high = np.interp(fill_temp_range, temp_range, hr_values)
    
            #The fulfilled area
            axs.fill_between(fill_temp_range, fill_hr_values_low, fill_hr_values_high, alpha=0.5, color="#7BD0F2")
            axs.fill_between(fill_temp_range, fill_hr_values_high, 0, alpha=0.2, color="#7BD0F2")

    # create new previous_hr_values for the next iteration
        previous_temp_range = temp_range
        previous_hr_values = hr_values

    axs.scatter(
        current_tdb,
        psy_data["hr"] * 1000,  #humidity ratio
        color="red", edgecolor="black", s=100  # No label is required to avoid legends
    )
    axs.set(
        ylabel="RH (%)",
        xlabel="Temperature (°C)",
        ylim=(0, 30),
        xlim=(10, 40),
    )
    axs.legend(frameon=False).remove()
    axs.grid(True, which="both", linestyle="--", linewidth=0.5)
    axs.spines["top"].set_visible(False)
    axs.spines["right"].set_visible(False)
    plt.tight_layout()

    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Heat stress chart",
        py=0,
    )


def SET_outputs_chart(inputs: dict = None, calculate_ce: bool = False, p_atmospheric: int = 101325):
    # Dry-bulb air temperature (x-axis)
    tdb_values = np.arange(10, 40, 0.5, dtype=float).tolist()

    # Prepare arrays for the outputs we want to plot
    set_temp = []  # set_tmp()
    skin_temp = []  # t_skin
    core_temp = []  # t_core
    clothing_temp = []  # t_cl
    mean_body_temp = []  # t_body
    total_skin_evaporative_heat_loss = []  # e_skin
    sweat_evaporation_skin_heat_loss = []  # e_rsw
    vapour_diffusion_skin_heat_loss = []  # e_diff
    total_skin_senesible_heat_loss = []  # q_sensible
    total_skin_heat_loss = []  # q_skin
    heat_loss_respiration = []  # q_res
    skin_wettedness = []  # w

    # Extract common input values
    tr = float(inputs[ElementsIDs.t_r_input.value])
    vr = float(
        v_relative(  # Ensure vr is scalar
            v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
        )
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=inputs[ElementsIDs.met_input.value]
    )

    current_tdb = inputs[ElementsIDs.t_db_input.value]
    current_rh = inputs[ElementsIDs.rh_input.value]
    psy_data = psy_ta_rh(current_tdb, current_rh)

    # Traverse the upper and lower limits of PMV and calculate different rh
    for pmv_limit in pmv_limits:
        for rh in np.arange(10, 110, 10):  # rh increases by 10% each time
            psy_data_rh = psy_ta_rh(current_tdb, rh)  

            # Use optimize.brentq to calculate the temperature at a given rh
            def function(x):
                return (
                        pmv(
                            x,
                            tr=inputs[ElementsIDs.t_r_input.value],
                            vr=vr,
                            rh=rh,
                            met=inputs[ElementsIDs.met_input.value],
                            clo=clo_d,
                            wme=0,
                            standard=model,
                            limit_inputs=False,
                        )
                        - pmv_limit
                )
            temp = optimize.brentq(function, 10, 40) # Find the temperature solution
            results.append(
                {
                    "rh": rh,
                    "hr": psy_data_rh['hr'] * 1000,  #Convert to g/kg
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )

    df = pd.DataFrame(results)  # Convert the result to DataFrame

    # Draw a chart
    fig, ax = plt.subplots(figsize=(8, 6))

    # Initial previous_hr_values is none
    previous_hr_values = None
    previous_temp_range = None

    #left and right for the central range
    length = 2

    # Traverse relative humidity and draw corresponding lines
    for rh in np.arange(10, 110, 10):
        temp_range = np.arange(10, 40, 1)  # Temperature range
        hr_values = [psy_ta_rh(t, rh)["hr"] * 1000 for t in temp_range]  # the center of humidity ratio
        
        ax.plot(temp_range, hr_values, color="grey", linestyle="--")  # Remove label to avoid legend
        
        #fill the area based on the upper and lower curve distribution
        if previous_hr_values is not None and previous_temp_range is not None:
            # The limitation of fulfill area

            central_fill_range_min = max(current_tdb - length, temp_range[0])
            central_fill_range_max = min(current_tdb + length, temp_range[-1])
             
            fill_temp_range = np.linspace(central_fill_range_min, central_fill_range_max, 100)
            fill_hr_values_low = np.interp(fill_temp_range, previous_temp_range, previous_hr_values)
            fill_hr_values_high = np.interp(fill_temp_range, temp_range, hr_values)
    
            #The fulfilled area
            ax.fill_between(fill_temp_range, fill_hr_values_low, fill_hr_values_high, alpha=0.5, color="#7BD0F2")
            ax.fill_between(fill_temp_range, fill_hr_values_high, 0, alpha=0.2, color="#7BD0F2")

    # create new previous_hr_values for the next iteration
        previous_temp_range = temp_range
        previous_hr_values = hr_values

    # Mark the input points
    ax.scatter(
        current_tdb,
        psy_data["hr"] * 1000,  #humidity ratio
        color="red", edgecolor="black", s=100  # No label is required to avoid legends
    )

    # Set axis labels
    ax.set_xlabel("Dry-bulb Temperature (°C)", fontsize=14)
    ax.set_ylabel("Humidity Ratio (g_water/kg_dry_air)", fontsize=14)
    ax.set_xlim(10, 40)
    ax.set_ylim(0, 30)

    #Add a comment for the current point
    label_text = (
        f"t_db: {current_tdb:.1f} °C\n"
        f"rh: {current_rh:.1f} %\n"
        f"Wa: {psy_data['hr'] * 1000:.1f} g_w/kg_da\n"
        f"twb: {psy_data['t_wb']:.1f} °C\n"
        f"tdp: {psy_data['t_dp']:.1f} °C\n"
        f"h: {psy_data['h'] / 1000:.1f} kJ/kg"
    )

    #Add annotation to the upper left corner of the figure
    ax.text(
        0.05, 0.95, label_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6)
    )

    #Adjust layout
    plt.tight_layout()

    # Save the image as base64 format
    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")

    # Return the image component
    return dmc.Image(
        src=f"data:image/png;base64,{img_base64}", alt="SET Outputs Chart", py=0

      
def pmot_ot_adaptive_ashrae(inputs: dict = None, model: str = "ashrae"):
    results = []
    pmv_limits = [-0.5, 0.5]  # PMV上下限
    
    default_met = 1.4  # default_met is 1.4 in pmv_en & pmv_ashare
    
    clo_d = clo_dynamic(
        clo=inputs[ElementsIDs.clo_input.value], met=default_met
    )
    vr = v_relative(
        v=inputs[ElementsIDs.v_input.value], met=default_met
    )
    current_tdb = inputs[ElementsIDs.t_db_input.value]
    current_rh = inputs[ElementsIDs.rh_input.value]
    psy_data = psy_ta_rh(current_tdb, current_rh)

    # Traverse the upper and lower limits of PMV and calculate different rh
    for pmv_limit in pmv_limits:
        for rh in np.arange(10, 110, 10):  # rh increases by 10% each time
            psy_data_rh = psy_ta_rh(current_tdb, rh)

            # Use optimize.brentq to calculate the temperature at a given rh
            def function(x):
                
                
                    
                return (
                            pmv(
                                x,
                                tr=inputs[ElementsIDs.t_r_input.value],
                                vr=vr,
                                rh=rh,
                                met=default_met,
                                clo=clo_d,
                                wme=0,
                                standard=model,
                                limit_inputs=False,
                            )
                            - pmv_limit
                )
                
                    # Use brentq to solve for the zero point of the function and find the appropriate temperature x
            temp = optimize.brentq(function, 10, 40)  # Find the temperature solution
            
              
            results.append(
                {
                    "rh": rh,
                    "hr": psy_data_rh['hr'] * 1000,  #Convert to g/kg
                    "temp": temp,
                    "pmv_limit": pmv_limit,
                }
            )
    
    

    df = pd.DataFrame(results)  # Convert the result to DataFrame

    # Draw a chart
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Initial previous_hr_values is none
    previous_hr_values = None
    previous_temp_range = None

    #left and right for the central range
    length = 2

    # Traverse relative humidity and draw corresponding lines
    for rh in np.arange(10, 110, 10):
        temp_range = np.arange(10, 40, 1)  # Temperature range
        hr_values = [psy_ta_rh(t, rh)["hr"] * 1000 for t in temp_range]  # the center of humidity ratio
        
        ax.plot(temp_range, hr_values, color="grey", linestyle="--")  # Remove label to avoid legend
        
        #fill the area based on the upper and lower curve distribution
        if previous_hr_values is not None and previous_temp_range is not None:
            # The limitation of fulfill area

            central_fill_range_min = max(current_tdb - length, temp_range[0])
            central_fill_range_max = min(current_tdb + length, temp_range[-1])
             
            fill_temp_range = np.linspace(central_fill_range_min, central_fill_range_max, 100)
            fill_hr_values_low = np.interp(fill_temp_range, previous_temp_range, previous_hr_values)
            fill_hr_values_high = np.interp(fill_temp_range, temp_range, hr_values)
    
            #The fulfilled area
            ax.fill_between(fill_temp_range, fill_hr_values_low, fill_hr_values_high, alpha=0.5, color="#7BD0F2")
            ax.fill_between(fill_temp_range, fill_hr_values_high, 0, alpha=0.2, color="#7BD0F2")

    # create new previous_hr_values for the next iteration
        previous_temp_range = temp_range
        previous_hr_values = hr_values

 
    # Mark the input points
    ax.scatter(
        current_tdb,
        psy_data["hr"] * 1000,  #humidity ratio
        color="red", edgecolor="black", s=100  # No label is required to avoid legends
    )

    # Set axis labels
    ax.set_xlabel("Dry-bulb Temperature (°C)", fontsize=14)
    ax.set_ylabel("Humidity Ratio (g_water/kg_dry_air)", fontsize=14)
    ax.set_xlim(10, 40)
    ax.set_ylim(0, 30)

    #Add a comment for the current point
    label_text = (
        f"t_db: {current_tdb:.1f} °C\n"
        f"rh: {current_rh:.1f} %\n"
        f"Wa: {psy_data['hr'] * 1000:.1f} g_w/kg_da\n"
        f"twb: {psy_data['t_wb']:.1f} °C\n"
        f"tdp: {psy_data['t_dp']:.1f} °C\n"
        f"h: {psy_data['h'] / 1000:.1f} kJ/kg"
    )

    #Add annotation to the upper left corner of the figure
    ax.text(
        0.05, 0.95, label_text, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=dict(facecolor='white', alpha=0.6)
    )

    #Adjust layout
    plt.tight_layout()

    # Save the image as base64 format
    my_stringIObytes = io.BytesIO()
    plt.savefig(
        my_stringIObytes,
        format="png",
        transparent=True,
        dpi=300,
        bbox_inches="tight",
        pad_inches=0,
    )
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    plt.close("all")

    # Return the image component
    return dmc.Image(
        src=f"data:image/png;base64, {my_base64_jpgData}",
        alt="Psychrometric chart",
        py=0,
    )