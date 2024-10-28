#version 330 core

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 plane;
uniform vec3 w_camera_position;
in vec3 position;
in vec3 normal;
in vec3 tangent;

out vec3 normal_position;
out vec3 tangent_position;
out vec2 frag_tex_coords;
out float distance_gradiant;
out vec3 camera_direction;
out mat4 model_matrix;

void main() {
    vec4 worldPosition = model * vec4(position, 1);
    gl_ClipDistance[0] = dot(worldPosition, plane);

    camera_direction = normalize(w_camera_position - worldPosition.xyz);

    distance_gradiant = length(position.xy - (0,0));
    //normal_position =  normalize(normal);//model * vec4(position, 1)).xyz;
    gl_Position = projection * view * model * vec4(position, 1);
    frag_tex_coords = position.xy;
    model_matrix = model;
    normal_position = normalize((model * vec4(normal, 0)).xyz);
    tangent_position = normalize((model * vec4(tangent, 0)).xyz);
}
