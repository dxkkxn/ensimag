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
from tree import Tree, CylinderMesh

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer()

    CylinderMesh.init_texture()
    viewer.add(Node(children=(Tree(complexity=5),), transform=translate(y=-3)))
    # default color shader
    viewer.run()


if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
