import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['text.usetex'] = False  # Use mathtext, not full LaTeX

# Define points and labels
x_start, x_end = 0, 1
internal_points = [0.175, 0.35, 0.725]
labels = [
    r'$\frac{\theta}{2}$',
    r'$\theta$',
    r'$p(\sigma,v)+\frac{\theta}{2}$'
]

# Create plot
fig, ax = plt.subplots(figsize=(3, 1.25))
y = 0

# Colored segments only (no black line)
x_middle = internal_points[1]
# Softer and vivid colors
soft_blue = '#91c9f7'
vivid_blue = 'blue'
vivid_red = 'red'
soft_red = '#f7a8a8'

# Left soft blue
ax.hlines(y=y, xmin=x_start, xmax=internal_points[0], color=vivid_blue, linewidth=6)
# Vivid blue segment
ax.hlines(y=y, xmin=internal_points[0], xmax=x_middle, color=vivid_red, linewidth=6)
# Vivid red segment
ax.hlines(y=y, xmin=x_middle, xmax=internal_points[2], color=soft_blue, linewidth=6)
# Right soft red
ax.hlines(y=y, xmin=internal_points[2], xmax=x_end, color=soft_red, linewidth=6)



# End bars and endpoint labels
bar_height = 0.15
ax.vlines([x_start, x_end], y - bar_height, y + bar_height, color='black', linewidth=2)
ax.text(x_start + 0.025, y - 0.06, '0', ha='center', va='top', fontsize=11)
ax.text(x_end - 0.025, y - 0.06, '1', ha='center', va='top', fontsize=11)

# Internal bars and math labels
for i, x in enumerate(internal_points):
    color = 'black' if i == 1 else 'gray'
    ax.vlines(x, y - bar_height / 2, y + bar_height / 2, color=color, linewidth=2)
    ax.text(x, y + 0.1, labels[i], ha='center', va='bottom', fontsize=10)

# Final touches
ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.3, 0.4)
ax.axis('off')

plt.tight_layout()
plt.savefig("01_plot_post.pdf", format="pdf", bbox_inches="tight")
plt.show()