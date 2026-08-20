# Space Weather & Communication Monitor

A Python project using NASA's DONKI API to analyze space-weather activity and demonstrate its potential impact on communications.

The project includes **Live Mode**, **Simulation Mode**, and an **Illustrative Simulator**.

## Features

* ☀️ Detects the strongest solar flare
* ☄️ Finds the fastest CME
* 🧲 Finds the maximum Kp index
* 📊 Calculates a communications impact level
* 📈 Visualizes space-weather activity
* 🖥️ Interactive Streamlit dashboard
* 📡 Models communication-signal degradation
* 🎛️ Uses R/G-scale conditions
* 📻 Adjustable frequency and amplitude
* 📶 Simulates noise, attenuation, and fading
* 🚫 Simulates communication blackouts
* 🎨 Interactive illustrative communication simulator

## Technologies

* Python
* NumPy
* Pandas
* Matplotlib
* Streamlit
* Plotly
* NASA DONKI API

## How It Works

### Live Mode

NASA DONKI → Space-weather data → KPI analysis → R/G classification → Impact assessment → Signal impact visualization

### Simulation Mode

R/G Scale → Impact Parameters → Noise + Attenuation + Fading + Blackouts → Simulated Signal

Users can adjust R/G conditions, frequency, and amplitude to explore modeled communication effects.

### Illustrative Simulator

Normal Signal → Solar Flare → Degraded Communication

## NOAA Scales

* **R0–R5** — Radio-blackout severity
* **G0–G5** — Geomagnetic-storm severity

Higher levels produce stronger modeled effects.

## Setup

Get a NASA API key from the NASA API portal and create a `.env` file:

NASA_API_KEY=your_api_key_here

Install dependencies:

pip install -r requirements.txt

Run:

 python -m streamlit run '.\Space Weather and Communication Monitor\gui.py'          

**Never upload your personal API key to GitHub.**

## Data Sources

* NASA DONKI API
* NOAA Space Weather Scales

## Note

The impact assessment and signal-simulation parameters are **project-specific models**, not official NASA or NOAA predictions. The simulator is an educational demonstration of the potential relationship between space weather and communication-system degradation.