from abc import ABC, abstractmethod
from functools import cache
from math import sqrt
from pathlib import Path
from typing import Callable

from PIL import Image, ImageColor


class StepProvider(ABC):
    @abstractmethod
    def step_at(self, t: float):
        ...


class UniformStepProvider(StepProvider):
    def __init__(self, step: float):
        if step < 0:
            raise ValueError()
        self._step = step

    def step_at(self, t: float):
        return self._step


class AdaptiveStepProvider(StepProvider):

    def __init__(self, f: Callable, h: float = 10e-3):
        self._f = f
        self._h = h

    def _derivative_at(self, t: float) -> tuple[float, float]:
        x0, y0 = self._f(t)
        x, y = self._f(t + self._h)
        return (x-x0)/self._h, (y-y0)/self._h

    def step_at(self, t: float):
        xp, yp = self._derivative_at(t)
        return 1/sqrt(xp**2 + yp**2)


Region = tuple[tuple[float, float], tuple[float, float]]


@cache
def get_project_dir() -> Path:
    current_dir = Path(__file__)
    return current_dir.parent.parent


@cache
def get_data_dir() -> Path:
    return get_project_dir() / 'data'


def draw_pixel(image: Image, x_rel: float, y_rel: float, center: tuple[int, int] = (0, 0), color: str = 'white'):
    x = int(center[0] + x_rel)
    y = int(center[1] + y_rel)
    max_x, max_y = image.size
    if x >= max_x or y >= max_y:
        return
    image.putpixel((x, y), ImageColor.getrgb(color=color))


def get_scale(x_max, y_max, region: Region) -> tuple[float, float]:
    scale_x = (region[0][1] - region[0][0]) / x_max
    scale_y = (region[1][1] - region[1][0]) / y_max
    return scale_x, scale_y
