import dash_mantine_components as dmc

def create_button(label, color="blue", fullWidth=True, style=None):
    default_style = {"height": "36px", "padding": "0.8px"}
    if style:
        default_style.update(style)
    return dmc.Button(
        label,
        variant="outline",
        color=color,
        fullWidth=fullWidth,
        style=default_style,
    )

def create_custom_ensemble_button():
    return create_button("Create Custom Ensemble")

def dynamic_predictive_clothing_button():
    return create_button("Dynamic predictive clothing")

def solar_gain_on_occupants_button():
    return create_button("Solar gain on occupants")

def set_pressure_button():
    return create_button("Set pressure", fullWidth=False, style={"width": "70%"})

def si_ip_button():
    return create_button("SI/IP", fullWidth=False, style={"width": "28%"})

def local_discomfort_button():
    return create_button("Local discomfort")

def reset_button():
    return create_button("Reset", fullWidth=False, style={"width": "25%"})

def save_button():
    return create_button("Save", color="green", fullWidth=False, style={"width": "25%"})

def reload_button():
    return create_button("Reload", color="yellow", fullWidth=False, style={"width": "25%"})

def share_button():
    return create_button("Share", color="violet", fullWidth=False, style={"width": "25%"})

def documentation_button():
    return create_button("Documentation", color="gray")

def globe_temp_button():
    return create_button("Globe temp")

def pmv_ashrae_bottom_buttons():
    return dmc.Stack([
        create_custom_ensemble_button(),
        dynamic_predictive_clothing_button(),
        solar_gain_on_occupants_button(),
        dmc.Group([set_pressure_button(), si_ip_button()], gap="xs", grow=True),
        local_discomfort_button(),
        dmc.Group([reset_button(), save_button(), reload_button(), share_button()],
                  gap="xs", grow=True, style={"width": "100%"}),
        documentation_button()
    ], gap="xs")

def adaptive_ashrae_bottom_button():
    return dmc.Stack([
        dmc.Group([set_pressure_button(), si_ip_button()], grow=True, gap="xs"),
        local_discomfort_button(),
        dmc.Group([reset_button(), save_button(), reload_button(), share_button()],
                  grow=True, gap="xs", style={"width": "100%"}),
        documentation_button()
    ], gap="xs")

def pmv_en_bottom_button():
    return dmc.Stack([
        create_custom_ensemble_button(),
        dmc.Group([
            reset_button(),
            set_pressure_button(),
            si_ip_button()
        ], grow=True, gap="xs"),
        dmc.Group([
            local_discomfort_button(),
            globe_temp_button()
        ], grow=True, gap="xs"),
        documentation_button()
    ], gap="xs")

def adaptive_en_bottom_button():
    return dmc.Stack([
        dmc.Group([
            reset_button(),
            set_pressure_button(),
            si_ip_button()
        ], grow=True, gap="xs"),
        dmc.Group([
            local_discomfort_button(),
            globe_temp_button()
        ], grow=True, gap="xs"),
        documentation_button()
    ], gap="xs")

def fans_heat_phs_bottom_button():
    return dmc.Stack([
        dmc.Group([
            reset_button(),
            set_pressure_button(),
            si_ip_button()
        ], grow=True, gap="xs"),
        dmc.Group([
            local_discomfort_button(),
            globe_temp_button()
        ], grow=True, gap="xs"),
        documentation_button()
    ], gap="xs")