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

class RotationControlNode(Node):
    def __init__(self, key_up, key_down, axis, angle=0):
        super().__init__(transform=rotate(axis, angle))
        self.angle, self.axis = angle, axis
        self.key_up, self.key_down = key_up, key_down

    def key_handler(self, key):
        self.angle += 5 * int(key == self.key_up)
        self.angle -= 5 * int(key == self.key_down)
        self.transform = rotate(self.axis, self.angle)
        super().key_handler(key)

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
    viewer = Viewer()

    # default color shader
    shader = Shader("color.vert", "color.frag")

    # place instances of our basic objects
    #viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
    #if len(sys.argv) < 2:
    #    viewer.add(Axis(shader))
    #    viewer.add(Node(children=[Cylinder(shader)], transform=translate(x=+2)))
    #    viewer.add(Node(children=[Triangle(shader)], transform=translate(x=-1)))
    #    print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
    #          ' format supported by assimp.' % (sys.argv[0],))

    # cylinder = Cylinder(shader)
    # axis = Axis(shader)
    # # viewer.add(Axis(shader))
    # #viewer.add(Node(children=[Cylinder(shader)], transform=translate(x=+2)))
    # #viewer.add(Node(children=[Triangle(shader)], transform=translate(x=-1)))

    # # make a flat cylinder
    # base_shape = Node(transform=scale(x=1, y=1, z=1))
    # base_shape.add(cylinder)                    # shape of robot base
    # # base_shape.add(axis)                    # shape of robot base

    # # make a thin cylinder
    # arm_shape = Node(transform=translate(y=1.5) @ scale(x=.5, y=1.5, z=.5))
    # arm_shape.add(cylinder)                     # shape of arm
    # # arm_shape.add(axis)                     # shape of arm

    # # make a thin cylinder
    # forearm_shape = Node(transform=translate(y=.5) @ scale(x=.3, y=.5, z=.3)) # 2*1.5 / 2
    # forearm_shape.add(cylinder)                 # shape of forearm
    # # forearm_shape.add(axis)                 # shape of forearm
    # # viewer.add(base_shape)
    # # viewer.add(arm_shape)
    # # viewer.add(forearm_shape)

    # theta = 45.0        # base horizontal rotation angle
    # phi1 = 45.0         # arm angle
    # phi2 = 20.0         # forearm angle

    # # transform_forearm = Node(transform=translate(y=1) @ rotate((0, 0, 1), (phi2)))
    # # transform_forearm.add(forearm_shape)

    # transform_arm = Node(transform=rotate((0, 0, 1), phi1))
    # transform_arm.add(arm_shape) #, transform_forearm)

    # transform_base = Node(transform=rotate((0, 1, 0), theta))
    # transform_base.add(base_shape, transform_arm)
    # viewer.add(transform_base)
    # # start rendering loop
    # viewer.run()
    cylinder = Cylinder(shader)
    theta = 35.0        # base horizontal rotation angle
    phi1 = 25.0         # arm angle

    base_shape = Node(transform=scale(.5, .1, .5))
    base_shape.add(cylinder)

    arm_shape = Node(transform=translate(0, .5, 0) @ scale(.1, .5, .1))
    arm_shape.add(cylinder)

    forearm_shape = Node(transform=translate(y=.5) @ scale(x=.3, y=.5, z=.3)) # 2*1.5 / 2
    forearm_shape.add(cylinder)                 # shape of forearm
    viewer.add(base_shape)
    viewer.add(arm_shape)
    viewer.add(forearm_shape)

    # rotation_arm = RotationControlNode(glfw.KEY_UP, glfw.KEY_DOWN, (0, 0, 1), angle=phi1)
    # rotation_arm.add(arm_shape)

    # transform_base = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, (0, 1, 0), angle=theta)
    # transform_base.add(base_shape)
    # transform_base.add(rotation_arm)

    # viewer.add(transform_base)  # only this root node is added to the viewer
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
