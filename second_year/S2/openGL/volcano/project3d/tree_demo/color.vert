#version 330 core

// global color
uniform vec3 global_color;

// input attribute variable, given per vertex
in vec3 position;
in vec3 color;
in vec3 normal;


// global matrix variables
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// uniform int is_leaf;

// // interpolated color for fragment shader, intialized at vertices
out vec3 fragment_color;

void main() {
    // initialize interpolated colors at vertices
    // fragment_color = color + normal + global_color;
    // fragment_color = (position.xyz+1)*.5;

    // fragment_color.x = 0.328125;
    // fragment_color.y = 0.24609375;
    // fragment_color.z = 0.17578125;

    // fragment_color.x = 0.328125;
    // fragment_color.y = 0.24609375;
    // fragment_color.z = 0.17578125;
    fragment_color.xyz = vec3(105./256, 255./256, 18./256);


    // tell OpenGL how to transform the vertex to clip coordinates
    gl_Position = projection * view * model * vec4(position, 1);
    // frag_tex_coords = tex_coord;
}
