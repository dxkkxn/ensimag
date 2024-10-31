#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_d;
uniform vec3 k_a;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

// output fragment color for OpenGL
out vec4 out_color;

void main() {
    // TODO: compute Lambert illumination
    // out_color = vec4(w_normal, 1);
    // float = clamp(float x,float minV,float maxV); // return min(max(x,minV),maxV)
    // out_color = vec4(k_d * max(dot(normal_tmp, light_dir), 0), 1); // lambert ilumination

    vec3 n = normalize(w_normal);
    vec3 l = normalize(light_dir);
    vec3 r = reflect(l, n);
    vec3 v = normalize(w_position - w_camera_position); // - w_position);
    out_color = vec4(k_a + k_d * max(dot(n, l), 0) + k_s * pow(max(dot(r, v), 0), s), 1);
}
