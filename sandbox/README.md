# 🛡️ Sandbox Isolation: Talent Reconnaissance Engine

## Overview
This directory houses the isolated sandbox environment for the **Dynamic Veteran Talent Reconnaissance Grid**. It is decoupled from the core production Lakehouse pipeline to enable rapid prototyping, local mock-data simulation, and dry-run validation without altering production assets.

---

## 📂 Sandbox Directory Structure

```
sandbox/
├── recon_app.py        # Standalone Streamlit dynamic search interface
├── mock_data.csv       # Local test ledger of veteran engineering profiles
├── test_recon.py       # Independent Pytest validation suite
└── README.md           # Sandbox specification & documentation
```

---

## 🚀 How to Run the Sandbox Locally

### 1. Launch the Isolated Streamlit App
```powershell
.\venv\Scripts\streamlit.exe run sandbox/recon_app.py
```

### 2. Run Isolated Sandbox Tests
```powershell
.\venv\Scripts\pytest.exe sandbox/test_recon.py -v
```

---

## 🎯 Gunslinger Lore: Building in the Trench

> *Before you take a new weapon system to the front lines, you test it in the trench. Sandbox isolation keeps the perimeter secure and your production line undisturbed while you calibrate your dynamic targeting algorithms.*
