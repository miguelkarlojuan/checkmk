# Perf-O-Meters for Check_MK's checks
#
# They are called with:
# 1. row -> a dictionary of the data row with at least the
#    keys "service_perf_data", "service_state" and "service_check_command"
# 2. The check command (might be extracted from the performance data
#    in a PNP-like manner, e.g if perfdata is "value=10.5;0;100.0;20;30 [check_disk]
# 3. The parsed performance data as a list of 7-tuples of
#    (varname, value, unit, warn, crit, min, max)

def perfometer_check_mk_df(row, check_command, perf_data):
    h = '<table><tr>'
    varname, value, unit, warn, crit, minn, maxx = perf_data[0]
    perc_used = 100 * (float(value) / float(maxx))
    perc_free = 100 - float(perc_used)
    color = { 0: "#0f8", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    h += perfometer_td(perc_used, color)
    h += perfometer_td(perc_free, "white")
    h += "</tr></table>"
    # return "%d%% of %.1fGB used" % (perc_used, float(value)/1024.0), h
    return "%d%%" % perc_used, h
    return "%d%% used" % perc_used, h

perfometers["check_mk-df"] = perfometer_check_mk_df
perfometers["check_mk-vms_df"] = perfometer_check_mk_df
perfometers["check_disk"] = perfometer_check_mk_df


def perfometer_check_mk_kernel_util(row, check_command, perf_data):
    h = '<table><tr>'
    h += perfometer_td(perf_data[0][1], "#f60")
    h += perfometer_td(perf_data[1][1], "#6f2")
    h += perfometer_td(perf_data[2][1], "#0bc")
    total = sum([float(p[1]) for p in perf_data])
    h += perfometer_td(100.0 - total, "white")
    h += "</tr></table>"
    return "%d%%" % total, h

perfometers["check_mk-kernel.util"] = perfometer_check_mk_kernel_util
perfometers["check_mk-vms_sys.util"] = perfometer_check_mk_kernel_util

def perfometer_check_mk_mem_used(row, check_command, perf_data):
    h = '<table><tr>'
    ram_total = float(perf_data[0][6])
    swap_total = float(perf_data[1][6])
    virt_total = ram_total + swap_total
    ram_used = float(perf_data[0][1])
    swap_used = float(perf_data[1][1])
    virt_used = ram_used + swap_used
    state = row["service_state"]
    ram_color, swap_color = { 0: ("#80ff40", "#008030"), 1: ("#ff2", "#dd0"), 2:("#f44", "#d00"), 3:("#fa2", "#d80") }[state]
    h += perfometer_td(100 * ram_used / virt_total, ram_color)
    h += perfometer_td(100 * swap_used / virt_total, swap_color)
    if virt_used < ram_total:
        h += perfometer_td(100 * (ram_total - virt_used) / virt_total, "#ccf")
        h += perfometer_td(100 * (virt_total - ram_total) / virt_total, "#fff")
    else:
        h += perfometer_td(100 * (virt_total - virt_used), "#fff")
    h += "</tr></table>"
    return "%d%%" % (100 * (virt_used / ram_total)), h

perfometers["check_mk-mem.used"] = perfometer_check_mk_mem_used

# def perfometer_check_mk_kernel(row, check_command, perf_data):
#     return "%d/s" % int(perf_data[0][1]), perfometer_logarithmic(perf_data[0][1], 1000, 10, "#f2a")
# 
# perfometers["check_mk-kernel"] = perfometer_check_mk_kernel

def perfometer_check_mk_cpu_threads(row, check_command, perf_data):
    color = { 0: "#a4f", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    return "%d" % int(perf_data[0][1]), perfometer_logarithmic(perf_data[0][1], 400, 2, color)

perfometers["check_mk-cpu.threads"] = perfometer_check_mk_cpu_threads


def perfometer_check_mk_cpu_loads(row, check_command, perf_data):
    color = { 0: "#68f", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    load = float(perf_data[0][1]) 
    return "%.1f" % load, perfometer_logarithmic(load, 4, 2, color)


perfometers["check_mk-cpu.loads"] = perfometer_check_mk_cpu_loads
