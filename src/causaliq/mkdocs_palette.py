import matplotlib.pyplot as plt
import matplotlib.patches as patches

IMG_WIDTH = 12

# Color data
color_names = ["Primary", "Accent", "Text", "Background"]
light_colors = ["#2a9d8f", "#8C2F39", "#1a1a1a", "#f8f9f9"]
dark_colors = ["#3fb5a3", "#f39c6b", "#E8E8E8", "#121A1C"]
light_bg = light_colors[-1]
dark_bg = dark_colors[-1]

fig, ax = plt.subplots(figsize=(12, 7), dpi=100)
plt.xlim(0, IMG_WIDTH)
plt.ylim(0, 7)
ax.axis('off')

# Backgrounds
ax.add_patch(patches.Rectangle((0, 3.5), IMG_WIDTH, 3.5, color=light_bg,
                               zorder=0))
ax.add_patch(patches.Rectangle((0, 0), IMG_WIDTH, 3.5, color=dark_bg,
                               zorder=0))

# Swatch layout
n = len(color_names)
box_size = 1.7
x_gap = (IMG_WIDTH - n * box_size) / (n + 1)
x_positions = [x_gap + i * (box_size + x_gap) for i in range(n)]
y_light_box = 4.5  # from 5
y_dark_box = 1.0  # from 1.8

# Light theme swatches
for i, (name, hexcode) in enumerate(zip(color_names, light_colors)):
    x = x_positions[i]
    # Color box
    ax.add_patch(patches.Rectangle((x, y_light_box), box_size, box_size,
                                   color=hexcode, ec='none', zorder=2))
    # Name
    ax.text(x + box_size/2, y_light_box - 0.18, name, ha='center', va='top',
            fontsize=20, fontweight='bold', color='#23242A',
            family='DejaVu Sans')
    # Hex
    ax.text(x + box_size/2, y_light_box - 0.55, hexcode, ha='center', va='top',
            fontsize=14, color='#23242A', family='DejaVu Sans')

# Dark theme swatches
for i, (name, hexcode) in enumerate(zip(color_names, dark_colors)):
    x = x_positions[i]
    # Color box
    ax.add_patch(patches.Rectangle((x, y_dark_box), box_size, box_size,
                                   color=hexcode, ec='none', zorder=2))
    # Name
    ax.text(x + box_size/2, y_dark_box - 0.18, name, ha='center', va='top',
            fontsize=20, fontweight='bold', color='white',
            family='DejaVu Sans')
    # Hex
    ax.text(x + box_size/2, y_dark_box - 0.55, hexcode, ha='center', va='top',
            fontsize=14, color='white', family='DejaVu Sans')

# Titles
ax.text(IMG_WIDTH / 2, 6.6, "Light Theme", ha='center', va='center',
        fontsize=32, fontweight='bold', color='#23242A',
        family='DejaVu Sans')
ax.text(IMG_WIDTH / 2, 3.1, "Dark Theme", ha='center', va='center',
        fontsize=32, fontweight='bold', color='white', family='DejaVu Sans')


plt.tight_layout()
plt.show()
