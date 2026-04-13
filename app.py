import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# --- Page Config ---
st.set_page_config(page_title="MEMS Digital Twin", layout="wide")
st.title("🔬 3D MEMS Optical Port - Predictive Maintenance Digital Twin")
st.markdown("Physical simulation of the degradation of optical routing switches in 100G Data Center networks.")

# --- Sidebar Controls ---
st.sidebar.header("🎛️ Operating Parameters (Physical Parameters)")
temperature = st.sidebar.slider("Server Temperature (°C)", min_value=20.0, max_value=70.0, value=35.0, step=1.0)
max_hours = st.sidebar.slider("Simulation Time (hours)", min_value=1000, max_value=12000, value=8000, step=500)
base_il = st.sidebar.number_input("Base IL dB)", value=1.5)

# --- Physics Engine ---
class OCS_DigitalTwin: 
def __init__(self, temp_celsius, base_loss): 
self.age_hours = 0 
self.base_loss = base_loss 
self.temp_k = temp_celsius + 273.15 
self.acc_factor = np.exp((0.5 / 8.617e-5) * (1/(25.0 + 273.15) - 1/self.temp_k)) 
self. drift_angle = 0.0 
self.contamination = 0.0 
self.history= {'hours': [], 'il': [], 'osnr': [], 'ber': []} 

def advance_time(self, hours): 
self.age_hours += hours 
self.drift_angle += (0.0001 * self.acc_factor) * hours 
self.contamination = min(1.0, self.contamination + (0.00005 * hours)) 

il = self.base_loss + 4.34 * ((self.drift_angle / 0.5) ** 2) + (self.contamination * 15.0) 
osnr = (0.0 - il) - (-40.0) 

q_approx = np.sqrt((10 ** (osnr / 10)) / 4.0) 
ber = max(1e-16, 0.5 * erfc(q_approx / np.sqrt(2))) if osnr > 10.0 else 1e-2

self.history['hours'].append(self.age_hours)

self.history['il'].append(il)

self.history['osnr'].append(osnr)

self.history['ber'].append(ber)

# --- Run Simulation ---
port = OCS_DigitalTwin(temperature, base_il)
step = 100
for _ in range(max_hours // step):

port.advance_time(step)

# --- Metrics Dashboard ---
st.subheader("📊 Current Performance Indicators (at the end of the simulation)")
col1, col2, col3 = st.columns(3)
final_il = port.history['il'][-1]
final_ber = port.history['ber'][-1]

col1.metric("Total Loss (Max IL)", f"{final_il:.2f} dB", delta=f"+{final_il - base_il:.2f} dB", delta_color="inverse")
col2.metric("Signal Quality (Min OSNR)", f"{port.history['osnr'][-1]:.2f} dB")
col3.metric("Error Rate (Final BER)", f"{final_ber:.1e}", "Catastrophic degradation" if final_ber > 1e-4 else "Stable")

# --- Charts ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(port.history['hours'], port.history['il'], 'r-', lw=2)
ax1.axhline(y=8.0, color='k', linestyle='--', label='Failure (8dB)')
ax1.set_title(f'Insertion Loss Degradation')
ax1.set_xlabel('Operating Hours')
ax1.set_ylabel('Loss (dB)')
ax1.grid(True)
ax1.legend()

ax2.semilogy(port.history['hours'], port.history['ber'], 'b-', lw=2)
ax2.axhline(y=1e-4, color='k', linestyle='--', label='Critical Error')
ax2.set_title('BER (Waterfall Effect)')
ax2.set_xlabel('Operating Hours')
ax2.set_ylim(1e-16, 1e-1)
ax2.grid(True)
ax2.legend()

st.pyplot(fig)

if final_il > 8.0:

st.error("⚠️ Physical failure: Loss exceeds the maximum limit! Requires immediate maintenance.")
else:

st.success("✅ System is operating within safe limits.")