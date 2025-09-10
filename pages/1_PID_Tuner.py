import streamlit as st
import numpy as np
import pandas as pd
import os
import datetime
from utils import PID_Object


def custom_slider(label, min_value, max_value, step=0.1, default=None):
    """
    Custom slider with manual input field, synced immediately,
    and auto-reset when min/max/default change (e.g. after new file load).
    """
    state_key = f"{label}_val"
    meta_key = f"{label}_meta"

    if default is None:
        default = min_value

    if (
        state_key not in st.session_state
        or meta_key not in st.session_state
        or st.session_state[meta_key] != (min_value, max_value, default)
    ):
        st.session_state[state_key] = default
        st.session_state[meta_key] = (min_value, max_value, default)

    def update_from_slider():
        st.session_state[state_key] = st.session_state[f"{label}_slider"]

    def update_from_number():
        st.session_state[state_key] = st.session_state[f"{label}_number"]

    col1, col2 = st.columns([3, 1])

    with col1:
        st.slider(
            label,
            min_value=min_value,
            max_value=max_value,
            step=step,
            key=f"{label}_slider",
            value=st.session_state[state_key],
            on_change=update_from_slider
        )

    with col2:
        st.number_input(
            " ",
            min_value=min_value,
            max_value=max_value,
            step=step,
            key=f"{label}_number",
            value=st.session_state[state_key],
            on_change=update_from_number
        )

    return st.session_state[state_key]


def get_data(file_name, separator, decimal_sep, header_row, skip_rows, skip_columns, dateparse):
    if skip_rows | skip_columns:
        ncols = len(pd.read_csv(file_name, sep=separator, decimal=decimal_sep, nrows=1).columns)
        if dateparse:
            return pd.read_csv(file_name,
                               sep=separator,
                               decimal=decimal_sep,
                               header=header_row,
                               index_col=0,
                               usecols=range(skip_columns, ncols),
                               skiprows=range(header_row + 1, header_row + skip_rows + 1),
                               parse_dates=['datetime'],
                               date_parser=dateparse
                               )
        else:
            return pd.read_csv(file_name,
                               sep=separator,
                               decimal=decimal_sep,
                               header=header_row,
                               usecols=range(skip_columns, ncols),
                               skiprows=range(header_row + 1, header_row + skip_rows + 1)
                               )
    else:
        return pd.read_csv(file_name,
                           sep=separator,
                           decimal=decimal_sep,
                           header=header_row,
                           index_col=0
                           )


st.set_page_config(
    page_title="PID Tuner",
)

st.write("# PID Tuner")
st.write("## Data Loading")

if st.checkbox("My file more than 200 Mb"):  # Check .csv files in root directory
    st.write("Upload your file in root directory")
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    file_name = st.selectbox("Choose data file", csv_files, index=None)
    st.write("*Press 'R' to update file list*")
else:
    try:
        file_name = st.file_uploader("Upload your .csv data file").name
        if not file_name.endswith(".csv"):
            raise ValueError
    except AttributeError:
        st.error("Select new file")
        st.stop()
    except ValueError:
        st.error("Select correct file extension (.csv)")
        st.stop()

if file_name is None:
    st.stop()

header_row = 0
skip_rows = 0
skip_columns = 0
date_format = "%d.%m.%Y %H:%M:%S"

col1, col2, col3 = st.columns(3)
with col1:
    separator = st.radio(
        "Column separator",
        [";",
         ",",
         ".",
         "  "],
        captions=["semicolon",
                  "comma",
                  "dot",
                  "tab"],
    )
with col2:
    decimal_sep = st.radio(
        "Decimal separator",
        [",",
         "."]
    )
with col3:
    header_row = st.number_input("Header is in row", min_value=0, step=1)
    if st.checkbox("Skip rows/columns"):
        skip_rows = st.number_input("Rows to skip", min_value=0, step=1)
        skip_columns = st.number_input("Columns to skip", min_value=0, step=1)
date_format = st.selectbox("Datetime format:",
                           ["%d.%m.%Y %H:%M:%S",
                            "%m.%d.%Y %H:%M:%S"]
                           )
try:
    if st.checkbox('No "datetime" column'):
        data = get_data(file_name, separator, decimal_sep, header_row, skip_rows, skip_columns, None)
        col1, col2, col3 = st.columns(3)
        with col1:
            freq = st.number_input("Set time interval (s)", step=1, min_value=1)
        with col2:
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            date = st.date_input("Set date", value="today")
        with col3:
            time = st.time_input("Set time", value="now", step=60)
            dt = datetime.datetime.combine(date, time)
            start = pd.Timestamp(dt)
            freq_s = str(freq) + "s"
            dt_index = pd.date_range(start=start, periods=len(data), freq=freq_s)
            ser = pd.Series(dt_index)
            data.index = ser
        if st.checkbox('Data preview'):
            st.dataframe(data.head())
    else:
        dateparse = lambda x: datetime.datetime.strptime(x, date_format)
        data = get_data(file_name, separator, decimal_sep, header_row, skip_rows, skip_columns, dateparse)
        freq = int((pd.Timestamp(data.index[1]) - pd.Timestamp(data.index[0])).total_seconds())
        start = data.index[0]
        if st.checkbox('Data preview'):
            st.dataframe(data.head())
except pd._libs.tslibs.parsing.DateParseError:
    if st.checkbox('Data preview'):
        st.dataframe(data.head())
    st.error("Check Header row")
    st.stop()
except ValueError:
    try:
        if st.checkbox('Data preview'):
            st.dataframe(data.head())
    except NameError:
        st.error("Check Data or choose 'No Datetime Column'")
        st.stop()
    st.error("Check Datetime or choose 'No Datetime Column'")
    st.stop()
except NameError:
    st.error("Data error")
    st.stop()


st.write("## Model Fitting")
try:
    manipulated_variable = st.selectbox("Choose manipulated variable (MV)", list(data.columns))
    process_variable = st.selectbox("Choose process variable (PV)", list(data.columns))
    if str(data[manipulated_variable][0]).lower() in ["none", "nan"] or str(data[process_variable][0]).lower() in \
            ["none", "nan"]:
        raise ValueError
    if st.checkbox("Show linechart"):
        st.line_chart(data=data, x=None, y=[process_variable, manipulated_variable], color=["#f00", "#00f"])
    order = st.selectbox(
        "Choose model", ["1st Order",
                         "2nd Order T1 != T2"]
    )

    t = list(range(0, len(data)*freq, freq))
    if not order:
        st.error("Please select model.")
    elif order == "1st Order":
        dx_cur = (max(data[manipulated_variable]) - min(data[manipulated_variable])) * 1.0
        dx = custom_slider('ΔMV', min(data[manipulated_variable]) - dx_cur, max(data[manipulated_variable]) + dx_cur,
                            default=dx_cur)

        k_ob_cur = (max(data[process_variable]) - min(data[process_variable])) * 1.0 / dx
        k_ob = custom_slider('Kob', min(data[process_variable]) - k_ob_cur,
                         max(data[process_variable]) + k_ob_cur,
                         default=k_ob_cur)

        mv_start = data[data[manipulated_variable].diff() >= 0.5 * dx].index[0]
        pv_start = data[data[process_variable].diff() >= (max(data[process_variable]) - min(data[process_variable]))
                        * 0.1].index[0]

        tau_ob_cur = int((pv_start - mv_start).total_seconds())
        tau_ob = custom_slider('τob', 0, tau_ob_cur * 3, step=1, default=tau_ob_cur)

        tob_1_cur = int((data[data[process_variable] >= 0.632 *
                              max(data[process_variable])].index[0] - pv_start).total_seconds())

        t1_ob = custom_slider('Tob', 0, 3 * tob_1_cur, step=1, default=tob_1_cur)

        obj = PID_Object(order, k_ob, tau_ob, t1_ob)

        first_order = lambda i: k_ob * (1 - np.exp(-(i - tau_ob) / t1_ob)) * dx
        y = [first_order(i) + min(data[process_variable]) if i >= tau_ob else 0 + min(data[process_variable]) for i in t]
    elif order == "2nd Order T1 != T2":
        dx_cur = (max(data[manipulated_variable]) - min(data[manipulated_variable])) * 1.0
        dx = custom_slider('ΔMV', min(data[manipulated_variable]) - dx_cur, max(data[manipulated_variable]) + dx_cur,
                       default=dx_cur)

        k_ob_cur = (max(data[process_variable]) - min(data[process_variable])) * 1.0 / dx
        k_ob = custom_slider('Kob', min(data[process_variable]) - k_ob_cur,
                         max(data[process_variable]) + k_ob_cur,
                         default=k_ob_cur)

        mv_start = data[data[manipulated_variable].diff() >= 0.5 * dx].index[0]
        pv_start = data[data[process_variable].diff() >= (max(data[process_variable]) - min(data[process_variable]))
                        * 0.1].index[0]

        tau_ob_cur = int((pv_start - mv_start).total_seconds())
        tau_ob = custom_slider('τob', 0, tau_ob_cur * 3, default=tau_ob_cur, step=1)

        tob_1_cur = int((data[data[process_variable] >= 0.632 *
                              max(data[process_variable])].index[0] - pv_start).total_seconds())

        t1_ob = custom_slider('T1ob', 1, 3 * tob_1_cur, default=tob_1_cur, step=1)
        try:
            t2_ob = custom_slider('T2ob', 1, 3 * tob_1_cur, default=tob_1_cur + 1, step=1)
            if t2_ob == t1_ob:
                raise ValueError
        except ValueError:
            st.error("T1ob must be not equal T2ob")
            st.stop()

        obj = PID_Object(order, round(k_ob, 4), tau_ob, t1_ob, t2_ob)

        second_order = lambda i: k_ob * (1 - max(t1_ob, t2_ob) / (max(t1_ob, t2_ob) - min(t1_ob, t2_ob)) * \
                                         np.exp(-(i - tau_ob) / max(t1_ob, t2_ob)) + min(t1_ob, t2_ob) /
                                         (max(t1_ob, t2_ob) - min(t1_ob, t2_ob)) * np.exp
                                         (-(i - tau_ob) / min(t1_ob, t2_ob))) * dx

        y = [second_order(i) + min(data[process_variable]) if i >= tau_ob else 0 + min(data[process_variable]) for i in t]
    elif order == "2nd Order T1 = T2":

        dx_cur = (max(data[manipulated_variable]) - min(data[manipulated_variable])) * 1.0
        dx = custom_slider('ΔMV', min(data[manipulated_variable]) - dx_cur, max(data[manipulated_variable]) + dx_cur,
                       default=dx_cur)

        k_ob_cur = (max(data[process_variable]) - min(data[process_variable])) * 1.0 / dx
        k_ob = custom_slider('Kob', min(data[process_variable]) - k_ob_cur,
                         max(data[process_variable]) + k_ob_cur,
                         default=k_ob_cur)

        mv_start = data[data[manipulated_variable].diff() >= 0.5 * dx].index[0]
        pv_start = data[data[process_variable].diff() >= (max(data[process_variable]) - min(data[process_variable]))
                        * 0.1].index[0]

        tau_ob_cur = int((pv_start - mv_start).total_seconds())
        tau_ob = custom_slider('τob', 0, tau_ob_cur * 3, default=tau_ob_cur, step=1)

        tob_1_cur = int((data[data[process_variable] >= 0.632 *
                              max(data[process_variable])].index[0] - pv_start).total_seconds())

        t1_ob = custom_slider('Tob', 1, 3 * tob_1_cur, default=tob_1_cur, step=1)
        t2_ob = t1_ob

        obj = PID_Object(order, k_ob, tau_ob, t1_ob, t2_ob)

        second_order_2 = lambda i: k_ob * (1 - np.exp(-(i - tau_ob) / t1_ob) * (1 + (i - tau_ob) / t1_ob)) * dx
        y = [second_order_2(i) + min(data[process_variable]) if i >= tau_ob else 0 + min(data[process_variable]) for i in t]

    if not order:
        st.stop()
    else:
        x = [dx if x >= 0 else 0 for x in t]
        t = pd.to_timedelta(t, unit='s')
        arr = pd.DataFrame({'ΔMV': x,
                            'model': y},
                           index=(t + start)
                           )

    data = pd.concat([arr, data], axis=1)

    st.line_chart(data=data,
                  x=None,
                  y=[process_variable, manipulated_variable, 'model'],
                  color=["#f00", "#00f", "#0f0"])

    st.write("## Object Parameters")
    if order == "1st Order":
        obj.t2_ob = None
        st.markdown(
            f"<h1 style='font-size: 24px;'>K = {round(obj.k_ob, 4)} <br> τ = {obj.tau_ob} <br> T = {obj.t1_ob}",
            unsafe_allow_html=True)

    elif order == "2nd Order T1 != T2" or order == "2nd Order T1 = T2":
        st.markdown(f"<h1 style='font-size: 24px;'>K = {round(obj.k_ob, 4)} <br> τ = {obj.tau_ob} <br> T<sub>1</sub> = \
{obj.t1_ob}"
                    f"<br>T<sub>2</sub> = {obj.t2_ob}</h1>", unsafe_allow_html=True)

    st.write("## PID Tuning")

    if st.selectbox("Choose PID type", ["PI", "PID"]) == "PI":
        obj.pid = 0
        obj.d_pid = None
        if obj.order == "1st Order":
            obj.method = st.selectbox("Choose PID method", ["Optimal Modulus method",
                                                            "Aperiodic Stability Method",
                                                            "Coon Method",
                                                            "Kopelovich Method",
                                                            "Kopelovich-Sharkov Method",
                                                            "Skogestads Method",
                                                            "Lambda Method",
                                                            "AMIGO Method",
                                                            "Ziegler-Nichols Method",
                                                            "Max Stability Method"])
        elif obj.order == "2nd Order T1 != T2":
            obj.method = st.selectbox("Choose PID method", ["Optimal Modulus method",
                                                            "Huang Method"])
    else:
        obj.pid = 1
        if obj.order == "1st Order":
            obj.method = st.selectbox("Choose PID method", ["Optimal Modulus method",
                                                            "Aperiodic Stability Method",
                                                            "Coon Method",
                                                            "Kopelovich Method",
                                                            "Kopelovich-Sharkov Method",
                                                            "Lambda Method",
                                                            "AMIGO Method",
                                                            "Ziegler-Nichols Method",
                                                            "Max Stability Method"])
        elif obj.order == "2nd Order T1 != T2":
            obj.method = st.selectbox("Choose PID method", ["Optimal Modulus method",
                                                            "Huang Method",
                                                            "Skogestads Method"])
    if obj.method == "Coon Method":
        col1, col2 = st.columns(2)
        with col1:
            overshoot = st.selectbox("Choose process type", ["Aperiodic process",
                                                             "20% overshoot process"])
            if overshoot == "Aperiodic process":
                obj.overshoot = 0
            else:
                obj.overshoot = 1
        with col2:
            disturbance = st.selectbox("Choose disturbance type", ["Setpoint disturbance",
                                                                   "Load disturbance"])
            if disturbance == "Setpoint disturbance":
                obj.disturbance = 0
            else:
                obj.disturbance = 1
    elif obj.method in ["Kopelovich Method", "Kopelovich-Sharkov Method"]:
        overshoot = st.selectbox("Choose process type", ["Aperiodic process",
                                                         "20% overshoot process",
                                                         "Minimum I2 process"])
        if overshoot == "Aperiodic process":
            obj.overshoot = 0
        elif overshoot == "20% overshoot process":
            obj.overshoot = 1
        else:
            obj.overshoot = 2
    elif obj.method == "Lambda Method":
        # st.write(obj)
        obj.lamb = custom_slider('Lambda1', 1.0, 3.0, default=3.0, step=0.1)

    obj.calculate_pid()

    pid_form = st.selectbox(
        "Choose PID form", ["Standard form (Siemens, Honeywell, Emerson, ABB)",
                            "Yokogawa CENTUM VP/CS3000",
                            "Parallel form"
                            ]
    )
    if pid_form == "Standard form (Siemens, Honeywell, Emerson, ABB)":
        if obj.pid == 0:
            st.latex(r"MV(t) = P \left( e(t) + \frac{1}{I}\int e(t)\,dt\right)")
            st.markdown(
                f"<h1 style='font-size: 24px;'>P = {round(obj.p_pid, 4)} <br> I [s] = {round(obj.i_pid, 4)}",
                unsafe_allow_html=True)
        elif obj.pid == 1:
            st.latex(r"MV(t) = P \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \cdot \frac{de(t)}{dt} \right)")
            st.markdown(
                f"<h1 style='font-size: 24px;'>P = {round(obj.p_pid, 4)} <br> I [s] = {round(obj.i_pid, 4)} <br> D [s] \
                = {round(obj.d_pid, 4)}", unsafe_allow_html=True)

    elif pid_form == "Parallel form":
        if obj.pid == 0:
            st.latex(r"u(t) = MV(t) = K_p e(t) + K_i \int_0^t e(t)\, dt")
            st.markdown(
                f"<h1 style='font-size: 24px;'>Kp = {round(obj.p_pid, 4)} <br> Ki [1/s] =\
{round(obj.i_pid * obj.p_pid, 4)}",
                unsafe_allow_html=True)
        elif obj.pid == 1:
            st.latex(r"u(t) = MV(t) = K_p e(t) + K_i \int_0^t e(t)\, dt + K_d \frac{de(t)}{dt}")
            st.markdown(
                f"<h1 style='font-size: 24px;'>Kp = {round(obj.p_pid, 4)} <br> Ki [1/s] = \
{round(obj.i_pid * obj.p_pid, 4)} <br> Kd [s] = {round(obj.d_pid * obj.d_pid, 4)}", unsafe_allow_html=True)
    elif pid_form == "Yokogawa CENTUM VP/CS3000":
        if obj.pid == 0:
            st.latex(r"MV(t) = \frac{100}{P} \left( e(t) + \frac{1}{I}\int e(t)\,dt\right)")
            st.markdown(
                f"<h1 style='font-size: 24px;'>P = {round(100 / obj.p_pid, 4)} <br> I [s] = {round(obj.i_pid, 4)}",
                unsafe_allow_html=True)
        elif obj.pid == 1:
            st.latex(r"MV(t) = \frac{100}{P} \left( e(t) + \frac{1}{I}\int e(t)\,dt + D \cdot \frac{de(t)}{dt} \right)")
            st.markdown(
                f"<h1 style='font-size: 24px;'>P = {round(100 / obj.p_pid, 4)} <br> I [s] = {round(obj.i_pid, 4)} <br> \
                D [s] = {round(obj.d_pid, 4)}", unsafe_allow_html=True)

except st.elements.lib.built_in_chart_utils.StreamlitColumnNotFoundError:
    st.error("Data doesn't have such a column")
except ValueError:
    st.error("Check header line or skip rows")
except IndexError:
    st.error("Check MV or PV. Make sure you chose the right column")
except TypeError:
    st.error("Check separators")

st.markdown("""
# Disclaimer
This software is provided "as is" for educational and informational purposes only.
The author makes no representations or warranties of any kind, express or implied, regarding the accuracy, reliability, 
or suitability of the PID tuning parameters or recommendations generated by this application.
Any use of this software, including applying its output to real-world systems or processes, is at your own risk.
The author shall not be held liable for any direct, indirect, incidental, or consequential damages, losses, or costs 
resulting from the use, misuse, or inability to use this software or its recommendations.""")

st.markdown("### Created by [NosterDream](https://github.com/nosterdream)")
