#!/usr/bin/env python3
import sys
from itertools import cycle
import OpenGL.GL as GL              # standard Python OpenGL wrapper
import glfw                         # lean window system wrapper for OpenGL
import numpy as np                  # all matrix manipulations & OpenGL args
from core import Shader, Viewer, Mesh, load
from texture import Texture, Textured
from animation import KeyFrames, KeyFrameControlNode
from transform import vec, quaternion, quaternion_from_euler



# -------------- Example textured plane class ---------------------------------
class TexturedPlane(Textured):
    """ Simple first textured object """
    def __init__(self, shader, tex_file1, tex_file2):
        # prepare texture modes cycling variables for interactive toggling
        self.wraps = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                            GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filters = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                              (GL.GL_LINEAR, GL.GL_LINEAR),
                              (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap, self.filter = next(self.wraps), next(self.filters)
        self.file1 = tex_file1
        self.file2 = tex_file2

        # setup plane mesh to be textured
        base_coords = ((-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0))
        tex_coord = ((0, 0), (0, 1), (1, 0), (1, 1))
        scaled = 100 * np.array(base_coords, np.float32)
        indices = np.array((0, 1, 2, 0, 2, 3), np.uint32)
        mesh = Mesh(shader, attributes=dict(position=scaled, tex_coord=tex_coord), index=indices)

        # setup & upload texture to GPU, bind it to shader name 'diffuse_map'
        texture1 = Texture(tex_file1, self.wrap, *self.filter)
        texture2 = Texture(tex_file2, self.wrap, *self.filter)
        super().__init__(mesh, diffuse_map=texture1, second_texture=texture2)

    def key_handler(self, key):
        # cycle through texture modes on keypress of F6 (wrap) or F7 (filtering)
        self.wrap = next(self.wraps) if key == glfw.KEY_F6 else self.wrap
        self.filter = next(self.filters) if key == glfw.KEY_F7 else self.filter
        if key in (glfw.KEY_F6, glfw.KEY_F7):
            texture = Texture(self.file, self.wrap, *self.filter)
            self.textures.update(diffuse_map=texture)



# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    my_keyframes = KeyFrames({0: 1, 3: 7, 6: 20})
    print(my_keyframes.value(1.5))
    vector_keyframes = KeyFrames({0: vec(1, 0, 0), 3: vec(0, 1, 0), 6: vec(0, 0, 1)})
    print(vector_keyframes.value(1.5))   # should display numpy vector (0.5, 0.5, 0)
    viewer = Viewer()
    shader = Shader("color.vert", "color.frag")

    translate_keys = {0: vec(0, 0, 0), 2: vec(1, 1, 0), 4: vec(0, 0, 0)}
    rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
                   3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    scale_keys = {0: 1, 2: 0.5, 4: 1}
    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(Cylinder(shader))
    viewer.add(keynode)

    # start rendering loop
    viewer.run()

#    viewer = Viewer()
#    shader = Shader("texture.vert", "texture.frag")
#    #light_dir = (-1, -1, -1)
#    #viewer.add(*load("cube/cube.obj", shader, "cube/cube.png", light_dir=light_dir))
#
#    viewer.add(*[mesh for file in sys.argv[1:] for mesh in load(file, shader)])
#
#    if len(sys.argv) != 2:
#        print('Usage:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
#              ' format supported by assimp.' % (sys.argv[0],))
#        viewer.add(TexturedPlane(shader, "grass.png", "flowers.png"))
#
#    # start rendering loop
#    viewer.run()
#

if __name__ == '__main__':
    main()                     # main function keeps variables locally scoped
