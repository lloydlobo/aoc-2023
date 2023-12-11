from cProfile import run
from datetime import datetime
from typing import Any, Callable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patheffects import withStroke
from numpy import ndarray, dtype

timestamp = datetime.now().strftime('%Y%m%d')  # '%Y%m%d%H%M%S'

PHI: float = (1 + np.sqrt(5)) / 2  # Golden ratio -> 1.618033988749895
DAY_OUTER_SPIRAL_OFFSET: float = (-0.1 * PHI)  # Adjust for precise positioning

PHI_INVERSE: float = 1 / PHI
PHI_SQUARE: float = PHI ** 2
PHI_SQUARE_INVERSE: float = 1 / PHI_SQUARE
PHI_CUBE: float = PHI ** 3
PHI_CUBE_INVERSE: float = 1 / PHI_CUBE
PI_INVERSE: float = 1 / np.pi

PLT_DAY_ORIGIN_LINE_WIDTH = PHI / np.sqrt(np.pi)
PLT_INNER_LINE_ALPHA = PI_INVERSE
PLT_OUTER_LINE_ALPHA = PHI * PI_INVERSE

holiday_red = '#FF7272'  # A deep, warm red
holiday_green = '#6FFF6F'  # A vibrant, holiday-themed green
holiday_green_glow = '#00FF00'  # A bright green glow for emphasis
holiday_blue = '#8C8CFF'  # A rich, dark blue for contrast
holiday_yellow = '#FFE066'  # A soft, golden yellow
holiday_purple = '#D872E8'  # A muted purple for a touch of elegance
holiday_night_bg = '#1A1A33'  # A deep, dark background for the night sky

holiday_colors = [holiday_red, holiday_yellow, holiday_blue, holiday_purple,
                  holiday_green]


def golden_spiral(num_points: int):
    """
    # >>> num_points = 100
    # >>> x, y = golden_spiral(num_points)
    # >>> assert (len(x) == len(y) == num_points)
    -> tuple[ndarray]:
    """
    theta: ndarray[Any, dtype[float | Any]]
    radius: ndarray | Any

    assert (isinstance(num_points, int)
            and f'"num_points" should be instance of type int')
    theta = np.linspace(0, 2 * np.pi, num_points)
    radius = np.exp(0.1 * theta)
    x_arr, y_arr = (radius * np.cos(theta)), (radius * np.sin(theta))
    return x_arr, y_arr


def get_week_color(week: int) -> str:
    return holiday_colors[week % len(holiday_colors)]


def to_rgba(hex_str: str, alpha: float = 1.0) -> tuple[Any, ...]:
    """
    Use bitwise operations to extract the red, green, and blue components
    from the 24-bit hexadecimal value

    @output:
         hex color code `#ffffff` to the RGBA tuple `(1.0, 1.0, 1.0, 1.0)`
    """
    assert (0.0 <= alpha <= 1.0 and 'Expected 0.0 <= alpha <= 1.0')
    hex_val = int(hex_str[1:], 16)  # hex.replace('#', '') == hex[1:]
    r: int = (hex_val >> 16) & 255
    g: int = (hex_val >> 8) & 255
    b: int = (hex_val & 255)
    rgb: list[int] = [r, g, b]
    rgb_color = np.array(rgb).astype(float) / 255.0
    return tuple(np.append(rgb_color, alpha))


def compute_coordinates(offset: float):
    coordinates = []

    for day in range(1, days + 1):
        index: int = scale * day
        x_pt, y_pt = x[index - 1], y[index - 1]

        tangent_angle = np.arctan2(y_pt, x_pt)
        x_off, y_off = (offset * np.cos(tangent_angle),
                        offset * np.sin(tangent_angle))

        nx, ny = x_pt + x_off, y_pt + y_off
        day_coords = nx - (x_off * PHI_SQUARE_INVERSE), ny - (
                y_off * PHI_SQUARE_INVERSE)

        gap_x, gap_y = nx + 2 * x_off, ny + 2 * y_off
        star_coords = [
            {'x': (gap_x * PHI_CUBE_INVERSE), 'y': (gap_y * PHI_CUBE_INVERSE)},
            {'x': (gap_x * PHI_INVERSE), 'y': (gap_y * PHI_INVERSE)}, ]

        coordinates.append((day_coords, star_coords, x_pt, y_pt))

    return coordinates


def plot_days(coordinates):
    """Annotate each point with day number, stars and draw lines from (0,0)"""
    base_url, cur_year = 'https://adventofcode.com', timestamp[:4]

    star_glow_color = to_rgba(holiday_yellow, 0.05 * PHI)

    for day in range(1, days + 1):
        day_pos, star_pos, x_pt, y_pt = coordinates[day - 1]

        week, day_txt_url = (day - 1) // 7, f'{base_url}/{cur_year}/day/{day}'
        week_color = get_week_color(week)

        # if False:  # Outer spiral points
        #     plt.scatter(x_pt, y_pt, color=(to_rgba(week_color, 0.5)),
        #                 marker='*', label=f'Day {day}', s=4, visible=True)

        for pe in path_effects_stars:  # Add elements with glow effect for stars
            for star in star_pos:  # Scatter plots for Stars
                plt.scatter(star['x'], star['y'], color=star_glow_color,
                            marker='*', path_effects=[pe],
                            s=14 if star_pos.index(star) + 1 == 2 else 7)
        for star in star_pos:  # Scatter plots for Stars
            index_star_ = star_pos.index(star) + 1
            plt.scatter(star['x'], star['y'], color='goldenrod', marker='*',
                        label=f'Day {day}: Star {index_star_}',
                        s=12 if index_star_ == 2 else 5)

        for pe in path_effects_text:  # Add text elements with the stroke effect
            plt.text(s=str(day), x=day_pos[0], y=day_pos[1], ha='center',
                     va='center', color='none', fontweight='bold', fontsize='9',
                     path_effects=[pe])
        plt.annotate(str(day), day_pos, ha='center', va='center',
                     color=holiday_green, fontweight='bold', fontsize='9',
                     url=day_txt_url)

        # Draw line from origin to day point ([0, day_pos[0]], [0, day_pos[1]])
        plt.plot([star_pos[0]['x'], star_pos[1]['x']],
                 [star_pos[0]['y'], star_pos[1]['y']],
                 color=(to_rgba(week_color, PLT_INNER_LINE_ALPHA)),
                 linestyle='dotted',
                 linewidth=PLT_DAY_ORIGIN_LINE_WIDTH)  # inner
        plt.plot([star_pos[1]['x'], day_pos[0]], [star_pos[1]['y'], day_pos[1]],
                 color=(to_rgba(week_color, PLT_OUTER_LINE_ALPHA)),
                 linestyle='dotted',
                 linewidth=PLT_DAY_ORIGIN_LINE_WIDTH)  # outer


def run_plt():
    global days, scale, x, y, path_effects_text, path_effects_stars

    days, scale = 25, 100  # 25, 365
    num_points: int = days * scale

    x, y = golden_spiral(num_points)

    # fig, ax = plt.subplots()
    plt.style.use('dark_background')
    plt.rcParams.update({"figure.facecolor": holiday_night_bg, })

    common_stroke: Callable[[Any], list[withStroke]] = lambda color: [
        withStroke(linewidth=5 * PHI_INVERSE,
                   foreground=to_rgba(color, 0.025 * PHI)),
        withStroke(linewidth=3 * PHI_INVERSE,
                   foreground=to_rgba(color, 0.05 * PHI)),
        withStroke(linewidth=2 * PHI_INVERSE,
                   foreground=to_rgba(color, 0.1 * PHI))
    ]  # Create a stroke path effect to simulate glow
    path_effects_text = common_stroke(holiday_green_glow)
    path_effects_stars = common_stroke('#FFE066')

    # if False:
    #     plt.plot(x, y, label='Golden Spiral',
    #              color=to_rgba(holiday_yellow, 0.3), visible=False)

    # coordinates = compute_coordinates(
    #   offset=(-0.1 * PHI), days=days, scale=scale, x=x, y=y)
    coordinates = compute_coordinates(offset=DAY_OUTER_SPIRAL_OFFSET)
    plot_days(coordinates)  # plot_days(ax, coordinates, days, holiday_night_bg)

    # ax.axis('off')  # Hide axis ticks and labels
    # ax.axis('equal')  # Set equal aspect ratio. 1 unit of x == 1 unit of y
    plt.axis('off')  # Hide axis ticks and labels
    plt.axis('equal')  # Set equal aspect ratio. 1 unit of x == 1 unit of y

    plt.title('Advent Of Code', color='goldenrod', fontsize='9', visible=False)

    return plt  # return fig


def main():
    updated_plt = run_plt()  # updated_fig = run_plt()

    f_out_name = f'{timestamp}-aoc-{timestamp[:4]}'
    updated_plt.savefig(f'{f_out_name}.png', transparent=True,
                        facecolor=holiday_night_bg)
    updated_plt.savefig(f'{f_out_name}.pdf', format='pdf',
                        facecolor=holiday_night_bg)
    # updated_plt.show()

    return 0


if __name__ == '__main__':
    """
    20231211172846
         1511728 function calls (1486125 primitive calls) in 2.644 seconds
    20231211171848
         1511728 function calls (1486125 primitive calls) in 2.677 seconds
    20231211171549
         1511730 function calls (1486127 primitive calls) in 2.647 seconds
    20231211171308
         1511730 function calls (1486127 primitive calls) in 2.702 seconds
    20231211170558
         1512451 function calls (1486848 primitive calls) in 2.726 seconds
    20231211165006
         1511580 function calls (1485977 primitive calls) in 2.822 seconds
    20231211164741
         1511580 function calls (1485977 primitive calls) in 3.336 seconds
    20231211162416
         1515913 function calls (1490264 primitive calls) in 2.974 seconds
    20231211162108
         1515963 function calls (1490314 primitive calls) in 3.194 seconds
    20231211161429
         1644487 function calls (1617063 primitive calls) in 3.200 seconds
    20231211160929
         1644950 function calls (1617526 primitive calls) in 3.334 seconds
    20231211152352
         1644487 function calls (1617063 primitive calls) in 3.504 seconds
    """
    print(datetime.now().strftime('%Y%m%d%H%M%S'))
    run('main()', sort='cumulative')
