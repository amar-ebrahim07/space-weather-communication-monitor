import streamlit as st
import analysis
import datetime
import pandas as pd
import calendar
import plotly.graph_objects as go
import signals
import attenuation
import matplotlib.pyplot as plt
import noise
import numpy as np


st.title("🛰️ Space Weather & Communication Monitor", text_alignment="left")
st.subheader("Potential Communications Impact Assessment")
st.write("----------------")
col1, col2 = st.columns(2)

with col1:
    if st.button("Live Mode", width="stretch"):
        st.session_state.mode = "live"

with col2:
    if st.button("Simulation Mode", width="stretch"):
        st.session_state.mode = "simulation"


if "mode" not in st.session_state:
    st.session_state.mode = "home"



if st.session_state.mode == "live":
    today = datetime.date.today().isoformat()
    date_range = pd.date_range(start="2026-08-01", end="2026-08-07", freq="D")

    flr = analysis.make_df(1, "2016-1-1", "2016-1-2")
    cme = analysis.make_df(2, today, today)
    gst = analysis.make_df(3, today, today)

    flr = analysis.clean_df(flr)
    cme = analysis.clean_df(cme)
    gst = analysis.clean_df(gst)

    st.header("Select Date:")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        year = st.selectbox("", range(2016, datetime.datetime.now().year + 1) )

    with col2:
        month = st.selectbox("", range(1, 13))
        month = f"{month:02d}"

    with col3:
        __, max = calendar.monthrange(int(year), int(month))
        day = st.selectbox("", range(1, max+1))
        day = f"{day:02d}"

    date = f"{year}-{month}-{day}"
    with col4:
        st.write("")    
        st.write("")
        flag = False
        if st.button("Analyze"):
            flr = analysis.make_df(1, date, date)
            cme = analysis.make_df(2, date, date)
            gst = analysis.make_df(3, date, date)

            flr = analysis.clean_df(flr)
            cme = analysis.clean_df(cme)
            gst = analysis.clean_df(gst)
            data = analysis.riskanalysis(flr, cme, gst)
            flag = True
            
    if flag:
        st.write("----------------------------------------")
        st.markdown(f"<h2 style='text-align: center;'>Potential Communications Impact</h2>", unsafe_allow_html=True)


        st.markdown(f"<h2 style='text-align: center;'><-- {data[5].upper()} --></h2>", unsafe_allow_html=True)


        st.markdown(f"<h3 style='text-align: center;'>Based on available space-weather observations</h3>", unsafe_allow_html=True)

        st.write("-------------------")

        col1, col2, col3 = st.columns(3, border=True)

        with col1:
            st.subheader("☀️ Strongest Flare", text_alignment="center")
            st.write("")
            st.subheader(data[0], text_alignment="center")
            st.subheader(data[3], text_alignment=("center"))
        with col2:
            st.subheader("☄️ Fastest CME",text_alignment="center")
            st.write("")
            st.write("")
            st.subheader(f"{data[1]} km/s", text_alignment="center")
            st.subheader("Informational", text_alignment="center")
        with col3:
            st.subheader("🧲 Maximum KP", text_alignment="center")
            st.write("")
            st.write("")
            st.subheader(data[2], text_alignment="center")
            st.subheader(data[4], text_alignment=("center"))

        st.write("----------------------")

        st.header("📊Event Activity")
        col1, col2, col3 = st.columns(3)


        with col1:
            st.subheader("FLARES", text_alignment="center")
            st.write("")
            st.write("")
            st.subheader(data[6], text_alignment="center")

        with col2:
            st.subheader("CMEs", text_alignment="center")
            st.write("")
            st.write("")
            st.subheader(data[7], text_alignment="center")
        with col3:
            st.subheader("GEOMAGNETIC STORMS", text_alignment="center")
            st.subheader(data[8], text_alignment="center")

        st.write("-------------------")

        days, flare_counts, cme_counts, gst_counts = analysis.monthly_event_counts(date)

        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                x=days,
                y=flare_counts,
                name="Solar Flares"
            )
        )

        fig.add_trace(
            go.Bar(
                x=days,
                y=cme_counts,
                name="CMEs"
            )
        )

        fig.add_trace(
            go.Bar(
                x=days,
                y=gst_counts,
                name="Geomagnetic Storms"
            )
        )

        fig.update_layout(
            xaxis_title="Day",
            yaxis_title="Number of Events",
            barmode="group"
        )

        st.plotly_chart(fig, use_container_width=True)


if st.session_state.mode == "simulation":
    st.subheader("Space Event Simulator")
    st.write("Simulate different space-weather conditions to explore how changes in solar activity and geomagnetic activity can affect the estimated communication risk.")
    st.write("")
    st.write("The R-scale measures the severity of solar radio blackouts caused by solar flares, while the G-scale measures the severity of geomagnetic storms caused by disturbances in Earth's magnetic field. Higher levels indicate stronger space-weather activity and greater potential impacts on communications.")

    flr_selector = st.select_slider("Solar Flare", ["R0", "R1", "R2", "R3", "R4", "R5"])
    gst_selector =  st.select_slider("Geomagnetic Storm", ["G0", "G1", "G2", "G3", "G4", "G5"])
    frequency = st.slider("Frequency (Hz)", 1, 10000)

    time = signals.generate_time(0.02, 100000)
    signal = signals.generate_sine(time, 0.4, frequency, 0)

    R = int(flr_selector[1])
    G = int(gst_selector[1])

    fading_frequency = {
        0: {0: 0.00, 1: 0.08, 2: 0.12, 3: 0.16, 4: 0.20, 5: 0.25},
        1: {0: 0.08, 1: 0.12, 2: 0.16, 3: 0.20, 4: 0.25, 5: 0.30},
        2: {0: 0.12, 1: 0.16, 2: 0.20, 3: 0.25, 4: 0.30, 5: 0.40},
        3: {0: 0.16, 1: 0.20, 2: 0.25, 3: 0.30, 4: 0.40, 5: 0.50},
        4: {0: 0.20, 1: 0.25, 2: 0.30, 3: 0.40, 4: 0.50, 5: 0.60},
        5: {0: 0.25, 1: 0.30, 2: 0.40, 3: 0.50, 4: 0.60, 5: 0.75}
    }


    fade_freq = fading_frequency[R][G]

    noise_variation = {
        0: {0: 0.00, 1: 0.01, 2: 0.02, 3: 0.03, 4: 0.04, 5: 0.05},
        1: {0: 0.01, 1: 0.02, 2: 0.025, 3: 0.03, 4: 0.035, 5: 0.04},
        2: {0: 0.02, 1: 0.025, 2: 0.03, 3: 0.035, 4: 0.04, 5: 0.05},
        3: {0: 0.03, 1: 0.03, 2: 0.035, 3: 0.04, 4: 0.05, 5: 0.06},
        4: {0: 0.04, 1: 0.035, 2: 0.04, 3: 0.05, 4: 0.06, 5: 0.07},
        5: {0: 0.05, 1: 0.04, 2: 0.05, 3: 0.06, 4: 0.07, 5: 0.08}
    }

    noise_std = noise_variation[R][G]
    signal = noise.add_noise(signal, noise_std)[0]


    blackout_probability_mat = {
    0: {0: 0.00, 1: 0.02, 2: 0.04, 3: 0.06, 4: 0.08, 5: 0.10},
    1: {0: 0.05, 1: 0.07, 2: 0.09, 3: 0.11, 4: 0.13, 5: 0.15},
    2: {0: 0.10, 1: 0.12, 2: 0.14, 3: 0.16, 4: 0.18, 5: 0.20},
    3: {0: 0.20, 1: 0.22, 2: 0.25, 3: 0.28, 4: 0.30, 5: 0.35},
    4: {0: 0.35, 1: 0.38, 2: 0.40, 3: 0.43, 4: 0.45, 5: 0.50},
    5: {0: 0.50, 1: 0.53, 2: 0.55, 3: 0.58, 4: 0.60, 5: 0.65}
    }


    signal = attenuation.attenuate(signal, time, fade_freq)

    blackout_signal = signal.copy()


    blackout_probability = blackout_probability_mat[R][G]
    max_duration = 0.005

    if np.random.random() < blackout_probability:

        start = np.random.uniform(0.1, 0.8)
        duration = np.random.uniform(0.02, max_duration)

        start_index = int(start * len(time))
        end_index = int((start + duration) * len(time))

        blackout_signal[start_index:end_index] = 0

        signal = blackout_signal


    fig, ax = plt.subplots()
    ax.plot(time, signal)
    ax.set_xlim(0,0.02)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Simulator")
    ax.grid(True)
    st.pyplot(fig)

    st.write("------------------")
    st.subheader("Illustrative Simulator")
    
    if "flare" not in st.session_state:
        st.session_state.flare = False

    if "signal" not in st.session_state:
        st.session_state.signal = False


    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Send Signal", width="stretch"):
            st.session_state.signal = True

    with col2:
        if st.button("Add Flares", width="stretch"):
            st.session_state.flare = True

    with col3:
        if st.button("Reset", width="stretch"):
            st.session_state.flare = False
            st.session_state.signal = False


    if not st.session_state.flare and not st.session_state.signal:
        st.image("Space Weather and Communication Monitor/No signals.png")

    elif not st.session_state.flare and st.session_state.signal:
        st.image("Space Weather and Communication Monitor/Normal Signal.png")

    elif st.session_state.flare and not st.session_state.signal:
        st.image("Space Weather and Communication Monitor/just flares.png")

    elif st.session_state.flare and st.session_state.signal:
        st.image("Space Weather and Communication Monitor/Flare signal.png")

    


else:
    pass

st.write("------------------")

st.markdown("""

### Understanding the KPIs

**Strongest Flare**  
The strongest solar flare detected during the selected date. Flare class indicates the intensity of the flare and its potential to cause HF radio disturbances.

**Fastest CME**  
The highest-speed coronal mass ejection detected during the selected date. CME speed provides context about the significance of solar activity, but is not used directly to determine the communications impact level.

**Maximum Kp**  
The highest Kp index recorded during the selected date. Kp measures global geomagnetic disturbance, with higher values indicating stronger disturbances that can affect radio and satellite communications.

**Potential Communications Impact**  
An overall assessment based primarily on solar flare intensity and geomagnetic activity. It represents the potential for communications disruption and should not be interpreted as a prediction of an actual outage.

**Event Counts**  
The number of solar flares, CMEs, and geomagnetic storms detected during the selected date. These provide additional context about the level of space-weather activity.

This program runs on NASA DONKI data.
""")
