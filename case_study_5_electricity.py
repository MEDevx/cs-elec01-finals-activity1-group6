"""
================================================================================
  CS ELEC 01 — COMPUTATIONAL SCIENCE
  Finals Activity 1  |  Case Study 5: Electricity Consumption & Power Analysis
================================================================================

  Course      : CS ELEC 01 – Computational Science
  Activity    : Finals Activity 1 – Numerical Methods Case Studies
  Topic       : Electricity Consumption and Power Analysis

  Group Members:
    • Muhammed Shariff Sumagka
    • Lara Rain Fuentes
    • Gerard Carl Palma

  Institution : College of Engineering and Information Technology
                Department of Computing and Library Information Science

  Description:
    A household records electric energy consumption (kWh) at different times
    of the day. This script:
      1. Computes instantaneous power usage (derivative of energy) using the
         Central Difference Method.
      2. Verifies total energy consumed via Numerical Integration (Trapezoidal
         Rule), which should approximate 13 kWh.
      3. Identifies peak usage periods and provides reduction recommendations.
      4. Produces a multi-panel visualization dashboard with analysis.

  Numerical Methods:
    ┌─────────────────────────────────────────────────────────────────────┐
    │  Power (Central Diff): P(t) ≈ [E(t+h) – E(t-h)] / (2h)            │
    │  Total Energy (Trap.): ∫ P(t) dt ≈ (h/2) Σ [P(tᵢ) + P(tᵢ₊₁)]    │
    └─────────────────────────────────────────────────────────────────────┘

  Note:
    h = 2 hours (uniform step size)
    Power is the rate of energy use: P(t) = dE/dt  [units: kW]
    Integrating P(t) over time recovers total energy [units: kWh]

  Dependencies : numpy, matplotlib
  Install      : pip install numpy matplotlib
  Usage        : python case_study_5_electricity.py

================================================================================
"""

# ── Standard Library ──────────────────────────────────────────────────────────
import sys

# ── Third-party ───────────────────────────────────────────────────────────────
try:
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.ticker import FuncFormatter
except ImportError as e:
    sys.exit(f"[ERROR] Missing dependency: {e}\nInstall: pip install numpy matplotlib")

# ══════════════════════════════════════════════════════════════════════════════
#  DATASET
# ══════════════════════════════════════════════════════════════════════════════
time   = np.array([0, 2, 4, 6, 8, 10], dtype=float)      # hours
energy = np.array([0, 1.5, 3.5, 6.0, 9.0, 13.0], dtype=float)  # kWh
h      = 2.0   # uniform step size (hours)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — Numerical Differentiation: Power P(t) = dE/dt
#  Central Difference: P(t) ≈ [E(t+h) – E(t-h)] / (2h)
#  Applied at interior points: t = 2, 4, 6, 8
# ══════════════════════════════════════════════════════════════════════════════
power: dict[int, float] = {}
for i in range(1, len(time) - 1):
    power[int(time[i])] = (energy[i + 1] - energy[i - 1]) / (2.0 * h)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — Numerical Integration (Trapezoidal Rule)
#  Build full power array using forward/backward differences at endpoints,
#  then integrate: ∫ P(t) dt  should ≈  total energy = 13 kWh
# ══════════════════════════════════════════════════════════════════════════════
p_full     = np.zeros(len(time))
p_full[0]  = (energy[1] - energy[0]) / h          # forward diff
p_full[-1] = (energy[-1] - energy[-2]) / h         # backward diff
for i in range(1, len(time) - 1):
    p_full[i] = power[int(time[i])]

trap_energy    = np.trapezoid(p_full, time)
expected_total = 13.0
error          = abs(trap_energy - expected_total)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — Analysis
# ══════════════════════════════════════════════════════════════════════════════
pw_keys     = sorted(power.keys())
pw_vals     = [power[t] for t in pw_keys]
max_pwr_t   = max(power, key=power.get)
max_pwr_v   = power[max_pwr_t]
delta_e     = np.diff(energy)

# Growth rate of power (is it accelerating?)
power_growth = np.diff(pw_vals)
is_increasing = all(g > 0 for g in power_growth)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE REPORT
# ══════════════════════════════════════════════════════════════════════════════
LINE = "═" * 62

print(f"\n{LINE}")
print("  CS ELEC 01  |  CASE STUDY 5 — ELECTRICITY CONSUMPTION")
print(LINE)
print("  Group: Sumagka · Fuentes · Palma")
print(LINE)

print(f"\n  GIVEN DATA")
print(f"  {'Time (hr)':<12} {'Energy (kWh)':>14}")
print(f"  {'─'*28}")
for t, e in zip(time.astype(int), energy):
    print(f"  {t:<12} {e:>14.1f}")

print(f"\n  STEP 1 — Power Consumption (Central Difference)")
print(f"  Formula : P(t) ≈ [E(t+h) – E(t-h)] / (2h),  h = {int(h)} hr")
print(f"\n  {'Time (hr)':<12} {'Energy (kWh)':>14}  {'Power (kW)':>14}")
print(f"  {'─'*44}")
for t, e in zip(time.astype(int), energy):
    p = power.get(t)
    ps = f"{p:>10.4f}" if p is not None else f"{'N/A (endpoint)':>18}"
    print(f"  {t:<12} {e:>14.1f}  {ps:>14}")

print(f"\n  STEP 2 — Total Energy Verification (Trapezoidal Rule)")
print(f"  Formula : ∫ P(t) dt ≈ (h/2) Σ [P(tᵢ) + P(tᵢ₊₁)]")
print(f"  ∫₀¹⁰ P(t) dt  ≈  {trap_energy:.4f} kWh")
print(f"  Expected total  =  {expected_total:.4f} kWh")
print(f"  Absolute Error  =  {error:.4f} kWh  {'✅' if error < 0.01 else '⚠️'}")

print(f"\n  STEP 3 — Analysis")
print(f"  Peak power at  : t = {max_pwr_t}h  →  {max_pwr_v:.4f} kW")
print(f"  Power trend    : {'INCREASING (accelerating consumption)' if is_increasing else 'VARIABLE'}")
print(f"  Flow type      : NON-CONSTANT (not steady-state)")
print(f"  Energy per 2hr period:")
for t0, t1, δ in zip(time.astype(int), time[1:].astype(int), delta_e):
    bar = "▓" * int(δ * 5)
    print(f"    {t0}h→{t1}h : +{δ:.1f} kWh  {bar}")

print(f"\n  STEP 4 — Peak Usage Reduction Suggestions")
suggestions = [
    "Shift heavy appliances (washer, dishwasher) to off-peak hours (0–4h)",
    "Install smart timers on high-consumption devices",
    "Use energy-efficient appliances rated A++ or higher",
    "Set HVAC to eco-mode during peak hours (8–10h)",
    "Install solar panels to offset daytime demand",
]
for i, s in enumerate(suggestions, 1):
    print(f"  {i}. {s}")
print(f"\n{LINE}\n")

# ══════════════════════════════════════════════════════════════════════════════
#  VISUALIZATION  — Warm Amber / Energy-Themed Dashboard
# ══════════════════════════════════════════════════════════════════════════════
BG     = "#0c0a04"
PANEL  = "#16120a"
CARD   = "#1c1810"
GRID   = "#2a2415"
C_AMB  = "#f59e0b"
C_RED  = "#f87171"
C_GRN  = "#6ee7b7"
C_BLU  = "#7dd3fc"
C_TEXT = "#fef3c7"
C_MUTE = "#78716c"

plt.rcParams.update({
    "font.family"       : "monospace",
    "text.color"        : C_TEXT,
    "axes.labelcolor"   : C_MUTE,
    "xtick.color"       : C_MUTE,
    "ytick.color"       : C_MUTE,
    "axes.edgecolor"    : GRID,
    "figure.facecolor"  : BG,
    "axes.facecolor"    : PANEL,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
})

fig = plt.figure(figsize=(16, 11))
fig.patch.set_facecolor(BG)

fig.text(0.5, 0.975,
         "▸  CASE STUDY 5  ·  ELECTRICITY CONSUMPTION & POWER ANALYSIS",
         ha="center", fontsize=14, fontweight="bold",
         color=C_AMB, fontfamily="monospace")
fig.text(0.5, 0.950,
         "CS ELEC 01 — Computational Science  |  Central Difference & Trapezoidal Rule",
         ha="center", fontsize=9, color=C_MUTE, fontfamily="monospace")

gs = gridspec.GridSpec(2, 3, figure=fig,
                       top=0.925, bottom=0.075,
                       hspace=0.52, wspace=0.38,
                       left=0.07, right=0.96)

# ── Panel A: Energy vs Time (full width) ──────────────────────────────────
axA = fig.add_subplot(gs[0, :])
axA.set_facecolor(CARD)
axA.plot(time, energy, color=C_AMB, lw=2.5,
         marker="o", markersize=9, zorder=4, label="Energy (kWh)")
axA.fill_between(time, energy, alpha=0.14, color=C_AMB)
for t, e in zip(time.astype(int), energy):
    axA.annotate(f"  {e} kWh", (t, e), fontsize=8.5, color=C_TEXT, va="center")
axA.set_title("Energy Consumption vs Time  (0 – 10 h)", fontsize=12, color=C_TEXT,
              pad=10, loc="left", fontweight="bold")
axA.set_xlabel("Time (hours)")
axA.set_ylabel("Energy (kWh)")
axA.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=9)
axA.grid(color=GRID, linestyle="--", linewidth=0.5)
axA.set_xlim(-0.3, 10.8)

# ── Panel B: Power vs Time ─────────────────────────────────────────────────
axB = fig.add_subplot(gs[1, 0])
axB.set_facecolor(CARD)
axB.plot(pw_keys, pw_vals, color=C_RED, lw=2.5,
         marker="D", markersize=8, zorder=4, label="Power (kW)")
axB.fill_between(pw_keys, pw_vals, alpha=0.14, color=C_RED)
# Highlight peak
axB.scatter([max_pwr_t], [max_pwr_v], color=C_TEXT, s=120,
            zorder=6, marker="*", label=f"Peak: {max_pwr_v:.4f} kW")
for t, p in zip(pw_keys, pw_vals):
    axB.annotate(f"  {p:.3f}", (t, p), fontsize=8, color=C_TEXT, va="center")
axB.set_title("Instantaneous Power vs Time", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axB.set_xlabel("Time (hours)")
axB.set_ylabel("Power (kW)")
axB.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=8)
axB.grid(color=GRID, linestyle="--", linewidth=0.5)

# ── Panel C: Energy per 2-hour period ─────────────────────────────────────
axC = fig.add_subplot(gs[1, 1])
axC.set_facecolor(CARD)
delta_labels = [f"{int(t0)}–{int(t1)}h"
                for t0, t1 in zip(time, time[1:])]
colors_bar = [C_GRN if δ <= np.median(delta_e) else C_RED for δ in delta_e]
bars = axC.bar(range(len(delta_e)), delta_e, color=colors_bar,
               width=0.55, alpha=0.85, zorder=3)
axC.set_xticks(range(len(delta_e)))
axC.set_xticklabels(delta_labels, fontsize=8.5)
for i, (bar, δ) in enumerate(zip(bars, delta_e)):
    axC.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 0.05, f"+{δ:.1f}",
             ha="center", color=C_TEXT, fontsize=9)
axC.set_title("Energy per 2-hr Period  (kWh)", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axC.set_xlabel("Time Interval")
axC.set_ylabel("ΔEnergy (kWh)")
axC.grid(color=GRID, linestyle="--", linewidth=0.5, axis="y")

# ── Panel D: Key Results Card ─────────────────────────────────────────────
axD = fig.add_subplot(gs[1, 2])
axD.set_facecolor(CARD)
axD.axis("off")
axD.set_title("Key Results", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")

metrics = [
    ("Peak power",       f"{max_pwr_v:.4f} kW @ t={max_pwr_t}h"),
    ("Peak period",      "8h – 10h"),
    ("∫ P(t) dt",        f"{trap_energy:.4f} kWh"),
    ("Expected energy",  f"{expected_total:.1f} kWh"),
    ("Integration error",f"{error:.4f} kWh  ✅"),
    ("Flow type",        "Non-constant (↑)"),
]
for k, (label, value) in enumerate(metrics):
    y = 0.88 - k * 0.155
    rect = plt.Rectangle((0.02, y - 0.07), 0.96, 0.13,
                          transform=axD.transAxes,
                          facecolor=GRID, edgecolor="none", zorder=1)
    axD.add_patch(rect)
    axD.text(0.07, y, label, transform=axD.transAxes,
             fontsize=8, color=C_MUTE, va="center")
    axD.text(0.95, y, value, transform=axD.transAxes,
             fontsize=9, color=C_AMB, ha="right",
             va="center", fontweight="bold")

# Footer
fig.text(0.5, 0.018,
         "Muhammed Shariff Sumagka  ·  Lara Rain Fuentes  ·  Gerard Carl Palma  "
         "|  CS ELEC 01 — Computational Science",
         ha="center", fontsize=8, color=C_MUTE, fontfamily="monospace")

out = "case5_electricity.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"✅  Visualization saved → {out}")
plt.show()
