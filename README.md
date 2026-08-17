# Space Weather & Communication Monitor

A Python project that uses NASA's DONKI API to analyze space-weather activity and demonstrate its potential impact on communications.

The project includes **Live Mode**, **Simulation Mode**, and an **Illustrative Simulator** designed for both technical and non-technical audiences.

## Features

* ☀️ Detects the strongest solar flare
* ☄️ Finds the fastest CME
* 🧲 Finds the maximum Kp index
* 📊 Calculates a communications impact level
* 📈 Visualizes space-weather activity
* 🖥️ Interactive Streamlit dashboard
* 📡 Simulates communication-signal degradation
* 🎛️ Adjustable R-scale and G-scale conditions
* 📻 Adjustable signal frequency
* 📶 Simulates noise and attenuation
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

NASA DONKI → Space-weather data → KPI analysis → Impact assessment

### Simulation Mode

R/G Scale
↓
Impact Parameters
↓
Noise + Attenuation + Fading + Blackouts
↓
Simulated Signal

Simulation parameters are project-specific engineering models intended to demonstrate potential communication effects rather than reproduce measured propagation data.

### Illustrative Simulator

A visual demonstration showing an HF communication link before and after a solar flare.

Normal Signal
↓
Solar Flare
↓
Disturbed Ionosphere
↓
Degraded Communication

Users can send a signal, introduce a solar flare, observe the changed communication environment, and reset the simulation.

## NOAA Scales

* **R0–R5** — Radio-blackout severity
* **G0–G5** — Geomagnetic-storm severity

Higher levels produce progressively stronger modeled effects.

## Setup

Get a NASA API key from the NASA API portal and create a `.env` file:

NASA_API_KEY=your_api_key_here

Install dependencies:

pip install -r requirements.txt

Run:

python -m streamlit run gui.py

**Never upload your personal API key to GitHub.**

## Data Sources

* NASA DONKI API
* NOAA Space Weather Scales

## Note

The impact assessment and simulation parameters are **project-specific models**, not official NASA or NOAA predictions. The project is an educational demonstration of the potential relationship between space weather and communication-system degradation.