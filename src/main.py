from math import pi, cos, sin

from PIL import Image

from src.rendering import draw_parametric_curve, draw_implicit_curve, draw_region
from src.utils import AdaptiveStepProvider, UniformStepProvider, get_data_dir


def q1_parametric():
    def circle(t: float) -> tuple[float, float]:
        return cos(t), sin(t)

    im = Image.new("RGB", (200, 200), color="black")
    draw_parametric_curve(
        image=im, f=circle, domain=(0, 2 * pi), step_provider=UniformStepProvider(10e-3), region=((-1, 1), (-1, 1)))
    im.save(get_data_dir() / 'q1_parametric.png')


def q1_implicit():
    im = Image.new("RGB", (200, 200), color="black")
    draw_implicit_curve(image=im, f=lambda x, y: 1 - x**2 - y**2, region=((-1, 1), (-1, 1)))
    im.save(get_data_dir() / 'q1_implicit.png')


def q2_uniform():
    im = Image.new("RGB", (200, 200), color="black")
    draw_parametric_curve(
        image=im, f=lambda t: (t*cos(t), t*sin(t)), domain=(0, 100), region=((-100, 100), (-100, 100)),
        step_provider=UniformStepProvider(10e-1))
    im.save(get_data_dir() / 'q2_uniform.png')


def q2_adaptive():
    def func(t: float) -> tuple[float, float]:
        return t * cos(t), t * sin(t)

    im = Image.new("RGB", (200, 200), color="black")
    draw_parametric_curve(
        image=im, f=func, domain=(0, 100), region=((-100, 100), (-100, 100)),
        step_provider=AdaptiveStepProvider(f=func))
    im.save(get_data_dir() / 'q2_adaptive.png')


def q3():
    im = Image.new("RGB", (200, 200), color="black")
    draw_region(
        image=im, region=((0, 1), (0, 1)), center=(0, 0),
        pertinence_function=lambda x, y: x + y > 1 and x ** 2 + (y - 1) ** 2 <= 1 and (x - 1) ** 2 + y ** 2 <= 1)
    im.save(get_data_dir() / 'q3.png')


def q4():
    im = Image.new("RGB", (200, 200), color="black")
    draw_implicit_curve(image=im, f=lambda x, y: y**2 - x**3 + x, region=((-2, 2), (-2, 2)))
    im.save(get_data_dir() / 'q4.png')


if __name__ == '__main__':
    q1_implicit()
    q1_parametric()
    q2_uniform()
    q2_adaptive()
    q3()
    q4()
