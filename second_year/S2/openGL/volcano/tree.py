#!/usr/bin/env python3

import OpenGL.GL as GL              # standard Python OpenGL wrapper
import numpy as np                  # all matrix manipulations & OpenGL args
import glfw                         # lean window system wrapper for OpenGL
import math
from random import random, randint
from texture import Texture, Textured

from core import Shader, Mesh, Node, load
from transform import translate, identity, rotate, scale, vec

class Sphere(Mesh):
    def __init__(self, shader):
        radius, slices, stacks = 1, 10, 10
        vertex_array = []
        normal_array = []
        texcoord_array = []
        for j in range(stacks):
            theta1 = j * np.pi / stacks
            theta2 = (j + 1) * np.pi / stacks
            for i in range(slices):
                phi1 = i * 2 * np.pi / slices
                phi2 = (i + 1) * 2 * np.pi / slices
                vertex_array.extend(
                    [
                        (radius * np.sin(theta1) * np.cos(phi1),
                        radius * np.cos(theta1),
                        radius * np.sin(theta1) * np.sin(phi1)),

                        (radius * np.sin(theta2) * np.cos(phi1),
                        radius * np.cos(theta2),
                        radius * np.sin(theta2) * np.sin(phi1)),

                        (radius * np.sin(theta2) * np.cos(phi2),
                        radius * np.cos(theta2),
                        radius * np.sin(theta2) * np.sin(phi2)),

                        (radius * np.sin(theta1) * np.cos(phi2),
                        radius * np.cos(theta1),
                        radius * np.sin(theta1) * np.sin(phi2))
                    ]
                )
                normal_array.extend(
                    [
                        np.sin(theta1) * np.cos(phi1),
                        np.cos(theta1),
                        np.sin(theta1) * np.sin(phi1),
                        np.sin(theta2) * np.cos(phi1),
                        np.cos(theta2),
                        np.sin(theta2) * np.sin(phi1),
                        np.sin(theta2) * np.cos(phi2),
                        np.cos(theta2),
                        np.sin(theta2) * np.sin(phi2),
                        np.sin(theta1) * np.cos(phi2),
                        np.cos(theta1),
                        np.sin(theta1) * np.sin(phi2),
                    ]
                )
                texcoord_array.extend(
                    [
                        i / slices,
                        j / stacks,
                        i / slices,
                        (j + 1) / stacks,
                        (i + 1) / slices,
                        (j + 1) / stacks,
                        (i + 1) / slices,
                        j / stacks,
                    ]
                )
        super().__init__(
            shader, dict(position=vertex_array)
        )  # , normal_array, texcoord_array

class CylinderMesh(Mesh):
    def __init__(self, shader, model):
        self.step = 120 # degrees step
        self.tex_coord = [(0,0)] # ((0, 0), (0, 1), (1, 0), (1, 1))
        position, index = self.circle(model=identity(), offset=0) # base circle
        base_length = len(position)
        upper_positions, upper_indexes = self.circle(model=model, offset=len(position))
        position.extend(upper_positions)
        index.extend(upper_indexes)
        # create the sides of the cylinder
        for i in range(1, base_length-1):
            j = i + base_length
            index.append((i, j, j+1))
            index.append((i, j+1, i+1))
        self.shader = shader

        index = np.array(index, np.uint32)
        self.tex_coords()
        super().__init__(shader=shader, attributes=dict(position=position, tex_coord=self.tex_coord), index=index)
        # mesh = Mesh(shader=shader, attributes=dict(position=position, tex_coord=self.tex_coord), index=index)
        # super().__init__(mesh, diffuse_map=CylinderMesh.texture)
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
    def tex_coords(self):
        for i, theta in enumerate(range(0, 361, self.step)):
            theta = math.radians(theta)
            self.tex_coord.append((theta, 0))
        self.tex_coord.append((0, 0))
        for i, theta in enumerate(range(0, 361, self.step)):
            theta = math.radians(theta)
            self.tex_coord.append((theta, 1))
    texture = None;
    @staticmethod
    def init_texture():
        CylinderMesh.texture = Texture("tree2.jpeg")
        # texture = Texture("tree2.jpeg")
        # super().__init__(mesh, diffuse_map=texture)
    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, **uniforms) #**uniforms)

class EnhancedTree(Node):
    """Hierarchical randomised l system modeling of a tree using cylinders"""
    def gen_l_system(self, nb_iterations, axiom, rules):
        prev_string = list(axiom)
        for _ in range(nb_iterations):
            curr_string = []
            for c in prev_string:
                res = rules.get(c)
                if res is not None:
                    curr_string.append(res)
            prev_string = "".join(curr_string)
        return prev_string

    def next_gen_l_system(self, curr_gen, rules):
        next_gen= []
        for c in curr_gen:
            res = rules.get(c)
            if res is not None:
                # if random() > .3:
                next_gen.append(res)
                # else:
                    # next_gen.append(c)

            else:
                next_gen.append(c)
        return "".join(next_gen)

    def __init__(self, shader, children=(), transform=identity()):
        super().__init__(children=children, transform=transform)
        self.shader = shader
        # self.cylinder = CylinderMesh(shader)
        # trunk_shape = Node(transform=scale(.5, 8, .5))
        # trunk_shape.add(Cylinder(shader))
        # self.base_model=scale(.5, 8, .5);
        # self.add(trunk_shape)
        # self.first = True
        # self.add(Node(children=(self.make_branch(5),), transform=translate(y=8)))
            # transform = Node(transform=)
            # X→
        self.plant1 = {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"} # axiom x
        self.plant2 = {"F": "FF+[+F-F-F]-[-F+F+F]"} # axiom F
        self.plant3 = {"X": "F[+X][-X]FX", "F": "FF"} # axiom x
        self.plant4 = {"X": "+F[+X]F[-X]+X", "F": "FF"}#axiom x
        # x = self.gen_l_system(*self.plant2)
        ng = "X"
        length = 1
        for _ in range(2):
            ng = self.next_gen_l_system(ng, self.plant1)
            # length *= 0.8
        self.add(self.display_l_system(ng, length))
        # self.add(self.cylinder)
    def make_branch(self, depth):
        if depth <= 0:
            return
        nb_branches = randint(1, 5)
        # height = .5
        # maxh = .95 * height
        # minh = .50 * height
        # nh = random() * (maxh-minh) + minh
        curr = Node()
        model_matrixes = []
        for _ in range(nb_branches):
            r = randint(-60, 60) #22.5 # random()*90-45
            r2 = randint(-60, 60) #22.5 # random()*90-45
            model = rotate((1, 0, 0), r) @ rotate((0, 0, 1), r2) @ translate(y=randint(2, 5)) @ scale(0.6, 1, 0.6)
            model_matrixes.append(model)
        if self.first:
            curr.add(Branch(self.shader, model_matrixes, self.base_model))
            self.first = False
        else:
            curr.add(Branch(self.shader, model_matrixes))
        for model in model_matrixes:
            transform = Node(transform=model)
            sub_branches = self.make_branch(depth-1) #, nh)
            if sub_branches:
                transform.add(sub_branches);
                curr.add(transform)
        return curr

    def _count_succ_forward(self, i, l_system):
        c = 0
        while i < len(l_system) and l_system[i] == "F":
            c += 1
            i += 1
        return c

    def _is_leaf(self, i, l_system):
        i += 1
        flag = True
        stack = 0
        while i < len(l_system) and flag:
            match l_system[i]:
                case "F":
                    flag = False
                case "]":
                    if stack == 0:
                        break;
                    stack -= 1
                case "[":
                    stack += 1
            i += 1
        return flag
    def odisplay_l_system(self, l_system, length):
        reduction_factor = .98
        s = scale(reduction_factor, 1, reduction_factor)
        node_stack = []
        root_node = current_node = Node()
        shader = Shader("color.vert", "color.frag")
        self.sphere = Sphere(shader)
        # shader = Shader("trunk_texture.vert", "trunk_texture.frag")
        t = translate(y=length)
        cylinder = Node(children=(CylinderMesh(shader, t),))
        i = 0
        while i < len(l_system):
            match l_system[i]:
                case "F":
                    count = self._count_succ_forward(i, l_system)
                    s1 = scale(reduction_factor, count*1, reduction_factor)
                    t1 = translate(y=count) # (reduction_factor, count*1, reduction_factor)
                    current_node.add()
                    new_node = Node(transform=t1)
                    shape = Node(children=(cylinder,), transform=s1)
                    current_node.add(shape)
                    current_node.add(new_node)
                    current_node = new_node
                    i += count - 1
                case "[":
                    node_stack.append(current_node)
                    r = randint(-360, 360)
                    trans = rotate((0, 1, 0), r)
                    new_node = Node(transform=trans)
                    current_node.add(new_node)
                    current_node = new_node
                case "]":
                    current_node = node_stack.pop()
                case "-":
                    trans = rotate((0, 0, 1), -35)
                    new_node = Node(transform=trans)
                    current_node.add(new_node)
                    current_node = new_node
                case "+":
                    trans = rotate((0, 0, 1), +35)
                    new_node = Node(transform=trans)
                    current_node.add(new_node)
                    current_node = new_node
            if l_system[i] == "F" and self._is_leaf(i, l_system):
                r = randint(-360, 360)
                current_node.add(Node(children=(self.sphere,), transform=rotate((1, 1, 1), r) @ scale(2, 2, 2) ))
            i += 1
        return root_node
    def display_l_system(self, l_system, length):
        reduction_factor = .98
        s = scale(reduction_factor, 0.8, reduction_factor)
        node_stack = []
        root_node = current_node = Node()
        i = 0

        shader = Shader("color.vert", "color.frag")
        self.sphere = Sphere(shader)
        # shader = Shader("texture.vert", "texture.frag")
        prev = identity()
        pending_r = False
        r = identity()
        t = translate(y=length)
        rotate_minus = rotate((0, 0, 1), -35)
        rotate_plus = rotate((0, 0, 1), +35)
        while i < len(l_system):
            match l_system[i]:
                case "F":
                    count = 1
                    if pending_r:
                        r, prev, pending_r = prev, identity(), False
                    count = self._count_succ_forward(i, l_system)
                    if count != 1:
                        t = translate(y=count*length)
                        s = scale(reduction_factor**count, 1, reduction_factor**count)
                    new_node = Node(transform= r @ t @ s)
                    current_node.add(CylinderMesh(shader, r @ t @ s))
                    current_node.add(new_node)
                    current_node = new_node
                    i += count-1

                case "[":
                    node_stack.append(current_node)

                    r = randint(-360, 360)
                    # prev = rotate((1, 1, 0), r) @ prev
                    trans = rotate((0, 1, 0), r) # @ scale(reduction_factor, 1, reduction_factor)
                    new_node = Node(transform=trans)
                    current_node.add(new_node)
                    current_node = new_node
                case "]":
                    current_node = node_stack.pop()
                case "-":
                    new_node = Node()
                    current_node.add(new_node)
                    current_node = new_node
                    prev = rotate_minus @ prev
                    pending_r = True
                case "+":
                    new_node = Node()
                    current_node.add(new_node)
                    current_node = new_node
                    prev = rotate_plus @ prev
                    pending_r = True
            if l_system[i] == "F" and self._is_leaf(i, l_system):
                r = randint(-360, 360)
                current_node.add(Node(children=(self.sphere,), transform=rotate((1, 1, 1), r) @ scale(2, 2, 2) ))
            i += 1
        return root_node


class Line(Mesh):
    def __init__(self, shader):
        super().__init__(shader=shader, attributes=dict(position=[(0, 0, 0), (0, 1, 0), (0, 1, 0), (1, 1, 1)], index=(0, 1, 1, 2)))
    def draw(self, primitives=GL.GL_LINES, attributes=None, **uniforms):
        super().draw(primitives=GL.GL_LINES, attributes=None, **uniforms)


class LineTree(Mesh):
    """Hierarchical randomised l system modeling of a tree using cylinders"""
    def __init__(self, shader, children=(), transform=identity()):
        self.shader = shader
        # l_system = (35, {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"}, "X") # axiom x
        # l_system = (25, {"X": "F[+X][-X]FX", "F": "FF"}, "X")
        l_system = (22.5, {"F": "F[+F]F[-F][F]"}, "F")
        self.angle, rules, axiom = l_system
        # self.angle = 35
        positions = self.display_l_system(self.gen_l_system(4, axiom, rules), 2)
        super().__init__(shader=shader, attributes=dict(position=positions))

    def gen_l_system(self, nb_iterations, axiom, rules):
        prev_string = list(axiom)
        for _ in range(nb_iterations):
            curr_string = []
            for c in prev_string:
                res = rules.get(c)
                if res is not None:
                    curr_string.append(res)
                else:
                    curr_string.append(c)
            prev_string = "".join(curr_string)
        return prev_string

    def draw(self, primitives=GL.GL_LINES, attributes=None, **uniforms):
        super().draw(primitives=GL.GL_LINES, attributes=None, **uniforms)

    def display_l_system(self, l_system, length):
        points =[(0, 0, 0, 1)]
        curr_point = vec(0, 0, 0, 1)
        points.append(curr_point)
        stack = []
        transform_stack = []
        curr_model = identity()
        i = 0
        unary_vec = vec(0, 1, 0, 1)
        while i < len(l_system):
            match l_system[i]:
                case "F":
                    points.append(curr_point)
                    # curr_model = translate(y=1) @ curr_model
                    p = unary_vec @ curr_model
                    curr_point = (translate(*(curr_point[:-1])) @  p)
                    points.append(curr_point)
                case "[":
                    stack.append(curr_point)
                    transform_stack.append(curr_model)
                    r = randint(-360, 360)
                    r = rotate((0, 1, 0), r)
                    curr_model = r @ curr_model
                case "]":
                    curr_point = stack.pop()
                    curr_model = transform_stack.pop()
                case "-":
                    # curr_model = curr_model @ rotate((0, 0, 1), +35)
                    curr_model =  rotate((0, 0, 1), -self.angle) @ curr_model
                    reset_r = True
                case "+":
                    curr_model =  rotate((0, 0, 1), +self.angle) @ curr_model
                    # curr_model = curr_model @ rotate((0, 0, 1), -35)
            # if l_system[i] == "F" and self._is_leaf(i, l_system):
            #     r = randint(-360, 360)
            #     current_node.add(Node(children=(self.sphere,), transform=rotate((1, 1, 1), r) @ scale(2, 2, 2) ))
            i += 1
        return points
