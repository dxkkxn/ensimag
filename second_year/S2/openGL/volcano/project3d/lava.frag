#version 400 core

uniform sampler2D diffuse_map;
in vec2 frag_tex_coords;

out vec4 out_color;


void main(void) {

	out_color = texture(diffuse_map, frag_tex_coords);

}