#version 330 core

layout (triangles) in;
layout (triangle_strip, max_vertices=3) out;

uniform mat4 model;

in vec3 normal_position[];
in vec2 frag_tex_coords[];
in float zfactor[];

out vec2 gfrag_tex_coords;
out vec3 normal;

void main() {
    vec3 edge1 = normal_position[1] - normal_position[0];
    vec3 edge2 = normal_position[2] - normal_position[0];
    normal = normalize(cross(edge1, edge2));
    for(int i=0; i<3; i++) {
        
        gl_Position = gl_in[i].gl_Position;
        gfrag_tex_coords = frag_tex_coords[i];
        EmitVertex();
    }
    EndPrimitive();
}