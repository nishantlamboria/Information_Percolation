import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Arc


# Matplotlib LaTeX settings
plt.rcParams.update({
    'text.usetex': True,
    'font.family': 'serif',
    'font.size': 14,
    'text.latex.preamble': r'\usepackage{amsmath}',
})

# Time and cutoff function
t = np.linspace(0, 10, 500)
t_mix = 5
sharpness = 2.5
raw_tanh = np.tanh(-sharpness * (t - t_mix))
d_n_t = 0.5 * (raw_tanh + 1)

# Scale to [0.01, 0.99]
lower, upper = 0.01, 0.99
d_n_t = lower + (upper - lower) * d_n_t

# Epsilon and key transition points
epsilon = 0.09
t_eps_idx = np.argmin(np.abs(d_n_t - epsilon))
t_1meps_idx = np.argmin(np.abs(d_n_t - (1 - epsilon)))
t_eps = t[t_eps_idx]
t_1meps = t[t_1meps_idx]

# Colors and styles
curve_color = '#9A393A'
highlight_color = '#EF7F1A'
dash_color = 'gray'
dash_alpha = 0.5

# Plot setup
fig, ax = plt.subplots(figsize=(7, 4.5))

# Highlight mixing window
ax.axvspan(t_eps, t_1meps, color=highlight_color, alpha=0.12, zorder=0)

# Main curve
ax.plot(t, d_n_t, color=curve_color, linewidth=2.5, zorder=3)

# Horizontal dashed lines (only up to curve)
ax.plot([0, t_eps], [epsilon, epsilon], linestyle='--', color=dash_color, linewidth=1, alpha=dash_alpha)
ax.plot([0, t_1meps], [1 - epsilon, 1 - epsilon], linestyle='--', color=dash_color, linewidth=1, alpha=dash_alpha)

# Vertical dashed lines at t_eps and t_1meps
ax.axvline(x=t_eps, linestyle='--', color=dash_color, linewidth=1, alpha=dash_alpha)
ax.axvline(x=t_1meps, linestyle='--', color=dash_color, linewidth=1, alpha=dash_alpha)

# Vertical dotted line at T_n
ax.axvline(x=t_mix, linestyle=':', color='black', linewidth=1)

# ε and 1−ε labels (closer to axis)
ax.annotate(r'$\varepsilon$', xy=(0, epsilon), xytext=(-8, 0),
            textcoords='offset points', va='center', ha='right', fontsize=11)

ax.annotate(r'$1 - \varepsilon$', xy=(0, 1 - epsilon), xytext=(-8, 0),
            textcoords='offset points', va='center', ha='right', fontsize=11)

# Add intersection marker dots
ax.plot(t_eps, epsilon, 'o', color=curve_color, markersize=5)
ax.plot(t_1meps, 1 - epsilon, 'o', color=curve_color, markersize=5)

# X-axis labels (clean spacing, clear order)
# ax.annotate(r'$T_n - t_\varepsilon$', 
#             xy=(t_eps, 0), xytext=(10, -20),
#             textcoords='offset points', ha='center', va='top', fontsize=9.5)

ax.annotate(r'$T_n$', xy=(t_mix, 0), xytext=(0, -20),
            textcoords='offset points', ha='center', va='top', fontsize=9.5)

# ax.annotate(r'$T_n + t_\varepsilon$', 
#             xy=(t_1meps, 0), xytext=(-10, -20),
#             textcoords='offset points', ha='center', va='top', fontsize=9.5)

# Keep only the T_n label
# ax.annotate(r'$T_n$', xy=(t_mix, 0), xytext=(0, -20),
#             textcoords='offset points', ha='center', va='top', fontsize=10.5)

# Right-side label with arrow pointing to the window

# --- Double-headed arrow directly above the window ---
arrow = FancyArrowPatch((t_eps, 1.02), (t_1meps, 1.02),
                        arrowstyle='<->', mutation_scale=10,
                        color='black', linewidth=1.2)
ax.add_patch(arrow)

# --- Curved arrow from above the window to the right side ---
arc = FancyArrowPatch(
    posA=((t_eps + t_1meps)/2, 1.02), posB=(7, 0.75),
    connectionstyle="arc3,rad=0.3",
    arrowstyle='->', color=dash_color, linewidth=1.1
)
ax.add_patch(arc)

# --- Text label on the right side ---
ax.annotate(
    r'$\boxed{w_n = o(T_n)}$',
    xy=(7, 0.75),
    ha='left', va='center',
    fontsize=15
)



# Y ticks and label
ax.set_yticks([0, 1])
ax.set_yticklabels(['0', '1'])
ax.set_ylabel(r'$d_{\mathrm{TV}}^{(n)}$', fontsize=13)

# No x-ticks
ax.set_xticks([])
ax.set_xlim([0, 10])
ax.set_ylim([-0.05, 1.05])

# Clean spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Optional title
# ax.set_title(r'\textbf{The Cutoff Phenomenon}', fontsize=14, pad=15)

# Save as PDF for LaTeX use (optional)
plt.savefig("cutoff_plot.pdf", bbox_inches='tight', transparent=True)

plt.tight_layout()
plt.show()