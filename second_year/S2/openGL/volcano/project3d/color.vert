#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
in vec3 position;
// in vec3 normal;

out vec3 w_position, w_normal;   // in world coordinates

void main() {
    vec3 normal = vec3(0, 1, 0);
    w_normal = (model * vec4(normal, 0)).xyz;
    w_position = (model * vec4(position, 0)).xyz;
    gl_Position = projection * view * model * vec4(position, 1);
}

