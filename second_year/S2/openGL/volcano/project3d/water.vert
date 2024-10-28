#version 400 core

in vec3 position;

out vec4 clipSpace;
out vec3 toCameraVector;
out vec2 textureCoords;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;
uniform vec3 w_camera_position;

const float tiling=1.0;

void main(void) {
	vec4 worldPosition = model * vec4(position.x, position.y, 0, 1.0);
	clipSpace= projection * view * worldPosition;
	gl_Position = clipSpace;
	textureCoords = vec2(position.x/2 + 0.5, position.y/2 + 0.5)*tiling;
	toCameraVector = w_camera_position - worldPosition.xyz;
}