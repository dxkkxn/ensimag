#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D second_texture;

in vec3 normal_position;
in vec2 frag_tex_coords;
in vec3 w_position, w_normal;   // in world coordinates

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

void main() {

    // vec3 n = normalize(w_normal);
    // vec3 l = normalize(light_dir);
    // vec3 r = reflect(l, n);
    // vec3 v = normalize(w_camera_position- w_position);
    // out_color = vec4(k_a + texture(diffuse_map, frag_tex_coords).xyz * max(dot(n, l), 0) +
    //             k_s * pow(max(dot(r, v), 0), s), 1);
    out_color = texture(diffuse_map, frag_tex_coords);
    // out_color = vec4(1, 0, 0, 1);
}
