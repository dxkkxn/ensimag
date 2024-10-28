#version 330 core

// output fragment color for OpenGL
out vec4 out_color;
in vec3 color;

void main() {
    out_color = vec4(color, 0.);
}
