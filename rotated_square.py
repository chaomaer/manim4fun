from __future__ import annotations

from manim import *


def next_edge_size(cur_size, degree):
    m = np.tan(degree * DEGREES)
    temp = 1.0 * m * cur_size / (m + 1)
    return temp / np.sin(degree * DEGREES)


class RotatedSquare(Scene):
    def construct(self):
        square_list = []
        cur_size = 22 * 2.5
        alpha = 5
        v_group = []
        for i in range(30):
            square1 = Square(side_length=0.1)
            v_group.append(square1)
            # square_list.append(square1.animate.rotate((i * alpha) * DEGREES).scale(2))
            square_list.append(square1.animate.rotate(((90 + i * alpha) * DEGREES)).scale(cur_size))

            cur_size = next_edge_size(cur_size, alpha)

        self.play(LaggedStart(
            *square_list,
            lag_ratio=0.4,
            run_time=15
        ))
        self.play(LaggedStart(
            *[Uncreate(el) for el in v_group[::-1]],
            lag_ratio=0,
            run_time=1
        ))
        self.wait()

