import math  # import cProfile

import matplotlib.pyplot as plt
import numpy as np

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio -> 1.618033988749895

holiday_red = '#FF4136'
holiday_green = '#2ECC40'
holiday_blue = '#0074CC'
holiday_yellow = '#FFD700'
holiday_purple = '#B10DC9'


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


def plot_days():
    """Annotate each point with day number, stars and draw lines from (0,0)"""
    offset = (-0.1) * PHI  # Adjust for precise positioning

    base_url, cur_year = 'https://adventofcode.com', 2023
    cur_yr_url = f'{base_url}/{cur_year}'

    for day in range(1, days + 1):
        index: int = scale * day
        x_pt, y_pt = x[index - 1], y[index - 1]
        tangent_angle = np.arctan2(y_pt, x_pt)
        # @formatter:off
        x_off, y_off = offset * np.cos(tangent_angle), offset * np.sin( tangent_angle)
        # @formatter:on
        nx, ny = x_pt + x_off, y_pt + y_off

        day_pos = (nx - (x_off / (PHI ** 2)), ny - (y_off / (PHI ** 2)))
        gap_x, gap_y = nx + 2 * x_off, ny + 2 * y_off
        star_pos = [{'x': (gap_x / PHI ** 3), 'y': (gap_y / PHI ** 3)},
                    {'x': (gap_x / PHI ** 1), 'y': (gap_y / PHI ** 1)}, ]

        week, day_txt_url = (day - 1) // 7, f'{cur_yr_url}/day/{day}'
        plt.scatter(x_pt, y_pt, color=(to_rgba(get_week_color(week), 1.0)),
                    marker='*', label=f'Day {day}', s=14, visible=False)
        for star in star_pos:  # Scatter plots for Stars
            plt.scatter(star['x'], star['y'], color='goldenrod', marker='*',
                        label=f'Star {star_pos.index(star) + 1}', s=12)
        # Draw line from origin to day point
        plt.plot([0, day_pos[0]], [0, day_pos[1]],
                 color=(to_rgba(get_week_color(week), PHI / (2 * np.pi))),
                 linestyle='-.', linewidth=1)
        plt.annotate(str(day), day_pos, ha='center', va='center',
                     color=holiday_green, fontweight='bold', fontsize='9',
                     url=day_txt_url)


days, scale = 25, 365
num_points = days * scale
x, y = golden_spiral(num_points)

plt.style.use('dark_background')
holiday_colors = [holiday_red, holiday_yellow, holiday_blue, holiday_purple,
                  holiday_green, ]

plt.plot(x, y, label='Golden Spiral', color='goldenrod', visible=False)
plot_days()

plt.axis('off')  # Hide axis ticks and labels
plt.axis('equal')  # Set equal aspect ratio. 1 unit of x == 1 unit of y
plt.title('Advent Of Code', color='goldenrod', fontsize='9', visible=False)

plt.show()
