#version 330 core

in vec3 fragment_color;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    out_color = vec4(fragment_color, 1);
    // out_color = texture(diffuse_map, frag_tex_coords);
}
