#version 330 core

uniform sampler2D diffuse_map;
uniform sampler2D second_texture;
in vec2 frag_tex_coords;

in vec3 w_position, w_normal;   // in world coordinates
uniform vec3 w_camera_position;

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties

// world camera position

out vec4 out_color;

void main() {
    vec3 k_d = vec3(1, 1, 1);
    vec3 k_a = vec3(1, 1, 1);
    vec3 k_s = vec3(1, 1, 1);
    float s = 3;
    vec3 n = normalize(w_normal);
    vec3 l = normalize(light_dir);
    vec3 r = reflect(l, n);
    vec3 v = normalize(w_camera_position- w_position);
    out_color = vec4(k_a + texture(diffuse_map, frag_tex_coords).xyz * max(dot(n, l), 0) +
                k_s * pow(max(dot(r, v), 0), s), 1);
    out_color = (texture(second_texture, frag_tex_coords) + texture(diffuse_map, frag_tex_coords))/2;
}
