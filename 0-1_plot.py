import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True  # Use LaTeX rendering

# Define points and labels
x_start, x_end = 0, 1
x_middle = 0.55  # Only the central bar is now used

label = r'$p(\sigma,v)$'

# Create plot
fig, ax = plt.subplots(figsize=(3, 1.25))
y = 0

# Softer and vivid colors
soft_blue = '#91c9f7'
vivid_blue = 'blue'
vivid_red = 'red'
soft_red = '#f7a8a8'

# Color segments: soft blue | vivid blue | vivid red | soft red
# ax.hlines(y=y, xmin=x_start, xmax=0.08, color=soft_blue, linewidth=6)
ax.hlines(y=y, xmin=0, xmax=x_middle, color=soft_blue, linewidth=6)
ax.hlines(y=y, xmin=x_middle, xmax=1, color=soft_red, linewidth=6)
# ax.hlines(y=y, xmin=0.92, xmax=x_end, color=soft_red, linewidth=6)

# End bars and endpoint labels
bar_height = 0.15
ax.vlines([x_start, x_end], y - bar_height, y + bar_height, color='black', linewidth=2)
ax.text(x_start + 0.025, y - 0.06, '0', ha='center', va='top', fontsize=11)
ax.text(x_end - 0.025, y - 0.06, '1', ha='center', va='top', fontsize=11)

# Only the middle bar and its label
ax.vlines(x_middle, y - bar_height / 2, y + bar_height / 2, color='black', linewidth=2)
ax.text(x_middle, y + 0.1, label, ha='center', va='bottom', fontsize=10)

# Final touches
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.3, 0.4)
ax.axis('off')

plt.tight_layout()
plt.savefig("01_plot.pdf", format="pdf", bbox_inches="tight")
plt.show()
