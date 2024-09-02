from pythermalcomfort.models import adaptive_ashrae


def calculate_adaptive_ashrae(tdb, tr, t_running_mean, v):

    results = adaptive_ashrae(tdb = tdb, tr= tr, t_running_mean= t_running_mean, v= v)
    # acceptability_limits_80 = results.acceptability_80
    # acceptability_limits_90 = results.acceptability_90
    # return acceptability_limits_80, acceptability_limits_90

    tmp_cmf = results['tmp_cmf']
    tmp_cmf_80_low = results['tmp_cmf_80_low']
    tmp_cmf_80_up = results['tmp_cmf_80_up']
    tmp_cmf_90_low = results['tmp_cmf_90_low']
    tmp_cmf_90_up = results['tmp_cmf_90_up']
    acceptability_80 = results['acceptability_80']
    acceptability_90 = results['acceptability_90']

    return tmp_cmf, tmp_cmf_80_low, tmp_cmf_80_up, tmp_cmf_90_low, tmp_cmf_90_up, acceptability_80, acceptability_90