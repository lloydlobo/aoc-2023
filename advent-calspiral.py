import cProfile
import math
from datetime import datetime
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patheffects import withStroke

# import matplotlib as mpl
# mpl.font_manager._rebuild()
# pip install matplotlib-sourcecodepro-font

# import matplotlib.font_manager as fm
# from matplotlib import rcParams
#
# Force Matplotlib to update the font cache
# prop = fm.FontProperties(
#     fname=fm.findfont(fm.FontProperties(family='Source Code Pro')))
#
# Set the default font for numbers
# rcParams['font.family'] = 'Source Code Pro'
# rcParams['font.size'] = 9

timestamp = datetime.now().strftime('%Y%m%d')  # '%Y%m%d%H%M%S'

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio -> 1.618033988749895

holiday_red = '#FF7272'  # A deep, warm red
holiday_green = '#6FFF6F'  # A vibrant, holiday-themed green
holiday_green_glow = '#00FF00'  # A bright green glow for emphasis
holiday_blue = '#8C8CFF'  # A rich, dark blue for contrast
holiday_yellow = '#FFE066'  # A soft, golden yellow
holiday_purple = '#D872E8'  # A muted purple for a touch of elegance
holiday_night_bg = '#1A1A33'  # A deep, dark background for the night sky

holiday_colors = [holiday_red, holiday_yellow, holiday_blue, holiday_purple,
                  holiday_green]


def golden_spiral(num_points):
    """
    @usage:
        days, scale = 25, 365
        scale = 365
        x, y = golden_spiral(num_points)
        x = array([1.        , 1.00006863, 1.00013679, ..., 1.87419616, 1.87432656, 1.87445609])
        y = array([ 0.00000000e+00,  6.88691091e-04,  1.37747671e-03, ..., -2.58130847e-03, -1.29074342e-03, -4.59109330e-16])
    """
    angle_rad = min((PHI * math.atan2(num_points, PHI)), 2)  # 2.541315..
    theta = np.linspace(0, angle_rad * np.pi, num_points)
    radius = np.exp(0.1 * theta)
    x, y = (radius * np.cos(theta)), (radius * np.sin(theta))
    return x, y


def get_week_color(week):
    return holiday_colors[week % len(holiday_colors)]


def to_rgba(hex, alpha: float = 1.0):
    """
    Use bitwise operations to extract the red, green, and blue components
    from the 24-bit hexadecimal value

    @output:
         hex color code `#ffffff` to the RGBA tuple `(1.0, 1.0, 1.0, 1.0)`
    """
    assert (0.0 <= alpha <= 1.0 and 'Expected 0.0 <= alpha <= 1.0')
    hex_val = int(hex[1:], 16)  # hex.replace('#', '') == hex[1:]
    r, g, b = (hex_val >> 16) & 255, (hex_val >> 8) & 255, hex_val & 255
    rgb_color = np.array([r, g, b]).astype(float) / 255.0
    return tuple(np.append(rgb_color, alpha))


def compute_coordinates(offset):
    coordinates = []
    for day in range(1, days + 1):
        index: int = scale * day
        x_pt, y_pt = x[index - 1], y[index - 1]

        tangent_angle = np.arctan2(y_pt, x_pt)
        x_off, y_off = offset * np.cos(tangent_angle), offset * np.sin(
            tangent_angle)
        nx, ny = x_pt + x_off, y_pt + y_off
        day_coords = (nx - (x_off / (PHI ** 2)), ny - (y_off / (PHI ** 2)))
        gap_x, gap_y = nx + 2 * x_off, ny + 2 * y_off
        star_coords = [{'x': (gap_x / PHI ** 3), 'y': (gap_y / PHI ** 3)},
                       {'x': (gap_x / PHI ** 1), 'y': (gap_y / PHI ** 1)}, ]

        coordinates.append((day_coords, star_coords, x_pt, y_pt))
    return coordinates


def plot_days():
    """Annotate each point with day number, stars and draw lines from (0,0)"""
    base_url, cur_year = 'https://adventofcode.com', timestamp[:4]
    offset = -0.1 * PHI  # Adjust for precise positioning
    coordinates = compute_coordinates(offset)

    for day in range(1, days + 1):
        day_pos, star_pos, x_pt, y_pt = coordinates[day - 1]

        week, day_txt_url = (day - 1) // 7, f'{base_url}/{cur_year}/day/{day}'

        plt.scatter(x_pt, y_pt, color=(to_rgba(get_week_color(week), 1.0)),
                    marker='*', label=f'Day {day}', s=14, visible=False)

        # Draw line from origin to day point ([0, day_pos[0]], [0, day_pos[1]])
        plt.plot([star_pos[0]['x'], star_pos[1]['x']],
                 [star_pos[0]['y'], star_pos[1]['y']],
                 color=(to_rgba(get_week_color(week), PHI / (1 * np.pi))),
                 linestyle='dotted', linewidth=PHI / np.sqrt(np.pi))
        plt.plot([star_pos[1]['x'], day_pos[0]], [star_pos[1]['y'], day_pos[1]],
                 color=(to_rgba(get_week_color(week), PHI / (PHI * np.pi))),
                 linestyle='dotted', linewidth=PHI / np.sqrt(np.pi))

        # Add additional text elements with the stroke effect for stars
        for pe in path_effects_stars:
            for star in star_pos:  # Scatter plots for Stars
                plt.scatter(star['x'], star['y'],
                            color=to_rgba(holiday_yellow, 0.05 * PHI),
                            marker='*', path_effects=[pe], s=14)
        for star in star_pos:  # Scatter plots for Stars
            plt.scatter(star['x'], star['y'], color='goldenrod', marker='*',
                        label=f'Star {star_pos.index(star) + 1}', s=12)

        # Add additional text elements with the stroke effect
        for pe in path_effects_text:
            plt.annotate(str(day), day_pos, ha='center', va='center',
                         color='none', fontweight='bold', fontsize='9',
                         url=day_txt_url, path_effects=[pe])
        # Create a main text element for the day number
        _main_text = plt.annotate(str(day), day_pos, ha='center', va='center',
                                  color=holiday_green, fontweight='bold',
                                  fontsize='9', url=day_txt_url)


def run_plt():
    global days, scale, x, y, path_effects_text, path_effects_stars

    days, scale = 25, 100  # 25, 365
    num_points = days * scale

    x, y = golden_spiral(num_points)

    plt.style.use('dark_background')

    # Customize colors for dark background
    # @formatter:off
    plt.rcParams.update({
        "figure.facecolor": holiday_night_bg, # Background color for entire figure
        # "axes.facecolor": "#111111",    # Background color for the axes
        # "axes.edgecolor": "#555555",    # Color of the axes' edges
        # "axes.labelcolor": "white",     # Color of axis labels
        # "text.color": "white",          # Color of text
        # "xtick.color": "white",         # Color of x-axis ticks
        # "ytick.color": "white"          # Color of y-axis ticks
    })
    # @formatter:on

    # Create a stroke path effect to simulate glow
    common_stroke = lambda color: [
        withStroke(linewidth=5 / PHI, foreground=to_rgba(color, 0.025 * PHI)),
        withStroke(linewidth=3 / PHI, foreground=to_rgba(color, 0.05 * PHI)),
        withStroke(linewidth=2 / PHI, foreground=to_rgba(color, 0.1 * PHI))
    ]
    path_effects_text = common_stroke(holiday_green_glow)
    path_effects_stars = common_stroke('#FFE066')

    plt.plot(x, y, label='Golden Spiral', color='goldenrod', visible=False)

    plot_days()

    plt.axis('off')  # Hide axis ticks and labels
    plt.axis('equal')  # Set equal aspect ratio. 1 unit of x == 1 unit of y
    plt.title('Advent Of Code', color='goldenrod', fontsize='9', visible=False)

    return plt


def main():
    updated_plt: matplotlib.pyplot = run_plt()
    # @formatter:off
    outfile_name = f'{timestamp}-aoc-{timestamp[:4]}'
    updated_plt.savefig(f'{outfile_name}.png', transparent=True, facecolor=holiday_night_bg)
    updated_plt.savefig(f'{outfile_name}.pdf', format='pdf', facecolor=holiday_night_bg)
    # updated_plt.show()
    # @formatter:on

    return 0


if __name__ == '__main__':
    cProfile.run('main()', sort='cumulative')
