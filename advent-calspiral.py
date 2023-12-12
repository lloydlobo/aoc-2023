from cProfile import run
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patheffects import withStroke
from numpy import ndarray, dtype

timestamp = datetime.now().strftime('%Y%m%d')  # '%Y%m%d%H%M%S'

# PHI: float = (1 + np.sqrt(5)) / 2  # Golden ratio -> 1.618033988749895
PHI = 1.61803398875
PHI_INVERSE = 0.61803398875
PHI_SQUARE = 2.61803398875
PHI_SQUARE_INVERSE = 0.38196601125
PHI_CUBE = 4.2360679775
PHI_CUBE_INVERSE = 0.2360679775
PI = 3.14159265358979323846
PI_INVERSE = 0.31830988618

PLT_DAY_OUTER_SPIRAL_OFFSET: float = (-0.1 * PHI)  # Adjust for precise positioning
PLT_DAY_ORIGIN_LINE_WIDTH = PHI / np.sqrt(np.pi)
PLT_INNER_ORIGIN_LINE_ALPHA = 1 * (PHI_CUBE_INVERSE ** PHI)
PLT_INNER_LINE_ALPHA = PI_INVERSE
PLT_OUTER_LINE_ALPHA = PHI * PI_INVERSE

holiday_red = '#FF7272'  # A deep, warm red
holiday_green = '#6FFF6F'  # A vibrant, holiday-themed green
holiday_green_glow = '#00FF00'  # A bright green glow for emphasis
holiday_blue = '#8C8CFF'  # A rich, dark blue for contrast
holiday_yellow = '#FFE066'  # A soft, golden yellow
holiday_purple = '#D872E8'  # A muted purple for a touch of elegance
holiday_night_bg = '#1A1A33'  # A deep, dark background for the night sky
holiday_night_bg = '#0A0A16'  # A deep, dark background for the night sky

holiday_colors = [holiday_red, holiday_yellow, holiday_blue, holiday_purple,
                  holiday_green]
LEN_HOLIDAY_COLORS = len(holiday_colors)


def golden_spiral(num_points: int):
    """
    # >>> num_points = 100
    # >>> x, y = golden_spiral(num_points)
    # >>> assert (len(x) == len(y) == num_points)
    -> tuple[ndarray]:
    """
    theta: ndarray[Any, dtype[float | Any]]
    radius: ndarray | Any
    assert (isinstance(num_points, int) and f'"num_points" should be instance of type int')
    theta = np.linspace(0, 2 * np.pi, num_points)
    radius = np.exp(0.1 * theta)
    x_arr, y_arr = (radius * np.cos(theta)), (radius * np.sin(theta))
    return x_arr, y_arr


def get_week_color(week: int) -> str:
    return holiday_colors[week % LEN_HOLIDAY_COLORS]


def to_rgba(hex_str: str, alpha: float = 1.0) -> tuple[Any, ...]:
    """
    Use bitwise operations to extract the red, green, and blue components
    from the 24-bit hexadecimal value

    @output:
         hex color code `#ffffff` to the RGBA tuple `(1.0, 1.0, 1.0, 1.0)`
    """
    assert (0.0 <= alpha <= 1.0 and 'Expected 0.0 <= alpha <= 1.0')
    hex_val = int(hex_str[1:], 16)  # hex.replace('#', '') == hex[1:]
    r = (hex_val >> 16) & 255
    g = (hex_val >> 8) & 255
    b = (hex_val & 255)
    rgb: list[int] = [r, g, b]
    rgb_color = np.array(rgb).astype(float) / 255.0
    return tuple(np.append(rgb_color, alpha))


def compute_np_coordinates(offset: float, days: int, scale: int, x: np.ndarray, y: np.ndarray) -> dict[
    str, ndarray[Any, dtype[float]] | tuple[float, float] | list[dict[str, float]]]:
    """
        indices: ndarray[Any, dtype[signedinteger[Any]]]
        x_pts: ndarray[Any, dtype[float]]
        y_pts: ndarray[Any, dtype[float]]
        nx: ndarray[Any, dtype[float]]
        ny: ndarray[Any, dtype[float]]
        days_pts: tuple[float, float]
        stars_pts: list[dict[str, float]]
    """
    indices = np.arange(1, days + 1) * scale
    x_pts, y_pts = x[indices - 1], y[indices - 1]
    tangent_angles = np.arctan2(y_pts, x_pts)
    x_offsets, y_offsets = offset * np.cos(tangent_angles), offset * np.sin(tangent_angles)
    nx, ny = x_pts + x_offsets, y_pts + y_offsets
    days_pts = (nx - (x_offsets * PHI_SQUARE_INVERSE), ny - (y_offsets * PHI_SQUARE_INVERSE))
    gap_x, gap_y = nx + (2 * x_offsets), ny + (2 * y_offsets)
    stars_pts = [{'x': (gap_x * var_scale), 'y': (gap_y * var_scale)} for var_scale in [PHI_CUBE_INVERSE, PHI_INVERSE]]
    return dict(x_pts=x_pts, y_pts=y_pts, days_pts=days_pts, stars_pts=stars_pts)


def plot_days(np_coordinates):
    """Annotate each point with day number, stars and draw lines from (0,0)"""
    base_url, cur_year = 'https://adventofcode.com', timestamp[:4]
    alphas = [PLT_INNER_ORIGIN_LINE_ALPHA, PLT_INNER_LINE_ALPHA, PLT_OUTER_LINE_ALPHA]
    path_effects_text = [withStroke(linewidth=5 * PHI_INVERSE, foreground=to_rgba(holiday_green_glow, 0.025 * PHI)),
                         withStroke(linewidth=3 * PHI_INVERSE, foreground=to_rgba(holiday_green_glow, 0.05 * PHI))]

    x_pts, y_pts, days_pts, stars_pts = np_coordinates.values()
    star1_pts, star2_pts = stars_pts

    star1_x_pts, star1_y_pts = star1_pts.values()
    star2_x_pts, star2_y_pts = star2_pts.values()
    day_x_pts, day_y_pts = days_pts

    for day in range(1, days + 1):
        idx = day - 1
        week = idx // 7
        week_color = get_week_color(week)

        sqrtday = np.sqrt(day)
        star_size = 4 * PHI * sqrt
        alpha_gradient_day = PI_INVERSE * np.arctan(1 / day % PHI)

        # Scatter plot for stars
        plt.scatter([star1_x_pts[idx], star2_x_pts[idx]], [star1_y_pts[idx], star2_y_pts[idx]],
                    label=f'Day {day}: Stars', s=[star_size / sqrtday, star_size], marker='*',
                    color=to_rgba(hex_str=holiday_yellow, alpha=(PHI_INVERSE - alpha_gradient_day)))

        # Annotation and text
        plt.text(s=str(day), x=day_x_pts[idx], y=day_y_pts[idx], ha='center', va='center', color='none',
                 fontweight='bold', fontsize='9', path_effects=path_effects_text)
        plt.annotate(str(day), (day_x_pts[idx], day_y_pts[idx]), ha='center', va='center', color=holiday_green,
                     fontweight='bold', fontsize='9', url=f'{base_url}/{cur_year}/day/{day}')

        # Lines between stars and day positions
        plt.plot([star1_x_pts[idx] * PHI_CUBE_INVERSE, star1_x_pts[idx]],
                 [star1_y_pts[idx] * PHI_CUBE_INVERSE, star1_y_pts[idx]], color=(to_rgba(week_color, alphas[0])),
                 linestyle=':', linewidth=PLT_DAY_ORIGIN_LINE_WIDTH)
        plt.plot([star1_x_pts[idx], star2_x_pts[idx]], [star1_y_pts[idx], star2_y_pts[idx]],
                 color=(to_rgba(week_color, alphas[1])), linestyle=':', linewidth=PLT_DAY_ORIGIN_LINE_WIDTH)
        plt.plot([star2_x_pts[idx], day_x_pts[idx]], [star2_y_pts[idx], day_y_pts[idx]],
                 color=(to_rgba(week_color, alphas[2])), linestyle=':', linewidth=PLT_DAY_ORIGIN_LINE_WIDTH)


def run_plt():
    global days, scale, x, y

    days, scale = 25, 100  # 25, 365
    num_points: int = days * scale
    # todo: or create cocentric spirals of tapering scale instead of generating offset coordinates
    x, y = golden_spiral(num_points)

    plt.style.use('dark_background')  # fig, ax = plt.subplots()
    plt.rcParams.update({"figure.facecolor": holiday_night_bg, })

    np_coordinates = compute_np_coordinates(offset=(-0.1 * PHI), days=days, scale=scale, x=x, y=y)
    plot_days(np_coordinates)

    plt.axis('off')  # Hide axis ticks and labels
    plt.axis('equal')  # Set equal aspect ratio. 1 unit of x == 1 unit of y

    return plt  # return fig


def plot_trivial_title_outline(x, y):
    if False:
        plt.plot(x, y, label='Golden Spiral', color=to_rgba(holiday_yellow, 0.3), visible=False)
        plt.title('Advent Of Code', color='goldenrod', fontsize='9', visible=False)


def main():
    updated_plt = run_plt()  # updated_fig = run_plt()
    f_out_name = f'{timestamp}-aoc-{timestamp[:4]}'
    updated_plt.savefig(f'{f_out_name}.png', transparent=True, facecolor=holiday_night_bg)
    updated_plt.savefig(f'{f_out_name}.pdf', format='pdf', facecolor=holiday_night_bg)
    # updated_plt.show()
    return 0


if __name__ == '__main__':
    print(datetime.now().strftime('%Y%m%d%H%M%S'))
    run('main()', sort='cumulative')

"""
20231212130334 541461 function calls (530939 primitive calls) in 1.181 seconds
20231212124946
         541463 function calls (530941 primitive calls) in 1.177 seconds
   Ordered by: cumulative time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    178/1    0.005    0.000    1.178    1.178 {built-in method builtins.exec}
        1    0.000    0.000    1.178    1.178 advent-calspiral.py:257(main)
        2    0.000    0.000    0.699    0.349 pyplot.py:1114(savefig)
        2    0.000    0.000    0.698    0.349 figure.py:3234(savefig)
        2    0.000    0.000    0.698    0.349 backend_bases.py:2052(print_figure)
        1    0.000    0.000    0.479    0.479 advent-calspiral.py:217(run_plt)
        1    0.002    0.002    0.475    0.475 advent-calspiral.py:136(plot_days)
20231212103213 583058 function calls (571211 primitive calls) in 1.266 seconds
20231212100035 579605 function calls (567858 primitive calls) in 1.291 seconds
20231212075456 
        579375 function calls (567628 primitive calls) in 1.211 seconds
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    178/1    0.005    0.000    1.212    1.212 {built-in method builtins.exec}
        1    0.000    0.000    1.212    1.212 advent-calspiral.py:256(main)
        2    0.000    0.000    0.746    0.373 pyplot.py:1114(savefig)
        2    0.000    0.000    0.746    0.373 figure.py:3234(savefig)
        2    0.000    0.000    0.746    0.373 backend_bases.py:2052(print_figure)
        2    0.000    0.000    0.470    0.235 backend_bases.py:2043(<lambda>)
        1    0.000    0.000    0.466    0.466 advent-calspiral.py:219(run_plt)
        1    0.001    0.001    0.461    0.461 advent-calspiral.py:176(plot_days)
20231212075146 579377 function calls (567630 primitive calls) in 1.243 seconds
20231212042804 579331 function calls (567584 primitive calls) in 1.402 seconds
20231212042408 579331 function calls (567584 primitive calls) in 1.647 seconds
20231212041556 579356 function calls (567609 primitive calls) in 1.549 seconds
20231212040114 691669 function calls (678212 primitive calls) in 1.568 seconds
20231212035500 691531 function calls (678074 primitive calls) in 2.156 seconds
20231212032905 653848 function calls (641145 primitive calls) in 1.585 seconds
20231212032510 653860 function calls (641157 primitive calls) in 1.588 seconds
20231211181756 598318 function calls (586944 primitive calls) in 1.267 seconds
20231211181618 598318 function calls (586944 primitive calls) in 1.275 seconds
20231211181323 598318 function calls (586944 primitive calls) in 1.415 seconds
20231211181239 653860 function calls (641157 primitive calls) in 1.391 seconds
20231211181047 709448 function calls (695416 primitive calls) in 1.674 seconds
20231211180413 709491 function calls (695459 primitive calls) in 1.486 seconds
20231211175747 709516 function calls (695484 primitive calls) in 1.519 seconds
20231211175720 709516 function calls (695484 primitive calls) in 1.660 seconds
20231211173759 1477913 function calls (1453819 primitive calls) in 2.689 seconds
20231211172846 1511728 function calls (1486125 primitive calls) in 2.644 seconds
20231211171848 1511728 function calls (1486125 primitive calls) in 2.677 seconds
20231211171549 1511730 function calls (1486127 primitive calls) in 2.647 seconds
20231211171308 1511730 function calls (1486127 primitive calls) in 2.702 seconds
20231211170558 1512451 function calls (1486848 primitive calls) in 2.726 seconds
20231211165006 1511580 function calls (1485977 primitive calls) in 2.822 seconds
20231211164741 1511580 function calls (1485977 primitive calls) in 3.336 seconds
20231211162416 1515913 function calls (1490264 primitive calls) in 2.974 seconds
20231211162108 1515963 function calls (1490314 primitive calls) in 3.194 seconds
20231211161429 1644487 function calls (1617063 primitive calls) in 3.200 seconds
20231211160929 1644950 function calls (1617526 primitive calls) in 3.334 seconds
20231211152352 1644487 function calls (1617063 primitive calls) in 3.504 seconds
"""
