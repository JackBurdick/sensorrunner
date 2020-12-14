from collections import Counter


def average_dict(v_dicts):
    # filter values with None
    for k_d, v_d in v_dicts.items():
        if v_d:
            v_dicts[k_d] = {k: v for k, v in v_d.items() if v is not None}

    # calculate average
    occurrence, sums = Counter(), Counter()
    for n, sensor_ret_d in v_dicts.items():
        sums.update(sensor_ret_d)
        occurrence.update(sensor_ret_d.keys())

    avg_res = {x: float(sums[x]) / occurrence[x] for x in sums.keys()}
    return avg_res