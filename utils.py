import numpy as np
from manim import *

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)



def unit_vector_from_to(point_from, point_to):
    """ Returns the unit vector of the vector.  """
    (from_x, from_y, _) = point_from.get_center()
    (to_x, to_y, _) = point_to.get_center()
    vector = np.array([to_x-from_x, to_y-from_y, 0])
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    angle = np.arctan2(v1[1], v1[0]) - np.arctan2(v2[1], v2[0])
    return angle


def perpen_direction(point_a, point_b : Dot):
    (x1, y1, _) = point_a.get_center()
    (x2, y2, _) = point_b.get_center()

    v_ab = Line3D(np.array([x1, y1, 0]), np.array([x2, y2, 0]))
    v_per = Line3D.perpendicular_to(v_ab, ORIGIN)
    v_per = Line(v_per.get_start(), v_per.get_end())
    ret = v_per.get_unit_vector()
    vector_ab = np.array([x2-x1, y2-y1, 0])
    if angle_between(ret, vector_ab) > 0:
        return ret
    else:
        return -1 * ret

