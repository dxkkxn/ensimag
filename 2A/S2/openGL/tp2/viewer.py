#!/usr/bin/env python3
"""
Python OpenGL practical application.
"""

import OpenGL.GL as GL             # standard Python OpenGL wrapper
import glfw                        # lean window system wrapper for OpenGL
import numpy as np                 # all matrix manipulations & OpenGL args
import math
from transform import Trackball, identity
from core import Shader, Mesh
import assimpcy                     # 3D resource loader


# ------------  Exercise 2: Scene object classes ------------------------
class Pyramid(Mesh):
    """ Class for drawing a pyramid object """
    def __init__(self, shader):
        self.shader = shader

        # TODO: this is still a triangle, new values needed for Pyramid
        position = np.array(((-.5, 0, -.5), (-.5, 0, .5), (.5, 0, .5), (.5, 0, -.5),
                             (0, 1, 0)), np.float32)
        self.index = np.array((4, 2, 3, 4, 1, 2, 4, 0, 1, 4, 3, 0,
                               2, 0, 3, 1, 0, 2), np.uint32)

        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1)), 'f')
        attrs = dict(position=position, color=color)
        super().__init__(shader=shader, attributes=attrs, index=self.index)



# -------------- 3D resource loader -----------------------------------------
def load(file, shader):
    """ load resources from file using assimp, return list of Mesh """
    try:
        pp = assimpcy.aiPostProcessSteps
        flags = pp.aiProcess_Triangulate | pp.aiProcess_GenSmoothNormals
        scene = assimpcy.aiImportFile(file, flags)
    except assimpcy.all.AssimpError as exception:
        print('ERROR loading', file + ': ', exception.args[0].decode())
        return []

    meshes = [Mesh(shader, attributes=dict(position=m.mVertices, color=m.mNormals),
                   index=m.mFaces)
              for m in scene.mMeshes]
    size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
    print('Loaded %s\t(%d meshes, %d faces)' % (file, len(meshes), size))
    return meshes

# ------------  Exercise 4  ------------------------
class Cylinder(Mesh):

    def circum_eq():
        """draw of circumference using circle eq """
        position = []
        position2 = []
        for x in range(-10, 11, 2):
            i = int((x+10)/2) # get current iteration
            x = x/10          # x position
            y = math.sqrt(1-x**2)
            position.append((x, y, 0))
            position2.append((x, -y, 0))
        position2.reverse();
        position.extend(position2)
        position = np.array(position, np.float32)
        index = []
        print(len(position))
        for i in range(1, 23):
            index.extend((10, i-1, i))
        #index.extend((10, i-1, i))
        index = np.array(index)
        print(index)
        print(position)
        #print(len(position))


    def __init__(self, shader):
        self.shader = shader
        position = []
        position.append((0, 0, 0))
        position.append((0, 0, 1))
        index = []
        for theta in range(0, 361, 4):
            theta = math.radians(theta)
            position.append((math.cos(theta), math.sin(theta), 0))
            position.append((math.cos(theta), math.sin(theta), 1))
            if theta != 0:
                i = len(position)-2
                index.extend((0, i, i-2))  # 0 center lower circle
                index.extend((1, i-1, i+1))  # 1 center upper circle

                index.extend((i-1, i, i+1))  # 1 center upper circle
                index.extend((i-1, i-2, i))  # 1 center upper circle
                # index.extend((i-2, i+2, i-1))  # 1 center upper circle

        index = np.array(index, np.uint32)

        super().__init__(shader=shader, attributes=dict(position=position), index=index)

    def draw(self, primitives=GL.GL_TRIANGLES, **uniforms):
        super().draw(primitives=primitives, **uniforms)

# ------------  Exercise 1  ------------------------
#class Pyramid:
#    """ Class for drawing a pyramid object """
#
#    def __init__(self, shader):
#        self.shader = shader
#
#        # TODO: this is still a triangle, new values needed for Pyramid
#        position = np.array(((-.5, 0, -.5), (-.5, 0, .5), (.5, 0, .5), (.5, 0, -.5),
#                             (0, 1, 0)) , np.float32)
#        self.index = np.array((4, 2, 3, 4, 1, 2, 4, 0, 1, 4, 3, 0,
#                               2, 0, 3, 1, 0, 2), np.uint32)
#
#        color = np.array(((1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1)), 'f')
#
#        self.glid = GL.glGenVertexArrays(1)  # create OpenGL vertex array id
#        GL.glBindVertexArray(self.glid)      # activate to receive state below
#        self.buffers = GL.glGenBuffers(3)    # create buffer for position attrib
#
#        # create position attribute, send to GPU, declare type & per-vertex size
#        loc = GL.glGetAttribLocation(shader.glid, 'position')
#        GL.glEnableVertexAttribArray(loc)    # assign to position attribute
#        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[0])
#        GL.glBufferData(GL.GL_ARRAY_BUFFER, position, GL.GL_STATIC_DRAW)
#        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)
#
#        # create color attribute, send to GPU, declare type & per-vertex size
#        loc = GL.glGetAttribLocation(shader.glid, 'color')
#        GL.glEnableVertexAttribArray(loc)    # assign to color
#        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[1])
#        GL.glBufferData(GL.GL_ARRAY_BUFFER, color, GL.GL_STATIC_DRAW)
#        GL.glVertexAttribPointer(loc, 3, GL.GL_FLOAT, False, 0, None)
#
#        # create a dedicated index buffer, copy python array to GPU
#        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[2])
#        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self.index,
#                        GL.GL_STATIC_DRAW)
#
#    def draw(self, projection, view, **_args):
#        GL.glUseProgram(self.shader.glid)
#
#        loc = GL.glGetUniformLocation(self.shader.glid, 'view')
#        GL.glUniformMatrix4fv(loc, 1, True, view)
#        loc = GL.glGetUniformLocation(self.shader.glid, 'projection')
#        GL.glUniformMatrix4fv(loc, 1, True, projection)
#
#        # draw triangle as GL_TRIANGLE indexed mode array, pass array size
#        GL.glBindVertexArray(self.glid)
#        GL.glDrawElements(GL.GL_TRIANGLES, self.index.size,
#                          GL.GL_UNSIGNED_INT, None)
#
#    def __del__(self):
#        GL.glDeleteVertexArrays(1, [self.glid])
#        GL.glDeleteBuffers(3, self.buffers)
#

# ------------  Viewer class & window management ------------------------------
class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """
    def __init__(self, width=2*640, height=2*480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, False)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # initialize trackball
        self.trackball = Trackball()
        self.mouse = (0, 0)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_cursor_pos_callback(self.win, self.on_mouse_move)
        glfw.set_scroll_callback(self.win, self.on_scroll)

        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_CULL_FACE)   # enable backface culling (Exercise 1)
        GL.glEnable(GL.GL_DEPTH_TEST)  # enable depth test (Exercise 1)

        # initially empty list of object to draw
        self.drawables = []

    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer, but also need to clear Z-buffer! (Exercise 1)
            #GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # comment this, uncomment next
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            win_size = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            projection = self.trackball.projection_matrix(win_size)

            # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(view=view, projection=projection,
                              model=identity())

            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)

            for drawable in self.drawables:
                if hasattr(drawable, 'key_handler'):
                    drawable.key_handler(key)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.trackball.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.trackball.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.trackball.zoom(deltay, glfw.get_window_size(win)[1])


# -------------- main program and scene setup --------------------------------
def main():
    """ create window, add shaders & scene objects, then run rendering loop """
    viewer = Viewer()
    color_shader = Shader("color.vert", "color.frag")
    #viewer.add(*load('suzanne.obj', color_shader))
    viewer.add(Cylinder(color_shader));
    # place instances of our basic objects
    #viewer.add(Pyramid(color_shader))

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    main()                  # main function keeps variables locally scoped
