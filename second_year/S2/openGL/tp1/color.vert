#version 330 core

// input attribute variable, given per vertex
in vec3 position;
uniform float timer;

out vec3 color;

mat2 rot_ma(float a) {
    float ca = cos(a);
    float sa = sin(a);
    return mat2(vec2(ca, sa), vec2(-sa, ca));
}

void main() {
    vec3 p = position;
    color = vec3((p.xy+1.)*0.5, 0.);
    p.xy = rot_ma(timer) * p.xy;
    //p.x = 0.5*sin(timer) + p.x;
    gl_Position = vec4(p, 1);
}
