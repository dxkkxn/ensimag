#!/usr/bin/env python3

# import PyOpenGL library
from OpenGL.GL import *
from OpenGL.GLUT import *

# vertex shader source code
vertex_shader_source = """
    #version 330

    layout(location = 0) in vec3 position;

    void main() {
        gl_Position = vec4(position, 1.0);
    }
"""

# geometry shader source code
geometry_shader_source = """
    #version 330

    layout (triangles) in;
    layout (triangle_strip, max_vertices=3) out;

    void main() {
        for (int i = 0; i < 3; i++) {
            gl_Position = gl_in[i].gl_Position;
            EmitVertex();
        }
        EndPrimitive();
    }
"""

# fragment shader source code
fragment_shader_source = """
    #version 330

    out vec4 out_color;

    void main() {
        out_color = vec4(1.0, 1.0, 1.0, 1.0);
    }
"""

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # use the shader program
    glUseProgram(shader_program)

    # draw a triangle
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glVertex3f( 0.0,  0.5, 0.0)
    glEnd()

    # swap the buffers
    glutSwapBuffers()

# initialize OpenGL
glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)
glutCreateWindow("Geometry Shader Example")

# create and compile the vertex shader
vertex_shader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertex_shader, vertex_shader_source)
glCompileShader(vertex_shader)

# create and compile the geometry shader
geometry_shader = glCreateShader(GL_GEOMETRY_SHADER)
glShaderSource(geometry_shader, geometry_shader_source)
glCompileShader(geometry_shader)

# create and compile the fragment shader
fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragment_shader, fragment_shader_source)
glCompileShader(fragment_shader)

# create a shader program and attach the shaders
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, geometry_shader)
glAttachShader(shader_program, fragment_shader)

# link the program
glLinkProgram(shader_program)

# set up the OpenGL state
glClearColor(0.0, 0.0, 0.0, 1.0)
glEnable(GL_DEPTH_TEST)

# set the display function
glutDisplayFunc(display)

# start the main loop
glutMainLoop()
