# 🔬 Sovereign Reliability Engine: Packet-Optical Data Center Digital Twin

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-brightgreen)
![SimPy](https://img.shields.io/badge/SimPy-Simulation-orange)

A highly advanced, physics-based **Discrete-Event Simulator (DES)** and **Digital Twin** for modern 100G/400G Data Center Networks (DCNs). This project explores the critical intersection of Software-Defined Networking (SDN) and Optical Physics, specifically focusing on **3D MEMS Optical Circuit Switches (OCS)**.

---

## 🎯 Research Objectives

Modern data centers (like those engineered by Google, Meta, and AI clusters) are shifting from purely electrical Spine-Leaf architectures to **Hybrid Packet-Optical Fabrics**. This simulator was built to mathematically and physically prove:

1. **The Flaw of Blind ECMP:** Hash collisions cause elephant flows to congest electrical links.
2. **The "Thundering Herd" Problem of Naive SDN:** Centralized controllers routing all traffic to the least-congested link paradoxically create massive queue buildups and spike Tail Latency (P99).
3. **The Power of Hybrid SDN:** Intelligently routing "Mice" flows via ECMP and "Elephant" flows via SDN.
4. **The Ultimate Optical Bypass:** Utilizing 3D MEMS Optical Circuit Switches to route Elephant flows via photons (Zero-Buffering, Zero-Queuing), drastically reducing Flow Completion Time (FCT).
5. **Physical Reliability (Digital Twin):** Simulating hardware degradation of MEMS mirrors (Thermal Drift, Dust Contamination) and its direct impact on Insertion Loss (IL), OSNR, and Bit Error Rate (BER Waterfall).

---

## ⚙️ Architecture & Features

This repository contains two core simulation engines:

### 1. `hybrid_sdn_simulator.py` (The Network Dynamics Engine)
A Packet-Level simulator comparing four architectural paradigms:
* **ECMP (Baseline):** Deterministic hashing. Fast but collision-prone.
* **SDN Naive:** Queue-aware routing. Suffers from the Thundering Herd phenomenon.
* **SDN Hybrid:** Intelligent traffic classification (Mice vs. Elephants) within electrical spines.
* **SDN Optical (3D MEMS):** Elephants are offloaded to an Optical Switch, bypassing electrical buffers entirely.

### 2. `mems_digital_twin.py` / `app.py` (The Physics Reliability Engine)
A Predictive Maintenance Digital Twin modeling the physical decay of optical hardware:
* **Gaussian Beam Coupling Loss:** Modeled via Arrhenius accelerated aging equations.
* **Contamination Scattering:** Degradation due to dust accumulation.
* **OSNR to BER Mapping:** Demonstrates the catastrophic "Waterfall BER Degradation" when optical Signal-to-Noise Ratio drops below critical thresholds (e.g., 12 dB for 100G DP-QPSK).

---

## 🚀 Installation & Usage

**Prerequisites:**
Standard Python data science libraries. No complex networking stacks required.
```bash
pip install simpy numpy pandas matplotlib scipy streamlit