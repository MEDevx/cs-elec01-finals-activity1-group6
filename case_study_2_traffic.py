"""
================================================================================
  CS ELEC 01 — COMPUTATIONAL SCIENCE
  Finals Activity 1  |  Case Study 2: Traffic Flow and Velocity Estimation
================================================================================

  Course      : CS ELEC 01 – Computational Science
  Activity    : Finals Activity 1 – Numerical Methods Case Studies
  Topic       : Traffic Flow and Velocity Estimation

  Group Members:
    • Muhammed Shariff Sumagka
    • Lara Rain Fuentes
    • Gerard Carl Palma

  Institution : College of Engineering and Information Technology
                Department of Computing and Library Information Science

  Description:
    A traffic monitoring system records the position of a vehicle every second.
    Engineers want to compute velocity and total distance traveled.
    This script:
      1. Estimates instantaneous velocity using the Central Difference Method.
      2. Estimates acceleration from the velocity values (optional extension).
      3. Verifies total distance via the Trapezoidal Rule and compares with
         the actual displacement.
      4. Produces a multi-panel visualization dashboard with analysis.

  Numerical Methods:
    ┌─────────────────────────────────────────────────────────────────────┐
    │  Velocity (Central Diff): v(t) = [x(t+1) – x(t-1)] / 2            │
    │  Acceleration (Central Diff): a(t) = [v(t+1) – v(t-1)] / 2        │
    │  Distance (Trapezoidal Rule): ∫ v(t) dt ≈ (h/2) Σ [v(tᵢ)+v(tᵢ₊₁)]│
    └─────────────────────────────────────────────────────────────────────┘

  Dependencies : numpy, matplotlib
  Install      : pip install numpy matplotlib
  Usage        : python case_study_2_traffic.py

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
time     = np.array([0, 1, 2, 3, 4, 5], dtype=float)   # seconds
position = np.array([0, 5, 15, 30, 50, 75], dtype=float)  # metres

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — Numerical Differentiation: Velocity
#  Central Difference: v(tᵢ) = [x(tᵢ₊₁) – x(tᵢ₋₁)] / 2
#  Applied at interior points: t = 1, 2, 3, 4
# ══════════════════════════════════════════════════════════════════════════════
velocity: dict[int, float] = {}
for i in range(1, len(time) - 1):
    velocity[int(time[i])] = (position[i + 1] - position[i - 1]) / 2.0

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — Optional Extension: Acceleration
#  Central Difference on velocity: a(t) = [v(t+1) – v(t-1)] / 2
# ══════════════════════════════════════════════════════════════════════════════
vel_keys = sorted(velocity.keys())
vel_vals = [velocity[t] for t in vel_keys]

acceleration: dict[int, float] = {}
for i in range(1, len(vel_keys) - 1):
    acceleration[vel_keys[i]] = (vel_vals[i + 1] - vel_vals[i - 1]) / 2.0

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — Numerical Integration: Distance Verification (Trapezoidal Rule)
#  Build a full velocity array (endpoints via forward/backward difference)
#  then integrate: ∫ v(t) dt ≈ actual displacement
# ══════════════════════════════════════════════════════════════════════════════
v_full    = np.zeros(len(time))
v_full[0] = position[1] - position[0]        # forward difference at t=0
v_full[-1]= position[-1] - position[-2]       # backward difference at t=5
for i in range(1, len(time) - 1):
    v_full[i] = velocity[int(time[i])]

trap_distance      = np.trapezoid(v_full, time)
actual_displacement= position[-1] - position[0]

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — Analysis
# ══════════════════════════════════════════════════════════════════════════════
# Acceleration is constant at 5 m/s² (uniform acceleration)
accel_vals    = list(acceleration.values())
is_uniform    = np.allclose(accel_vals, accel_vals[0], atol=1e-9)
accel_const   = accel_vals[0]
max_vel_t     = max(velocity, key=velocity.get)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE REPORT
# ══════════════════════════════════════════════════════════════════════════════
LINE = "═" * 62

print(f"\n{LINE}")
print("  CS ELEC 01  |  CASE STUDY 2 — TRAFFIC FLOW & VELOCITY")
print(LINE)
print("  Group: Sumagka · Fuentes · Palma")
print(LINE)

print(f"\n  GIVEN DATA")
print(f"  {'Time (s)':<10} {'Position (m)':>14}")
print(f"  {'─'*26}")
for t, x in zip(time.astype(int), position.astype(int)):
    print(f"  {t:<10} {x:>14,}")

print(f"\n  STEP 1 — Velocity (Central Difference)")
print(f"  Formula : v(tᵢ) = [x(tᵢ₊₁) – x(tᵢ₋₁)] / 2")
print(f"\n  {'Time (s)':<10} {'Position (m)':>14}  {'Velocity (m/s)':>16}")
print(f"  {'─'*44}")
for t, x in zip(time.astype(int), position.astype(int)):
    v = velocity.get(t)
    vs = f"{v:>12.2f}" if v is not None else f"{'N/A (endpoint)':>20}"
    print(f"  {t:<10} {x:>14,}  {vs:>16}")

print(f"\n  STEP 2 — Acceleration (Optional Extension)")
print(f"  Formula : a(t) = [v(t+1) – v(t-1)] / 2")
print(f"\n  {'Time (s)':<10} {'Velocity (m/s)':>16}  {'Acceleration (m/s²)':>22}")
print(f"  {'─'*52}")
for t, v in zip(vel_keys, vel_vals):
    a = acceleration.get(t)
    a_s = f"{a:>14.2f}" if a is not None else f"{'N/A (endpoint)':>22}"
    print(f"  {t:<10} {v:>16.2f}  {a_s:>22}")

print(f"\n  STEP 3 — Distance Verification (Trapezoidal Rule)")
print(f"  Formula : ∫ v(t) dt ≈ (h/2) Σ [v(tᵢ) + v(tᵢ₊₁)]")
print(f"  ∫₀⁵ v(t) dt  ≈  {trap_distance:.4f} m")
print(f"  Actual displacement   = {actual_displacement:.4f} m")
print(f"  Absolute Error        = {abs(trap_distance - actual_displacement):.4f} m  ✅")

print(f"\n  STEP 4 — Analysis")
print(f"  Motion type      : {'UNIFORM ACCELERATION' if is_uniform else 'NON-UNIFORM'}")
print(f"  Acceleration     : {accel_const:.2f} m/s² (constant)")
print(f"  Peak velocity    : {velocity[max_vel_t]:.1f} m/s  at  t = {max_vel_t}s")
print(f"  No anomalies     : position increases smoothly every second")
print(f"  Trapezoidal dist : exactly matches actual displacement (0 error)")
print(f"\n{LINE}\n")

# ══════════════════════════════════════════════════════════════════════════════
#  VISUALIZATION  — Electric Teal / Motion-Themed Dashboard
# ══════════════════════════════════════════════════════════════════════════════
BG     = "#060f18"
PANEL  = "#0a1a28"
CARD   = "#0e2035"
GRID   = "#152b40"
C_TEAL = "#2dd4bf"
C_PINK = "#f472b6"
C_GRN  = "#4ade80"
C_GOLD = "#fcd34d"
C_TEXT = "#ddeeff"
C_MUTE = "#4d7a99"

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
         "▸  CASE STUDY 2  ·  TRAFFIC FLOW & VELOCITY ESTIMATION",
         ha="center", fontsize=14, fontweight="bold",
         color=C_TEAL, fontfamily="monospace")
fig.text(0.5, 0.950,
         "CS ELEC 01 — Computational Science  |  Central Difference & Trapezoidal Rule",
         ha="center", fontsize=9, color=C_MUTE, fontfamily="monospace")

gs = gridspec.GridSpec(2, 3, figure=fig,
                       top=0.925, bottom=0.075,
                       hspace=0.52, wspace=0.38,
                       left=0.07, right=0.96)

# ── Panel A: Position vs Time (full width) ────────────────────────────────
axA = fig.add_subplot(gs[0, :])
axA.set_facecolor(CARD)
axA.plot(time, position, color=C_TEAL, lw=2.5,
         marker="o", markersize=9, zorder=4, label="Position (m)")
axA.fill_between(time, position, alpha=0.12, color=C_TEAL)
for t, x in zip(time.astype(int), position.astype(int)):
    axA.annotate(f"  {x}m", (t, x), fontsize=8.5, color=C_TEXT, va="center")
axA.set_title("Position vs Time  (0 – 5 s)", fontsize=12, color=C_TEXT,
              pad=10, loc="left", fontweight="bold")
axA.set_xlabel("Time (s)")
axA.set_ylabel("Position (m)")
axA.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=9)
axA.grid(color=GRID, linestyle="--", linewidth=0.5)
axA.set_xlim(-0.2, 5.4)

# ── Panel B: Velocity vs Time ─────────────────────────────────────────────
axB = fig.add_subplot(gs[1, 0])
axB.set_facecolor(CARD)
axB.plot(vel_keys, vel_vals, color=C_PINK, lw=2.5,
         marker="s", markersize=8, zorder=4, label="Velocity (m/s)")
axB.fill_between(vel_keys, vel_vals, alpha=0.12, color=C_PINK)
for t, v in zip(vel_keys, vel_vals):
    axB.annotate(f"  {v:.1f}", (t, v), fontsize=8.5, color=C_TEXT, va="center")
axB.set_title("Velocity vs Time", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axB.set_xlabel("Time (s)")
axB.set_ylabel("Velocity (m/s)")
axB.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=9)
axB.grid(color=GRID, linestyle="--", linewidth=0.5)

# ── Panel C: Acceleration vs Time ─────────────────────────────────────────
axC = fig.add_subplot(gs[1, 1])
axC.set_facecolor(CARD)
a_keys = sorted(acceleration.keys())
a_vals = [acceleration[t] for t in a_keys]
axC.bar(a_keys, a_vals, color=C_GRN, width=0.4, alpha=0.85, zorder=3)
axC.axhline(y=accel_const, color=C_GOLD, lw=1.5, linestyle="--",
            label=f"Constant = {accel_const:.1f} m/s²")
for t, a in zip(a_keys, a_vals):
    axC.text(t, a + 0.05, f"{a:.1f}", ha="center", color=C_TEXT, fontsize=9)
axC.set_title("Acceleration vs Time (Optional)", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axC.set_xlabel("Time (s)")
axC.set_ylabel("Acceleration (m/s²)")
axC.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=9)
axC.grid(color=GRID, linestyle="--", linewidth=0.5, axis="y")
axC.set_ylim(0, accel_const * 2)

# ── Panel D: Key Results Card ─────────────────────────────────────────────
axD = fig.add_subplot(gs[1, 2])
axD.set_facecolor(CARD)
axD.axis("off")
axD.set_title("Key Results", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")

metrics = [
    ("Max velocity",      f"{velocity[max_vel_t]:.1f} m/s  @ t={max_vel_t}s"),
    ("Acceleration",      f"{accel_const:.2f} m/s²  (const.)"),
    ("Motion type",       "Uniform accel."),
    ("∫ v(t) dt",         f"{trap_distance:.2f} m"),
    ("Actual displace.",  f"{actual_displacement:.2f} m"),
    ("Error",             f"{abs(trap_distance - actual_displacement):.4f} m  ✅"),
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
             fontsize=9, color=C_TEAL, ha="right",
             va="center", fontweight="bold")

# Footer
fig.text(0.5, 0.018,
         "Muhammed Shariff Sumagka  ·  Lara Rain Fuentes  ·  Gerard Carl Palma  "
         "|  CS ELEC 01 — Computational Science",
         ha="center", fontsize=8, color=C_MUTE, fontfamily="monospace")

out = "/mnt/user-data/outputs/case2_traffic.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"✅  Visualization saved → {out}")
plt.show()
