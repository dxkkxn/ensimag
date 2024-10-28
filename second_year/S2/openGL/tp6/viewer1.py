#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale
from animation import KeyFrames, KeyFrameControlNode
from transform import vec, quaternion, quaternion_from_euler, quaternion_from_axis_angle


class Axis(Mesh):
    """ Axis object useful for debugging coordinate frames """
    def __init__(self, shader):
        pos = ((0, 0, 0), (1, 0, 0), (0, 0, 0), (0, 1, 0), (0, 0, 0), (0, 0, 1))
        col = ((1, 0, 0), (1, 0, 0), (0, 1, 0), (0, 1, 0), (0, 0, 1), (0, 0, 1))
        super().__init__(shader, attributes=dict(position=pos, color=col))

    def draw(self, primitives=GL.GL_LINES, **uniforms):
        super().draw(primitives=primitives, **uniforms)


class Triangle(Mesh):
    """Hello triangle object"""
    def __init__(self, shader):
        position = np.array(((0, .5, 0), (-.5, -.5, 0), (.5, -.5, 0)), 'f')
        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1)), 'f')
        self.color = (1, 1, 0)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)

    def key_handler(self, key):
        if key == glfw.KEY_C:
            self.color = (0, 0, 0)


class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader))  # just load cylinder from file


# -------------- main program and scene setup --------------------------------

def main():
    """ create a window, add scene objects, then run rendering loop """
    my_keyframes = KeyFrames({0: 1, 3: 7, 6: 20})
    print(my_keyframes.value(1.5))
    vector_keyframes = KeyFrames({0: vec(1, 0, 0), 3: vec(0, 1, 0), 6: vec(0, 0, 1)})
    print(vector_keyframes.value(1.5))   # should display numpy vector (0.5, 0.5, 0)
    viewer = Viewer()
    shader = Shader("color.vert", "color.frag")

    # translate_keys = {0: vec(0, 0, 10), 2: vec(10, 0, 0), 3:vec(-10, 0, 0),
    #                   4: vec(-10, 0, -10)}
    # translate_keys = = {}
    # rotate_keys = {0: quaternion_from_axis_angle(vec(0, 0, 1), 0),
    #                2: quaternion_from_axis_angle(vec(0, 1, 0), 0),
    #                3: quaternion_from_axis_angle(vec(1, 0, 0), 0),
    #                4: quaternion_from_axis_angle(vec(0, 0, 1), 0)
    #               }

    # rotate_keys = {0: quaternion_from_axis_angle(vec(0, 0, 1), 0),
    #             2: quaternion_from_axis_angle(vec(0, 0, 1), 0),
    #             3: quaternion_from_axis_angle(vec(0, 0, 1), 0),
    #             4: quaternion_from_axis_angle(vec(0, 0, 1), 0)
    #             }
    # rotate_keys = {0: identity(),
    #                2: identity(),
    #                3: identity(),
    #                4: identity()
    #             }
    # scale_keys = {0: 1, 2: 1, 4: 1}
    import math
    translate_keys, rotate_keys, scale_keys = {}, {}, {}
    for i, theta in enumerate(range(0, 361, 20)):
        theta = math.radians(theta)
        translate_keys[i*2] = 10*vec(math.cos(theta), 0, math.sin(theta))
        rotate_keys[i*2] = quaternion_from_axis_angle(vec(1, 0, 0), 45)
        scale_keys[i*2] = 1
    # rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
    #                3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(Cylinder(shader))
    viewer.add(keynode)
    viewer.add(Axis(shader))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
