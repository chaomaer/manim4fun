from __future__ import annotations

import queue
import re

from manim import *

from utils import unit_vector_from_to


def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code."""
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i] * 2, 16) / div if div else
                         int(hx[i] * 2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i + 2], 16) / div if div else
                     int(hx[i:i + 2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code.')


def generate_color_ray(steps):
    start_color = hex_to_rgb("#DC75CD")
    end_color = hex_to_rgb("#FF862F")
    color_list = []

    for i in range(steps + 1):
        # 计算当前颜色
        color_cur = tuple(start + i * (end - start) / steps for start, end in zip(start_color, end_color))
        res = '#%02x%02x%02x' % (int(color_cur[0]), int(color_cur[1]), int(color_cur[2]))
        color_list.append(res)
    return color_list


class PythagorasTree(MovingCameraScene):
    def construct(self):
        # self.camera.frame.set(height=3)
        #########################
        # 创建一个正方形

        # start = Text("Pythagorean Tree")
        #
        # self.play(Write(start))
        #
        # self.play(Unwrite(start))

        side_length = 1.5
        max_depth = 8

        #####
        # self.next_color = generate_color_ray(max_depth)
        square = Square(side_length=side_length, stroke_width=4).shift(DOWN * 2.7)

        dot_b = Dot(square.get_start(), radius=0, fill_opacity=0)

        dot_a = Dot(dot_b.get_center(), radius=0, fill_opacity=0).shift(LEFT * side_length)

        v = midpoint(dot_a.get_center(), dot_b.get_center())

        dot_from = Dot(v, radius=0, fill_opacity=0).shift(DOWN * side_length)
        dot_to = Dot(v, radius=0, fill_opacity=0)

        group = VDict([('a', dot_a), ('b', dot_b), ('sq', square), ('from', dot_from), ('to', dot_to)])
        group.set_fill(BLUE, opacity=0.5)
        # 添加正方形和追踪路径到场景中
        self.play(Create(group))
        #########################

        i = 30
        all_group = [0] * 100
        #
        while i <= 60:
            result = self.create_tree(group, side_length=side_length, alpha=i * DEGREES, max_depth=max_depth,
                                      is_play=(i == 45))
            all_group[i] = result
            i = i + 1

        for i in range(45, 30, -1):
            self.play(ReplacementTransform(all_group[i], all_group[i - 1]), run_time=1 / 10)

        for i in range(30, 59):
            self.play(ReplacementTransform(all_group[i], all_group[i + 1]), run_time=1 / 10)

        for i in range(59, 45, -1):
            self.play(ReplacementTransform(all_group[i], all_group[i - 1]), run_time=1 / 10)

        # self.camera.frame.save_state()
        # self.play(self.camera.frame.animate.set(width=1))
        #
        # self.camera.frame.restore()
        #
        # # clear
        # for mobj in self.mobjects:
        #     self.remove(mobj)
        #
        # self.play(Write(Text("The End")))

    def create_tree(self, group, side_length, alpha=20 * DEGREES, max_depth=4, is_play=False):

        cur_depth = 0
        q = queue.Queue()
        q.put((group, side_length))

        cur_layer_num = 1

        all_object = []
        group = VGroup()

        while not q.empty() and cur_depth < max_depth:
            # 取出当前层数
            temp_layer_num = cur_layer_num
            cur_layer_num = 0
            ani_lis = []
            play_list = []
            # lay_color = self.next_color[cur_depth]
            for i in range(temp_layer_num):
                (c_group, size_len) = q.get()
                # c_group['sq'].set_fill(GREEN)
                # 复制两个
                copy1 = c_group.copy()
                copy1.set_fill(BLUE, opacity=0.5)
                copy2 = c_group.copy()
                copy2.set_fill(GREEN, opacity=0.5)

                perp_ab = unit_vector_from_to(c_group['from'], c_group['to'])
                pivot_a = c_group['a'].get_center()
                pivot_b = c_group['b'].get_center()

                if is_play:
                    ani1_play = copy1.animate.shift(perp_ab * size_len).scale(np.cos(alpha),
                                                                              about_point=pivot_a).rotate(
                        alpha,
                        about_point=pivot_a)
                    # ani1_play.set_color(lay_color)
                    ani2_play = copy2.animate.shift(perp_ab * size_len).scale(np.cos(PI / 2 - alpha),
                                                                              about_point=pivot_b).rotate(
                        - (PI / 2 - alpha),
                        about_point=pivot_b)
                    # ani2_play.set_color(lay_color)
                    play_list.extend([ani1_play, ani2_play])
                ani1 = copy1.shift(perp_ab * size_len).scale(np.cos(alpha), about_point=pivot_a).rotate(alpha,
                                                                                                        about_point=pivot_a)
                ani2 = copy2.shift(perp_ab * size_len).scale(np.cos(PI / 2 - alpha),
                                                             about_point=pivot_b).rotate(- (PI / 2 - alpha),
                                                                                         about_point=pivot_b)

                ani_lis.append(ani1)
                ani_lis.append(ani2)

                q.put((copy1, np.cos(alpha) * size_len))
                q.put((copy2, np.cos(PI / 2 - alpha) * size_len))

                cur_layer_num += 2
            if is_play:
                self.play(*play_list, run_time=1 / (0.8 * cur_depth + 1))
                # self.play(self.camera.frame.animate.set(height=3 + 1 * cur_depth))
                # self.play(self.camera.frame.animate.set(width=10 + cur_depth))

            for el in ani_lis:
                group.add(el)
                all_object.append(el)

            # all_object.group(el) for el in ani_lis
            # self.play(*[Create(el) for el in ani_lis])
            cur_depth += 1

        return group
