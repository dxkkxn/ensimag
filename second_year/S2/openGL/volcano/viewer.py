#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import sys                          # for system arguments

# External, non built-in modules
import OpenGL.GL as GL              # standard Python OpenGL wrapper
from OpenGL.GLU import *              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL
from itertools import cycle
import math
from random import random, randint
from texture import Texture, Textured

from core import Shader, Mesh, Viewer, Node, load
from transform import translate, identity, rotate, scale, vec
from tree import *

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
    #     y
    #     |
    #     |
    #     |
    # ---------x
        position = np.array(((-.5, 0, 0), (.5, 0, 0), (0, 1, 0)), 'f')
        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1)), 'f')
        self.color = (1, 1, 0)
        attributes = dict(position=position, color=color)
        super().__init__(shader, attributes=attributes, index=(0, 1, 2, 0, 2, 1))

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, global_color=self.color, **uniforms)

    def key_handler(self, key):
        if key == glfw.KEY_C:
            self.color = (0, 0, 0)


class Cylinder(Node):
    """ Very simple cylinder based on provided load function """
    def __init__(self, shader):
        super().__init__()
        # self.add(*load('cylinder.obj', shader))  # just load cylinder from file
        self.add(CylinderMesh(shader))


class Cone(Mesh):

    def __init__(self, shader):
        h = 1
        position = []
        position.append((0, 0, 0))
        position.append((0, h, 0))
        position.append((1, 0, 0)) # cos(0), 0, sin(0)
        index = []
        step = 20
        for i, theta in enumerate(range(step, 361, step)):
            i += 3
            theta = math.radians(theta)
            position.append((math.cos(theta), 0, math.sin(theta)))
            index.append((0, i-1, i))
            index.append((1, i, i-1))

        index = np.array(index, np.uint32)
        super().__init__(shader=shader, attributes=dict(position=position), index=index)

class Branch(Mesh):

    def circle(self, model, offset):
        position = []
        center = vec(0, 0, 0, 1)
        position.append((model @ center)[:-1])
        first = vec(1, 0, 0, 1) # cos(0), 0, sin(0)
        position.append((model @ first)[:-1])
        index = []
        for i, theta in enumerate(range(self.step, 361, self.step)):
            i += 2 + offset
            theta = math.radians(theta)
            n_coord = vec(math.cos(theta), 0, math.sin(theta), 1)
            position.append((model @ n_coord)[:-1])
            index.append((offset, i, i-1))
        return position, index;


    def __init__(self, shader, models=None, base_model=identity()):
        self.step = 20 # degrees step
        position, index = self.circle(model=base_model, offset=0)
        base_length = len(position)
        for k, model in enumerate(models):
            new_positions, new_indexes = self.circle(model=model, offset=len(position))
            position.extend(new_positions)
            index.extend(new_indexes)
            # create the sides of the cylinder
            for i in range(1, base_length-1):
                j = i + base_length*(k+1)
                index.append((i, j, j+1))
                index.append((i, j+1, i+1))

        #     position, in = []
        #     v = vec((0, h, 0, 0))
        #     position.append((r @ v)[:-1])
        #     index = []
        #     tex_coord = [(0,0), (0,0)] # ((0, 0), (0, 1), (1, 0), (1, 1))
        #     for theta in range(0, 361, 20):
        #         theta = math.radians(theta)
        #         tex_coord.append((theta, 0))
        #         tex_coord.append((theta, 1))
        #         position.append((math.cos(theta), 0, math.sin(theta)))
        #         v = vec(math.cos(theta), h, math.sin(theta), 0)
        #         position.append((r @ v)[:-1])
        #         if theta != 0:
        #             i = len(position)-2
        #             index.extend((i, 0, i-2))  # 0 center lower circle
        #             index.extend((i-1, 1, i+1))  # 1 center upper circle

        #             index.extend((i-1, i+1, i))  # 1 center upper circle
        #             index.extend((i, i-2, i-1))

        # index = np.array(index, np.uint32)
        super().__init__(shader=shader, attributes=dict(position=position), index=index)

class LeafBranch(Node):
    def __init__(self, children=(), transform=identity()):
        super().__init__(children=children, transform=transform)
        shader = Shader("texture.vert", "texture.frag")
        self.leaf = Node(children=(Leaf(shader, "branch_tree.png"),), transform=translate(x=-1) @ scale(1, 1, 1))
        self.add(self.leaf)
    def draw(self, model=identity(), **other_uniforms):
        GL.glDisable(GL.GL_CULL_FACE)   # backface culling enabled (TP2)
        GL.glDisable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)
        super().draw(model=model, **other_uniforms)
        GL.glEnable(GL.GL_CULL_FACE)   # backface culling enabled (TP2)
        GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)






class Tree(Node):
    """Hierarchical randomised modeling of a tree using Cylinders"""
    def __init__(self, shader, children=(), transform=identity()):
        super().__init__(children=children, transform=transform)
        self.leaf = Node(children=(LeafBranch(),))
        self.cylinder = Cylinder(shader)
        trunk_shape = Node(transform=scale(.02, .4, .02))
        trunk_shape.add(self.cylinder)
        transform_trunk = Node()
        transform_trunk.add(trunk_shape)
        self.depth = 5;
        x = self.branch(4, .4)
        transform_trunk.add(*x)
        self.add(transform_trunk)
    def branch(self, depth, height):
        if depth == 0 :
            return
        maxh = .95 * height
        minh = .50 * height
        nh = random() * (maxh-minh) + minh
        width = .02 - (.02*(.1*(self.depth - depth)))
        # if depth == 1:
        #     nh = 3
        res = []
        if depth == 1:
            # display leafs
            nb_leaf = randint(0, 1)
            nb_branches = 0
            for _ in range(nb_leaf):
                r = randint(-180, 180) #22.5 # random()*90-45
                r2 = randint(-180, 180) #22.5 # random()*90-45
                r3 = randint(-180, 180) #22.5 # random()*90-45
                transform = Node(transform=translate(y=height) @ rotate((1, 0, 0), r) @ rotate((0, 0, 1), r2) @ rotate((0, 1, 0), r3))
                transform.add(self.leaf)
                res.append(transform)
            return res
        branch = Node(transform=scale(width, nh, width))
        branch.add(self.cylinder)
        nb_branches = randint(1, 4)
        for _ in range(nb_branches):
            r = randint(-35, 35) #22.5 # random()*90-45
            r2 = randint(-35, 35) #22.5 # random()*90-45
            transform = Node(transform=translate(y=height) @ rotate((1, 0, 0), r) @ rotate((0, 0, 1), r2))
            transform.add(branch)
            sub_branches = self.branch(depth-1, nh)
            if sub_branches:
                transform.add(*sub_branches);
            res.append(transform)
        return res


        # return res
    # def branch(self, depth, height):
    #     if depth == 0 :
    #         return
    #     nh = height - height*.2 # new_heigh
    #     branch = Node(transform=scale(1, nh, 1))
    #     branch.add(self.cylinder)

    #     r = random()*90-45
    #     r = 22.5 # random()*90-45
    #     res = []
    #     transform_right = Node(transform=translate(y=height) @ rotate((-1, 0, 0), r))
    #     if random() > 0.2:
    #         transform_right.add(branch)
    #         sub_branches = self.branch(depth-1, nh)
    #         if sub_branches:
    #             transform_right.add(*sub_branches);
    #     transform_left = Node(transform=translate(y=height) @ rotate((0.5, 0, .866), r))
    #     if random() > 0.2 :

    #         transform_left.add(branch)
    #         sub_branches = self.branch(depth-1, nh)
    #         if sub_branches:
    #             transform_left.add(*sub_branches);

    #     transform = Node(transform=translate(y=height) @ rotate((0.5, 0, -.866), r))
    #     if random() > 0.2 :
    #         transform.add(branch)
    #         sub_branches = self.branch(depth-1, nh)
    #         if sub_branches:
    #             transform.add(*sub_branches);
    #     return [transform, transform_left, transform_right];
        # trunk_shape.add(branch_shape)
        # theta = 35.0        # base horizontal rotation angle
        # phi1 = 25.0         # arm angle

        # base_shape = Node(transform=scale(.5, .1, .5))
        # base_shape.add(cylinder)
        # # viewer.add(base_shape)

        # arm_shape = Node(transform=translate(0, .5, 0) @ scale(.1, .5, .1))
        # arm_shape.add(cylinder)

        # forearm_shape = Node(transform=translate(y=.5) @ scale(x=.3, y=.5, z=.3)) # 2*1.5 / 2
        # forearm_shape.add(cylinder)                 # shape of forearm
        # viewer.add(base_shape)
        # viewer.add(arm_shape)
        # viewer.add(forearm_shape)

        # rotation_arm = RotationControlNode(glfw.KEY_UP, glfw.KEY_DOWN, (0, 0, 1), angle=phi1)
        # rotation_arm.add(arm_shape)

        # transform_base = RotationControlNode(glfw.KEY_LEFT, glfw.KEY_RIGHT, (0, 1, 0), angle=theta)
        # transform_base.add(base_shape)
        # transform_base.add(rotation_arm)

        # viewer.add(transform_base)  # only this root node is added to the viewer

# -------------- Example textured plane class ---------------------------------
class Leaf(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file1):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file1

        # setup plane mesh to be textured
        base_coords = ((0, 0, 0), (2, 0, 0), (0, 2, 0), (2, 2, 0))
        tex_coord = ((0, 0), (1, 0), (0, 1), (1, 1))
        tex_coord = tuple(reversed(list(tex_coord)))
        # scaled = 5 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 3, 0, 3, 2), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=base_coords, tex_coord=tex_coord), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file1, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)
    # def draw(self, primitives=GL.GL_TRIANGLES, **other_uniforms):
    #     GL.glDisable(GL.GL_CULL_FACE)   # backface culling enabled (TP2)
    #     GL.glDisable(GL.GL_DEPTH_TEST)
    #     super().draw(primitives, other_uniforms)
    #     GL.glEnable(GL.GL_CULL_FACE)   # backface culling enabled (TP2)
    #     GL.glEnable(GL.GL_DEPTH_TEST)  # depth test now enabled (TP2)

class TexturedCylinder(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        # setup plane mesh to be textured
        # base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        # scaled = 100 * np.array(base_coords, np.float32)
        # indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = CylinderMesh(shader) #, attributes=dict( tex_coord=tex_coord), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)

class SkyBox(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        base_coords = (
                        # Front Face
                        ( -1.000000, 1.000000, 1.000000),
                        ( -1.000000, -1.000000, 1.000000),
                        ( 1.000000, -1.000000, 1.000000),
                        ( 1.000000, 1.000000, 1.000000),

                        # Left Face
                        ( -1.000000 ,1.000000 ,1.000000),
                        ( -1.000000 ,-1.000000, 1.000000),
                        ( -1.000000 ,-1.000000, -1.000000),
                        ( -1.000000 ,1.000000 ,-1.000000),

                        # Right Face
                        ( 1.000000, 1.000000, 1.000000),
                        ( 1.000000, -1.000000, 1.000000),
                        ( 1.000000, -1.000000, -1.000000),
                        ( 1.000000, 1.000000, -1.000000),

                        # Back Face
                        (-1.000000,  1.000000, -1.000000),
                        (-1.000000, -1.000000, -1.000000),
                        ( 1.000000, -1.000000, -1.000000),
                        ( 1.000000,  1.000000, -1.000000),

                        # Top Face
                        (-1.000000, 1.000000, -1.000000),
                        (-1.000000, 1.000000, 1.000000),
                        ( 1.000000, 1.000000, 1.000000),
                        ( 1.000000, 1.000000, -1.000000),

                        # Bottom Face
                        (-1.000000, -1.000000, -1.000000),
                        (-1.000000, -1.000000, 1.000000),
                        ( 1.000000, -1.000000, 1.000000),
                        ( 1.000000, -1.000000, -1.000000)
                      )

        tex_coords = (
                      # Front Face
                      (0.333333, 0.500000),
                      (0.333333, 0.000000),
                      (0.000000, 0.000000),
                      (0.000000, 0.500000),
                      # Left Face
                      (0.000000, 1.000000),
                      (0.000000, 0.500000),
                      (0.333333, 0.500000),
                      (0.333333, 1.000000),
                      # Right Face
                      (1.000000, 1.000000),
                      (1.000000, 0.500000),
                      (0.666666, 0.500000),
                      (0.666666, 1.000000),
                      # Back Face
                      (0.333333, 1.000000),
                      (0.333333, 0.500000),
                      (0.666666, 0.500000),
                      (0.666666, 1.000000),
                      # Top Face
                      (0.340000, 0.500000),
                      (0.666666, 0.500000),
                      (0.666666, 0.000000),
                      (0.340000, 0.000000),
                      # Bottom Face
                      (0.666666, 0.500000),
                      (0.666666, 0.000000),
                      (1.000000, 0.000000),
                      (1.000000, 0.500000),
                    )

        index = (2, 1, 0, 2, 0, 3, 4, 5, 6, 7, 4, 6, 10, 9, 8, 10, 8, 11, 12,
                 13, 14, 15, 12, 14, 18, 17, 16, 18, 16, 19, 23, 20, 22, 20,
                 21, 22)

        scaled = 5 * np.array(base_coords, np.float32)
        # indices = np.array((0, 1, 3, 3, 1, 2))
        # # , 3, 2, 4, 3, 4, 5, 0, 3, 7, 3, 5,
        # #                     7, 2, 6, 4, 2, 1, 6, 0, 7, 1, 7, 6, 1, 1, 6, 2, 2,
        # #                     6, 4, 6, 5, 4, 6, 7, 5), np.uint32)
        # # tex_coord = ((.6666, .5), (.666, 0), (0, 1), (1, .5))
        # # , 5, 4, 6, 7, 5,
        # #                     6, 7, 5, 4, 0, 3, 7) , np.uint32)

        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=tex_coords), index=index)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)

# -------------- main program and scene setup --------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file = tex_file

        base_coords = ((-1.0, -1.0, 0), (1.0, -1.0, 0), (-1.0, 1.0, 0), (1.0, 1.0, 0))

        scaled = 1 * np.array(base_coords, np.float32)
        indices = np.array((0, 3, 1, 0, 2, 3), np.uint32)

        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=((0,1), (1, 1), (0, 0), (1, 0))), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture = Texture(tex_file, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture)


def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    # default color shader
    skybox = Node()
    shader = Shader("trunk_texture.vert", "trunk_texture.frag")
    front = Node(children=(TexturedPlane(shader, "skybox/front.jpg"),), transform=translate(z=-1) @ rotate((0, 1, 0), 180))
    viewer.add(front)
    back = Node(children=(TexturedPlane(shader, "skybox/back.jpg"),), transform=translate(z=1))
    viewer.add(back)
    left = Node(children=(TexturedPlane(shader, "skybox/left.jpg"),), transform=rotate((0, 1, 0), 90) @ translate(z=1))
    viewer.add(left)
    right = Node(children=(TexturedPlane(shader, "skybox/right.jpg"),), transform=rotate((0, 1, 0), -90) @ translate(z=1))
    viewer.add(right)
    top = Node(children=(TexturedPlane(shader, "skybox/top.jpg"),), transform=rotate((0, 1, 0), 180) @ rotate((1, 0, 0), -90) @ translate(z=1))
    viewer.add(top)
    bottom = Node(children=(TexturedPlane(shader, "skybox/bottom.jpg"),), transform=rotate((0, 1, 0), 180) @ rotate((1, 0, 0), 90) @ translate(z=1) )
    viewer.add(bottom)
    # back = Node(children=(TexturedPlane(shader, "skybox/front.jpg"),), transform=rotatetranslate(z=-1))
    viewer.add(Axis(shader))
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
