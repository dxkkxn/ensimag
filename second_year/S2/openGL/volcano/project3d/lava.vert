#version 400 core

in vec3 position;

out vec2 frag_tex_coords;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;


void main(void) {

	gl_Position = projection * view * model * vec4(position, 1.0);
	frag_tex_coords = position.xy;
 
}