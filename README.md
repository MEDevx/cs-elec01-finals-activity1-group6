# 📊 CS ELEC 01 — Computational Science
## Finals Activity 1: Numerical Methods Case Studies

> **College of Engineering and Information Technology**
> Department of Computing and Library Information Science

---

## 👥 Group Members

| Name | Role |
|------|------|
| Muhammed Shariff Sumagka | Member |
| Lara Rain Fuentes | Member |
| Gerard Carl Palma | Member |

---

## 📋 Overview

This repository contains our solutions for **Finals Activity 1** of CS ELEC 01 – Computational Science. We selected **3 out of 5 case studies**, each applying real-world numerical methods to analyze discrete data without a continuous function.

Each solution includes:
- ✅ Step-by-step numerical computation with formulas
- ✅ Console-printed tables and analysis report
- ✅ Multi-panel visualization dashboard (dark-themed, publication-quality)
- ✅ Full inline documentation and docstrings

---

## 📁 Repository Structure

```
.
├── case_study_1_population.py    # Case Study 1: Population Growth
├── case_study_2_traffic.py       # Case Study 2: Traffic Flow & Velocity
├── case_study_5_electricity.py   # Case Study 5: Electricity Consumption
├── case1_population.png          # Output visualization – Case 1
├── case2_traffic.png             # Output visualization – Case 2
├── case5_electricity.png         # Output visualization – Case 5
└── README.md
```

---

## 🔢 Numerical Methods Used

| Method | Formula | Applied In |
|--------|---------|------------|
| **Central Difference** | `f'(xᵢ) ≈ [f(xᵢ₊₁) – f(xᵢ₋₁)] / 2` | Cases 1, 2, 5 |
| **Trapezoidal Rule** | `∫f(x)dx ≈ (h/2) Σ [f(xᵢ) + f(xᵢ₊₁)]` | Cases 1, 2, 5 |
| **Exponential Regression** | `P(t) = a · eᵇᵗ` | Case 1 |

---

## 📦 Case Studies

---

### 📈 Case Study 1 — Population Growth Analysis

**File:** `case_study_1_population.py`

**Scenario:** A local government has yearly population data and wants to analyze growth trends, estimate rates of change, and forecast future population.

**Given Data:**

| Year | Population |
|------|-----------|
| 2020 | 10,000 |
| 2021 | 10,800 |
| 2022 | 11,900 |
| 2023 | 13,200 |
| 2024 | 14,800 |

**Methods:**
- **Central Difference** → estimates growth rate (people/year) at years 2021–2023
- **Trapezoidal Rule** → integrates population over 2020–2024 (person-years)
- **Exponential Regression** → fits `P(t) = a·eᵇᵗ` and predicts 2025 population

**Key Results:**

| Metric | Value |
|--------|-------|
| Growth Rate 2021 | 950 ppl/yr |
| Growth Rate 2022 | 1,200 ppl/yr |
| Growth Rate 2023 | 1,450 ppl/yr |
| ∫ P(t) dt (2020–2024) | 48,300 person-years |
| Growth constant b | 0.1001/yr |
| Doubling time | 6.93 years |
| **2025 Forecast** | **≈ 16,227 people** |

**Analysis:**
- Growth accelerated most in **2022** (+250 ppl/yr increase in rate)
- Growth is **exponential**, not linear (confirmed by positive b value)
- Population growth is consistently increasing each year

---

### 🚗 Case Study 2 — Traffic Flow and Velocity Estimation

**File:** `case_study_2_traffic.py`

**Scenario:** A traffic monitoring system records vehicle position every second. Engineers compute velocity, acceleration, and verify total distance.

**Given Data:**

| Time (s) | Position (m) |
|----------|-------------|
| 0 | 0 |
| 1 | 5 |
| 2 | 15 |
| 3 | 30 |
| 4 | 50 |
| 5 | 75 |

**Methods:**
- **Central Difference** → velocity at t = 1, 2, 3, 4
- **Central Difference (2nd pass)** → acceleration from velocity values
- **Trapezoidal Rule** → distance ∫v(t)dt compared to actual displacement

**Key Results:**

| Time (s) | Velocity (m/s) |
|----------|---------------|
| 1 | 7.50 |
| 2 | 12.50 |
| 3 | 17.50 |
| 4 | 22.50 |

| Metric | Value |
|--------|-------|
| Acceleration | 5.00 m/s² (constant) |
| Motion type | Uniform acceleration |
| ∫ v(t) dt | 75.00 m |
| Actual displacement | 75.00 m |
| **Error** | **0.0000 m ✅** |

**Analysis:**
- The vehicle undergoes **uniform acceleration** at a constant 5.00 m/s²
- Motion is **not uniform** — velocity increases each second
- Trapezoidal integration **exactly matches** actual displacement (zero error)
- No anomalies detected; position increases smoothly

---

### ⚡ Case Study 5 — Electricity Consumption and Power Analysis

**File:** `case_study_5_electricity.py`

**Scenario:** A household records energy consumption (kWh) every 2 hours. The goal is to determine instantaneous power and verify total energy via integration.

**Given Data:**

| Time (hr) | Energy (kWh) |
|-----------|-------------|
| 0 | 0.0 |
| 2 | 1.5 |
| 4 | 3.5 |
| 6 | 6.0 |
| 8 | 9.0 |
| 10 | 13.0 |

**Methods:**
- **Central Difference** (h = 2) → instantaneous power P(t) = dE/dt at t = 2, 4, 6, 8
- **Trapezoidal Rule** → ∫P(t)dt should ≈ 13 kWh (total energy)

**Key Results:**

| Time (hr) | Power (kW) |
|-----------|-----------|
| 2 | 0.8750 |
| 4 | 1.1250 |
| 6 | 1.3750 |
| 8 | 1.7500 |

| Metric | Value |
|--------|-------|
| ∫ P(t) dt | 13.0000 kWh |
| Expected energy | 13.0000 kWh |
| **Integration error** | **0.0000 kWh ✅** |
| Peak power | 1.7500 kW at t=8h |
| Consumption trend | Non-constant, increasing |

**Analysis:**
- Electricity consumption is **accelerating** — not steady
- Peak usage is during **8h–10h** period (+4.0 kWh in 2 hours)
- Integration perfectly confirms the expected 13 kWh total
- Suggestions: shift heavy appliances to off-peak hours (0–4h), use smart timers, install energy-efficient devices

---

## 🛠️ Setup and Usage

### Requirements

```
Python 3.8+
numpy
matplotlib
scipy  (Case Study 1 only)
```

### Installation

```bash
pip install numpy matplotlib scipy
```

### Running the Scripts

```bash
# Case Study 1 – Population Growth
python case_study_1_population.py

# Case Study 2 – Traffic Flow
python case_study_2_traffic.py

# Case Study 5 – Electricity Consumption
python case_study_5_electricity.py
```

Each script will:
1. Print a formatted console report with all computed values
2. Display and save a visualization dashboard as a `.png` file

---

## 📊 Sample Output Visualizations

### Case Study 1 — Population Growth
![Case 1](case1_population.png)

### Case Study 2 — Traffic Flow
![Case 2](case2_traffic.png)

### Case Study 5 — Electricity Consumption
![Case 5](case5_electricity.png)

---

## 📚 References

- Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis* (9th ed.). Brooks/Cole.
- Chapra, S. C., & Canale, R. P. (2015). *Numerical Methods for Engineers* (7th ed.). McGraw-Hill.
- NumPy Documentation: https://numpy.org/doc/
- Matplotlib Documentation: https://matplotlib.org/stable/

---

## 📝 Notes

- All numerical methods are implemented **from scratch** using only NumPy arrays (no built-in derivative/integral shortcuts for the core computations).
- The `scipy.optimize.curve_fit` used in Case Study 1 is only for the optional exponential regression / 2025 prediction step.
- Visualizations use `matplotlib` with a custom dark dashboard theme.

---

*CS ELEC 01 – Computational Science | Finals Activity 1 | AY 2025–2026*
