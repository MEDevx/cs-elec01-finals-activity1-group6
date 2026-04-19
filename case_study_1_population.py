"""
================================================================================
  CS ELEC 01 — COMPUTATIONAL SCIENCE
  Finals Activity 1  |  Case Study 1: Population Growth Analysis
================================================================================

  Course      : CS ELEC 01 – Computational Science
  Activity    : Finals Activity 1 – Numerical Methods Case Studies
  Topic       : Population Growth Analysis Using Numerical Methods

  Group Members:
    • Muhammed Shariff Sumagka
    • Lara Rain Fuentes
    • Gerard Carl Palma

  Institution : College of Engineering and Information Technology
                Department of Computing and Library Information Science

  Description:
    A local government wants to analyze how population changes over time.
    Using only discrete yearly data (not a continuous function), this script:
      1. Estimates population growth rate via Numerical Differentiation
         using the Central Difference Method.
      2. Estimates total cumulative population change via Numerical Integration
         using the Trapezoidal Rule.
      3. Fits an exponential growth model and predicts population for 2025.
      4. Produces a multi-panel visualization dashboard with analysis.

  Numerical Methods:
    ┌─────────────────────────────────────────────────────────────────────┐
    │  Central Difference:  f'(xᵢ) ≈ [f(xᵢ₊₁) – f(xᵢ₋₁)] / 2          │
    │  Trapezoidal Rule:    ∫ f(x) dx ≈ (h/2) Σ [f(xᵢ) + f(xᵢ₊₁)]      │
    └─────────────────────────────────────────────────────────────────────┘

  Dependencies : numpy, matplotlib, scipy
  Install      : pip install numpy matplotlib scipy
  Usage        : python case_study_1_population.py

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
    from scipy.optimize import curve_fit
except ImportError as e:
    sys.exit(f"[ERROR] Missing dependency: {e}\nInstall: pip install numpy matplotlib scipy")

# ══════════════════════════════════════════════════════════════════════════════
#  DATASET
# ══════════════════════════════════════════════════════════════════════════════
years      = np.array([2020, 2021, 2022, 2023, 2024], dtype=float)
population = np.array([10_000, 10_800, 11_900, 13_200, 14_800], dtype=float)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — Numerical Differentiation (Central Difference)
#  f'(xᵢ) ≈ [f(xᵢ₊₁) – f(xᵢ₋₁)] / 2
#  Applied at interior points: years 2021, 2022, 2023
# ══════════════════════════════════════════════════════════════════════════════
growth_rate: dict[int, float] = {}
for i in range(1, len(years) - 1):
    growth_rate[int(years[i])] = (population[i + 1] - population[i - 1]) / 2.0

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — Numerical Integration (Trapezoidal Rule)
#  ∫₂₀₂₀²⁰²⁴ P(t) dt — represents cumulative person-years 2020–2024
# ══════════════════════════════════════════════════════════════════════════════
trap_total = np.trapezoid(population, years)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — Exponential Regression + 2025 Prediction
#  Model: P(t) = a · exp(b · t),  t = year – 2020  (normalised)
# ══════════════════════════════════════════════════════════════════════════════
def exponential_model(t: np.ndarray, a: float, b: float) -> np.ndarray:
    """Exponential growth model: P(t) = a * exp(b * t)."""
    return a * np.exp(b * t)

t_norm           = years - 2020
popt, _          = curve_fit(exponential_model, t_norm, population, p0=[10_000, 0.1])
a_fit, b_fit     = popt
pred_2025        = exponential_model(5.0, *popt)   # t_norm(2025) = 5
doubling_time    = np.log(2) / b_fit

t_fine    = np.linspace(0, 5.5, 300)
pop_curve = exponential_model(t_fine, *popt)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — Analysis
# ══════════════════════════════════════════════════════════════════════════════
yoy_change = np.diff(population)
yoy_years  = years[1:].astype(int)

gr_years       = sorted(growth_rate.keys())
accelerations  = {
    gr_years[i]: growth_rate[gr_years[i]] - growth_rate[gr_years[i - 1]]
    for i in range(1, len(gr_years))
}
max_accel_yr  = max(accelerations, key=accelerations.get)
max_accel_val = accelerations[max_accel_yr]

# ══════════════════════════════════════════════════════════════════════════════
#  CONSOLE REPORT
# ══════════════════════════════════════════════════════════════════════════════
LINE  = "═" * 62
line  = "─" * 62

print(f"\n{LINE}")
print("  CS ELEC 01  |  CASE STUDY 1 — POPULATION GROWTH ANALYSIS")
print(LINE)
print("  Group: Sumagka · Fuentes · Palma")
print(LINE)

print(f"\n  GIVEN DATA")
print(f"  {'Year':<8} {'Population':>14}")
print(f"  {'─'*24}")
for yr, pop in zip(years.astype(int), population.astype(int)):
    print(f"  {yr:<8} {pop:>14,}")

print(f"\n  STEP 1 — Central Difference (Growth Rate)")
print(f"  Formula : f'(xᵢ) ≈ [f(xᵢ₊₁) – f(xᵢ₋₁)] / 2")
print(f"\n  {'Year':<8} {'Population':>14}  {'Growth Rate (ppl/yr)':>22}")
print(f"  {'─'*48}")
for yr, pop in zip(years.astype(int), population.astype(int)):
    r = growth_rate.get(yr)
    rs = f"{r:>12,.1f}" if r is not None else f"{'N/A (endpoint)':>22}"
    print(f"  {yr:<8} {pop:>14,}  {rs:>22}")

print(f"\n  STEP 2 — Trapezoidal Rule (Integration)")
print(f"  Formula : ∫ P(t) dt ≈ (h/2) Σ [P(tᵢ) + P(tᵢ₊₁)]")
print(f"  Result  : ∫₂₀₂₀²⁰²⁴ P(t) dt  ≈  {trap_total:>12,.2f}  person-years")

print(f"\n  STEP 3 — Exponential Model & Prediction")
print(f"  Model    : P(t) = {a_fit:,.2f} × e^({b_fit:.4f}·t)  [t = year – 2020]")
print(f"  Growth   : {b_fit*100:.2f}% continuous growth per year")
print(f"  Doubling : {doubling_time:.2f} years")
print(f"  ⟹  Predicted Population (2025) ≈ {pred_2025:,.0f} people")

print(f"\n  STEP 4 — Analysis")
print(f"  Year-over-Year Changes:")
for yr, δ in zip(yoy_years, yoy_change.astype(int)):
    bar = "█" * int(δ / 100)
    print(f"    {yr}: +{δ:>5,}  {bar}")
print(f"  Growth accelerated most in {max_accel_yr}  (Δ rate = +{max_accel_val:,.0f} ppl/yr)")
print(f"  Growth type   : EXPONENTIAL  (b = {b_fit:.4f} > 0)")
print(f"  2025 Forecast : ≈ {pred_2025:,.0f} people")
print(f"\n{LINE}\n")

# ══════════════════════════════════════════════════════════════════════════════
#  VISUALIZATION  — Dark Navy Scientific Dashboard
# ══════════════════════════════════════════════════════════════════════════════
BG      = "#07101f"
PANEL   = "#0c1a2e"
CARD    = "#0f2035"
GRID    = "#172840"
C_BLUE  = "#38bdf8"
C_ORG   = "#fb923c"
C_LIME  = "#86efac"
C_GOLD  = "#fbbf24"
C_TEXT  = "#dde6f0"
C_MUTED = "#4e6a85"

plt.rcParams.update({
    "font.family"       : "monospace",
    "text.color"        : C_TEXT,
    "axes.labelcolor"   : C_MUTED,
    "xtick.color"       : C_MUTED,
    "ytick.color"       : C_MUTED,
    "axes.edgecolor"    : GRID,
    "figure.facecolor"  : BG,
    "axes.facecolor"    : PANEL,
    "axes.spines.top"   : False,
    "axes.spines.right" : False,
})

fig = plt.figure(figsize=(16, 11))
fig.patch.set_facecolor(BG)

# Header
fig.text(0.5, 0.975,
         "▸  CASE STUDY 1  ·  POPULATION GROWTH ANALYSIS",
         ha="center", fontsize=14, fontweight="bold",
         color=C_BLUE, fontfamily="monospace")
fig.text(0.5, 0.950,
         "CS ELEC 01 — Computational Science  |  Central Difference & Trapezoidal Rule",
         ha="center", fontsize=9, color=C_MUTED, fontfamily="monospace")

gs = gridspec.GridSpec(2, 3, figure=fig,
                       top=0.925, bottom=0.075,
                       hspace=0.52, wspace=0.38,
                       left=0.07, right=0.96)

# ── Panel A: Population vs Time (full width) ──────────────────────────────
axA = fig.add_subplot(gs[0, :])
axA.set_facecolor(CARD)
axA.plot(t_fine + 2020, pop_curve, color=C_BLUE, lw=1.6,
         linestyle="--", alpha=0.5, label="Exponential fit")
axA.scatter(years, population, color=C_BLUE, s=100, zorder=6,
            edgecolors="white", linewidths=0.7, label="Observed data")
axA.scatter([2025], [pred_2025], color=C_GOLD, s=180,
            marker="*", zorder=7, label=f"2025 Prediction ≈ {pred_2025:,.0f}")
for yr, pop in zip(years.astype(int), population.astype(int)):
    axA.annotate(f"  {pop:,}", (yr, pop), fontsize=8.5, color=C_TEXT, va="center")
axA.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))
axA.set_title("Population vs Time  (2020–2025)", fontsize=12, color=C_TEXT,
              pad=10, loc="left", fontweight="bold")
axA.set_xlabel("Year")
axA.set_ylabel("Population")
axA.legend(facecolor=CARD, edgecolor=GRID, labelcolor=C_TEXT, fontsize=9)
axA.grid(color=GRID, linestyle="--", linewidth=0.5)
axA.set_xlim(2019.5, 2025.9)

# ── Panel B: Growth Rate Bar Chart ────────────────────────────────────────
axB = fig.add_subplot(gs[1, 0])
axB.set_facecolor(CARD)
gr_vals = [growth_rate[y] for y in gr_years]
bars = axB.bar(gr_years, gr_vals, color=C_ORG, width=0.5,
               alpha=0.85, zorder=3, edgecolor="none")
for bar, val in zip(bars, gr_vals):
    axB.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 12, f"{val:,.0f}",
             ha="center", color=C_TEXT, fontsize=8.5)
axB.set_title("Growth Rate  (ppl / yr)", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axB.set_xlabel("Year")
axB.set_ylabel("ppl / yr")
axB.grid(color=GRID, linestyle="--", linewidth=0.5, axis="y")
axB.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

# ── Panel C: Year-over-Year Change ────────────────────────────────────────
axC = fig.add_subplot(gs[1, 1])
axC.set_facecolor(CARD)
axC.plot(yoy_years, yoy_change, color=C_LIME, lw=2.2,
         marker="o", markersize=8, zorder=4)
axC.fill_between(yoy_years, yoy_change, alpha=0.15, color=C_LIME)
for yr, δ in zip(yoy_years, yoy_change.astype(int)):
    axC.annotate(f"+{δ:,}", (yr, δ), textcoords="offset points",
                 xytext=(0, 9), ha="center", fontsize=8.5, color=C_TEXT)
axC.set_title("Year-over-Year Δ Population", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")
axC.set_xlabel("Year")
axC.set_ylabel("Δ People")
axC.grid(color=GRID, linestyle="--", linewidth=0.5)
axC.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.0f}"))

# ── Panel D: Key Results Card ─────────────────────────────────────────────
axD = fig.add_subplot(gs[1, 2])
axD.set_facecolor(CARD)
axD.axis("off")
axD.set_title("Key Results", fontsize=11, color=C_TEXT,
              pad=8, loc="left", fontweight="bold")

metrics = [
    ("∫ P(t) dt",        f"{trap_total:,.0f} person-yrs"),
    ("Growth const b",   f"{b_fit:.4f} / yr"),
    ("Doubling time",    f"{doubling_time:.2f} yrs"),
    ("Peak accel year",  f"{max_accel_yr}"),
    ("2025 Forecast",    f"{pred_2025:,.0f} people"),
]
for k, (label, value) in enumerate(metrics):
    y = 0.82 - k * 0.18
    rect = plt.Rectangle((0.02, y - 0.08), 0.96, 0.14,
                          transform=axD.transAxes,
                          facecolor=GRID, edgecolor="none", zorder=1)
    axD.add_patch(rect)
    axD.text(0.07, y, label, transform=axD.transAxes,
             fontsize=8.5, color=C_MUTED, va="center")
    axD.text(0.95, y, value, transform=axD.transAxes,
             fontsize=9.5, color=C_BLUE, ha="right",
             va="center", fontweight="bold")

# Footer
fig.text(0.5, 0.018,
         "Muhammed Shariff Sumagka  ·  Lara Rain Fuentes  ·  Gerard Carl Palma  "
         "|  CS ELEC 01 — Computational Science",
         ha="center", fontsize=8, color=C_MUTED, fontfamily="monospace")

out = "/mnt/user-data/outputs/case1_population.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"✅  Visualization saved → {out}")
plt.show()
