#version 330 core

in vec3 w_position, w_normal;   // in world coordinates
uniform vec3 w_camera_position;

// output fragment color for OpenGL
out vec4 out_color;
uniform vec3 light_dir;

void main() {
    vec3 k_d = vec3(1, 1, 1);
    vec3 k_a = vec3(.3, .3, .3);
    vec3 k_s = vec3(.1, .1, .1);
    vec3 color = vec3(105./256, 255./256, 18./256);
    vec3 n = normalize(w_normal);
    vec3 l = normalize(light_dir);
    vec3 r = reflect(l, n);
    vec3 v = normalize(w_position - w_camera_position); // - w_position);
    float s = 3;
    out_color = vec4(k_a * color + k_d * max(dot(n, l), 0)+ k_s * pow(max(dot(r, v), 0), s), 1);
    // out_color = texture(diffuse_map, frag_tex_coords);
}
