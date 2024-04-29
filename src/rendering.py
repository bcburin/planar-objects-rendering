from typing import Callable

from PIL import Image

from src.utils import StepProvider, Region, draw_pixel, get_scale


def draw_parametric_curve(
        image: Image, f: Callable[[float], tuple[float, float]], domain: tuple[float, float],
        step_provider: StepProvider, region: Region, center: tuple[int, int] | None = None):
    a, b = domain
    if a >= b:
        raise ValueError()
    x_max, y_max = image.size
    scale_x, scale_y = get_scale(x_max, y_max, region)
    if center is None:
        center = x_max/2, y_max/2
    t = a
    while t <= b:
        x, y = f(t)
        draw_pixel(image=image, center=center, x_rel=x / scale_x, y_rel=y / scale_y)
        t += step_provider.step_at(t)


def draw_implicit_curve(
        image: Image, f: Callable[[float, float], float], region: Region, center: tuple[int, int] | None = None):
    x_max, y_max = image.size
    scale_x, scale_y = get_scale(x_max, y_max, region)
    if center is None:
        center = x_max/2, y_max/2
    for x in range(x_max):
        for y in range(y_max):
            values = [f((x - center[0] + i)*scale_x, (y - center[1] + j)*scale_y) for i in range(2) for j in range(2)]
            positive_values = [v for v in values if v >= 0]
            negative_values = [v for v in values if v <= 0]
            if len(positive_values) == 0 or len(negative_values) == 0:
                continue
            draw_pixel(image=image, x_rel=x, y_rel=y)


def draw_region(
        image: Image, pertinence_function: Callable[[float, float], bool], region: Region,
        center: tuple[int, int] | None = None):
    x_max, y_max = image.size
    scale_x, scale_y = get_scale(x_max, y_max, region)
    if center is None:
        center = x_max/2, y_max/2
    for x in range(x_max):
        for y in range(y_max):
            belongs = pertinence_function((x-center[0])*scale_x, (y - center[1])*scale_y)
            if belongs:
                draw_pixel(image=image, x_rel=x, y_rel=y)
